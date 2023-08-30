import board
import displayio
from adafruit_st7789 import ST7789
import time

# Release any resources currently in use for the displays
displayio.release_displays()

# Set up the SPI connection
spi = board.SPI()
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000)
spi.unlock()

# Set up the display
tft_cs = board.IO10
tft_dc = board.IO9
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.IO8)
display = ST7789(display_bus, width=172, height=320)
print("Display initialized")

# Create a display group for our screen objects
splash = displayio.Group()
display.show(splash)

# Create a bitmap with a single color
color_bitmap = displayio.Bitmap(172, 320, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFF0000 # Red

# Create a TileGrid using the Bitmap and Palette
background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette)

# Add the background to the display group
splash.append(background)
print("Background added to display group")
# Wait for the display to refresh
time.sleep(1)

# Keep the program running to keep the image on screen
while True:
    pass
