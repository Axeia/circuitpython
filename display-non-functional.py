import board
import displayio
import busio
from adafruit_st7789 import ST7789

# Set up SPI
spi = busio.SPI(board.IO12, MOSI=board.IO11)

# Set up display
display_bus = displayio.FourWire(spi, command=board.IO6, chip_select=board.IO5)
display = ST7789(display_bus, width=172, height=320)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(240, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFF0000

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)

while True:
    pass
