import board
import busio
import displayio
from adafruit_st7789 import ST7789 # https://github.com/adafruit/Adafruit_CircuitPython_ST7789
from adafruit_display_text import label
import terminalio

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

displayio.release_displays()

MOSI_PIN = board.IO11 # Fixed pin - do not change
SCK_PIN = board.IO12  # Fixed pin - do not change

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

display = ST7789(display_bus, width=320, height=172, colstart=34, rotation=270)

splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(320, 172, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFF0000

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Create the text label
text = "Hello, World!"
text_area = label.Label(terminalio.FONT, text=text)
text_area.x = 10
text_area.y = 10

# Add the text label to the group
splash.append(text_area)

# MISO does not need to be connected.
# MISO_PIN = board.IO13 # Fixed pin - do not change

# Main loop:
while True:
    pass
