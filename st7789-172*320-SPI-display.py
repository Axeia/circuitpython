import board
import digitalio
import time
import busio
from adafruit_rgb_display.st7789 import ST7789
from adafruit_rgb_display import color565

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

# Set up the SPI connection
spi = board.SPI()

# Set up the display
RESET_PIN = board.IO5 # Can be changed
DC_PIN    = board.IO6 # Can be changed
CS_PIN    = board.IO7 # Can be changed

MOSI_PIN = board.IO11 # Fixed pin - do not change
SCK_PIN = board.IO12  # Fixed pin - do not change
#MISO does not need to be connected.
#MISO_PIN = board.IO13 # Fixed pin - do not change
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=SCK_PIN, MOSI=MOSI_PIN)#, MISO=MISO_PIN)

# Create the ST7789 display:
display = ST7789(
    spi,
    rotation=90,
    width=172,
    height=320,
    x_offset=34, # Trial and error - 34 seems to be right.
    y_offset=0,
    baudrate=BAUDRATE,
    cs=digitalio.DigitalInOut(CS_PIN),
    dc=digitalio.DigitalInOut(DC_PIN),
    rst=digitalio.DigitalInOut(RESET_PIN))

# Main loop:
while True:
    # Clear the display
    display.fill(0)
    # Draw a red pixel in the center.
    display.pixel(86, 160, color565(255, 0, 0))
    # Pause 2 seconds.
    time.sleep(2)
    # Clear the screen blue.
    display.fill(color565(0, 0, 255))
    # Pause 2 seconds.
    time.sleep(2)
