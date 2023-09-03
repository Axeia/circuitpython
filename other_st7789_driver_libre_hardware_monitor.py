import board
import busio
import displayio
from adafruit_st7789 import ST7789 # https://github.com/adafruit/Adafruit_CircuitPython_ST7789
from adafruit_display_text import label
import terminalio
import wifi 
import socketpool
import ssl
import adafruit_requests
from adafruit_display_shapes.rect import Rect
import time


'''
BPI-Leaf-S3 pinout:
(High res image:)[https://wiki.banana-pi.org/images/7/7e/Leaf-S3_board.png]
| Function | ADC      | Touch    | Analog    | IO |  IO | Analog    | Touch   | ADC      | Function |
|----------|----------|----------|-----------|---:|----:|-----------|---------|----------|----------|
|          |          |          | 3.3v      |    | GND |           |         |          |          |
|          |          |          | 3.3v      |    |  43 |           |         |          | TX       |
|          |          |          | RESET     | EN |  44 |           |         |          | RX       |
|          | ADC1_CH3 | Touch 4  |  Analog 3 |  4 |   1 | Analog 0  | Touch 1 | ADC1_CH0 |          |
|          | ADC1_CH4 | Touch 5  |  Analog 4 |  5 |   2 | Analog 1  | Touch 2 | ADC1_CH1 |          |
|          | ADC1_CH5 | Touch 6  |  Analog 5 |  6 |  42 |           |         |          |          |
|          | ADC1_CH6 | Touch 7  |  Analog 6 |  7 |  41 |           |         |          |          |
| SDA      | ADC2_CH4 |          | Analog 14 | 15 |  40 |           |         |          |          |
| SCL      | ADC2_CH5 |          | Analog 15 | 16 |  39 |           |         |          |          |
|          | ADC2_CH6 |          | Analog 16 | 17 |  38 |           |         |          |          |
|          | ADC2_CH7 |          | Analog 17 | 18 |  37 |           |         |          |          |
|          | ADC1_CH7 | Touch 8  |  Analog 7 |  8 |  36 |           |         |          |          |
|          | ADC1_CH2 | Touch 3  |  Analog 2 |  3 |  35 |           |         |          |          |
|          |          |          |           | 46 |   0 |           |         |          | BOOT     |
|          | ADC1_CH8 | Touch 9  |  Analog 8 |  9 |  45 |           |         |          |          |
| SS       | ADC1_CH9 | Touch 10 |  Analog 9 | 10 |  48 |           |         |          |          |
| MOSI     | ADC2_CH0 | Touch 11 | Analog 10 | 11 |  47 |           |         |          |          |
| SCK      | ADC2_CH1 | Touch 12 | Analog 11 | 12 |  21 |           |         |          |          |
| MISO     | ADC2_CH2 | Touch 13 | Analog 12 | 13 |  20 | Analog 19 |         | ADC2_CH9 |          |
|          | ADC2_CH3 | Touch 14 | Analog 13 | 14 |  19 | Analog 18 |         | ADC2_CH8 |          |


ST7789 1.47" inch IPS Display 172*320 resolution, SPI Interface
pinout + connect to:
GND  --> Board GND
VCC  --> Board 3.3v
SCL  --> Board IO12 [Board SCK] (Fixed - do not change)
SDA  --> Board IO11 [Board MOSI] (Fixed - do not change)
RES  --> Board IO5 (Not fixed, just pick an IO pin)
DC   --> Board IO6 (Not fixed, just pick an IO pin)
CS   --> Board IO7 (Not fixed, just pick an IO pin)
BLK  --> Not connected
'''

# Edit these variables to reflect your environment.
WIFI_SSID = "Your Wifi Network Name"
WIFI_PASSWORD = "Your Wifi password" #Storing it as plain text is probably not smart
LIBRE_DATA_URL = "http://192.168.1.102:8085/data.json" # data.json URL from Libre Hardware Monitor

'''
    Prepare display and UI
'''

displayio.release_displays()

MOSI_PIN = board.IO11 # Fixed pin - do not change
SCK_PIN = board.IO12  # Fixed pin - do not change

def setup_display() -> ST7789:
    # Set up the SPI connection
    spi = busio.SPI(SCK_PIN, MOSI_PIN)
    while not spi.try_lock():
        pass
    spi.configure(baudrate=24000000) # Configure SPI for 24MHz
    spi.unlock()

    # Set up the display
    RESET_PIN = board.IO5  # Can be changed
    DC_PIN = board.IO6  # Can be changed
    CS_PIN = board.IO7  # Can be changed

    display_bus = displayio.FourWire(spi, command=DC_PIN, chip_select=CS_PIN, reset=RESET_PIN)

    return ST7789(display_bus, width=320, height=172, colstart=34, rotation=270)

display = setup_display()
text_y_offset = 40

def add_ui_segments(display: ST7789) -> displayio.Group:
    splash = displayio.Group()
    display.show(splash)

    first_rect_height = int(display.height/2) - 2
    rect_cpu = Rect(0, 0, int(display.width/3), first_rect_height, fill=0x00FF00)
    rect_gpu = Rect(0, first_rect_height+4, int(display.width/3), int(display.height/2) - 2, fill=0x00FF00)
    splash.append(rect_cpu)
    splash.append(rect_gpu)

    # Create the text label
    text = "CPU: "
    text_area = label.Label(terminalio.FONT, text=text, scale=4)
    text_area.x = 10
    text_area.y = text_y_offset
    # Add the text label to the group
    splash.append(text_area)


    text2 = "GPU: "
    text_area2 = label.Label(terminalio.FONT, text=text2, scale=4)
    text_area2.x = 10
    text_area2.y = int(display.height/2) + text_y_offset
    # Add the text label to the group
    splash.append(text_area2)

    return splash

add_ui_segments(display)

'''
    Set up Wifi connection and add methods to parse JSON
'''
def connect_to_wifi(network_name: str, password: str) -> tuple:
    print(f"Connecting to {network_name}...")
    wifi.radio.connect(network_name, password)
    print(
        f"Connected to {network_name} and assigned ip: {wifi.radio.ipv4_address}")

    # Create a socket pool and an SSL context
    pool = socketpool.SocketPool(wifi.radio)
    ssl_context = ssl.create_default_context()

    return (pool, ssl_context)


def fetch_libre_hwm_data(pool: socketpool.SocketPool, ssl_context: ssl.SSLContext) -> dict:
    requests = adafruit_requests.Session(pool, ssl_context)
    try:
        response = requests.get(LIBRE_DATA_URL)
        print(f'[Success] Fetched data from {LIBRE_DATA_URL}')
        return response.json()
    except Exception as e:
        print(f"['Error'] Failed to fetch data from {LIBRE_DATA_URL}: {e}")
        return {}

def iterate_nodes(data, path: str = "") -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}/{key}" if path else key
            iterate_nodes(value, new_path)

            if key == "Text":
                if value.startswith("AMD Ryzen")\
                        or value.startswith("Intel Core"):
                    add_stats('CPU', data['Children'])
                if value.startswith("ATI Radeon")\
                        or value.startswith("AMD Radeon")\
                        or value.startswith("NVIDIA"):
                  add_stats('GPU', data['Children'])
    elif isinstance(data, list):
        for i, value in enumerate(data):
            new_path = f"{path}/{i}"
            iterate_nodes(value, new_path)

stats = {}
def add_stats(stat: str, data):
  stats[stat] = []
  # Finds the temperatures node and extracts the temperatures to populate stats
  for child in data:
      if 'Text' in child and child['Text'] == 'Temperatures':
          for grandChild in child['Children']:
              stats[stat].append(grandChild["Value"])

pool, ssl_context = connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)

# Main loop:
while True:
    json = fetch_libre_hwm_data(pool, ssl_context)
    iterate_nodes(json)

    base_x_offset = 120
    group = add_ui_segments(display)

    # Add CPU stats:
    cpu_x_offset = base_x_offset
    if 'CPU' in stats:
        for temp in stats['CPU']:
            text_area = label.Label(terminalio.FONT, text=temp, scale=2)
            text_area.x = cpu_x_offset + 20
            text_area.y = text_y_offset
            group.append(text_area)

            cpu_x_offset += 80

    # GPU stats:
    gpu_x_offset = base_x_offset
    if 'GPU' in stats:
        for temp in stats['GPU']:
            text_area = label.Label(terminalio.FONT, text=temp, scale=2)
            text_area.x = gpu_x_offset + 20
            text_area.y = int(display.height / 2) + text_y_offset
            group.append(text_area)

            gpu_x_offset += 80

    display.show(group)
    if json == {}:
        time.sleep(10)
    else:
        time.sleep(3)
