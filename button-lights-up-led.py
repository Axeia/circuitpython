import time
import board
import digitalio
import neopixel

# Set up the NeoPixel
pixel_pin = board.NEOPIXEL # NeoPixel pin
num_pixels = 1 # Number of NeoPixels
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

# Set the colors
RED = (255, 0, 0)
OFF = (0, 0, 0)

# Set up the push button switch
switch_pin = board.IO43 # Switch pin
switch = digitalio.DigitalInOut(switch_pin)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.DOWN

while True:
    if switch.value: # If the switch is pressed
        pixels.fill(RED) # Turn on the NeoPixel
    else:
        pixels.fill(OFF) # Turn off the NeoPixel
    pixels.show()
    time.sleep(0.1) # Wait for 0.1 second
