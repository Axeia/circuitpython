# How did this come to be
I wanted to send a color over serial to my BPI-Leaf-S3 to change its Neopixel color so I wrote pyside6_pc_app.py which sends a color through serial over USB.
However, the Banana Pi Leaf S3 (BPI-LEAF-S3) I use only has a couple of USB end points. Quoting the [documentation](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/how-many-usb-devices-can-i-have)
> ESP32-S2 and ESP32-S3 effectively provide only 4 pairs, not counting pair 0. (There are 6 pairs, but the hardware allows only 4 IN endpoints active at a time, not including pair 0.) So if you wanted both CDC console and data, you would have to turn everything else off, including CIRCUITPY.

Losing the CIRCUITPY drive sounds like a bad time to me, I'm not quite sure how you'd save a file without it.
So I decided that losing the CDC console would be the lesser of two evils and I could somewhat replicate its functionality by outputting errors and print message to UART instead.
Then if I take in the UART on a second board (a vanilla ESP32 dev board) connected to my PC and read that out through the serial monitor I still have some debugging options.

# pyside6_pc_app.py
This is a very simple program I wrote using PySide6 (so it should be extremely easy to port to C(++) if that's your preference). 
All it does is when you change the color it sends that color out over serial (COM6 by default, adjust to your COM port or non-windows equivelant)

# esp32.ino 
Arduino IDE code for the ESP32 that I use to monitor the serial output

# boot.py
Needed to disable the console and enable the now freed up COM port to take in data

# How this setup works
  1. The PC App (pyside6_pc_app.py) sends the color to the BPI-Leaf-S3 running circuitpy_main_code.py
  2. The BPI-Leaf-S3 receives the color and sets Neopixel to match and redirects any errors/print statements to UART
  3. The ESP32 receives anything send over UART and prints it to the serial monitor
  4. You get to watch the pixel change and any errors on the ESP32 serial monitor

# How to
  1. Connect the two boards together RX of one to TX on the other and vice versa and connect ground to ground as well
  2. Copy paste the content of circuitpy_main_code.py to your code.py or main.py file on your CIRCUITPY drive
  3. Copy boot.py to your CIRCUITPY drive (it doesn't exist by default so you have to create it) and perform a hard reset
    * It doesn't actually get picked up on untill you do a hard reset on the board by pressing the reset button or replugging the whole thing (assuming you don't have a battery connected)
  4. Compile and upload ReadSerialUART.ino in Arduino IDE to your 'listening' board and then open your Serial Monitor
  5. Run pyside6_pc_app.py on your PC and change the color and hopefully everything works, and if it doesn't hopefully errors can be seen in the serial monitor of the listening board
