import time
import board
import neopixel

# Set up the NeoPixel
pixel_pin = board.NEOPIXEL # NeoPixel pin
num_pixels = 1 # Number of NeoPixels
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

# Set the colors
RED = (255, 0, 0)
OFF = (0, 0, 0)

while True:
    pixels.fill(RED) # Turn on the NeoPixel
    pixels.show()
    time.sleep(1) # Wait for 1 second
    pixels.fill(OFF) # Turn off the NeoPixel
    pixels.show()
    time.sleep(1) # Wait for 1 second
