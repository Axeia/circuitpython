# circuitpython
Just a literal repository for me to dump some scripts that I got working on a Banana Pi Leaf S3 (BPI-Leaf-S3) using circuitpython.
Not really intended to be supported in any way :)

I don't plan on going in depth how I have things wired up etc etc so if you're hoping to replicate what I have done the best thing I can do is to suggest looking at my code and reverse engineering from there.
I did go fairly in depth in the st7789 example as it took me quite some time to get it running.

I'm using:
* [circuitpython 8.2.3](https://circuitpython.org/board/bpi_leaf_s3/)
* [libraries from adafruits library bundle for circuitpython 8.x](https://circuitpython.org/libraries)
* [Banana Pi Leaf S3 (BPI-Leaf-S3)](https://wiki.banana-pi.org/BPI-Leaf-S3)
* [A very cheap 1.47" SPI display from Aliexpress](https://vi.aliexpress.com/item/1005003771379232.html)
![BPI-Leaf-S3 pinout](https://wiki.banana-pi.org/images/7/7e/Leaf-S3_board.png)

# Display Shenanigans 
## adafruit_rgb_display/st7789.py
The 'default' library st7789 driver (adafruit_rgb_display/st7789.py) doesn't offer much functionality and would require a lot of extra code to do things with but its pixel and rectangle methods do work! 
The big plus is that it allows using more than one display at the same time.
## https://github.com/adafruit/Adafruit_CircuitPython_ST7789
This displayio st7789 offers a lot more functionality **but** doesn't allow the use of more than one SPI display as it gives a 
`RuntimeError: Too many display busses` 

examples of both are up.

# No License
This isn't really for a functional program or anything so feel free to do whatever you want with the code on here
