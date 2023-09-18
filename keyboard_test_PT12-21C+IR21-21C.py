import time
import board
from analogio import AnalogIn

'''
Keyboard base test.

PT12-21C is connected as such:
    - Side without the triangle to IO8 and a 10k resistor and ground
    - Side with the triangle to 3.3v

IR21-21C is connected as such:
    - Side with the triangle to a 100 ohm resistor to 3.3v
        * 100ohm resistor drops the amperage to a safe level
    - Side without the triangle straight to ground

Lining both LEDs up should result in serial output.
Considering the size of the components and how direct they need to line up if 
you're just testing I recommend just grabbing a IR-remote and pointing it at the
PT12-21C whilst pushing some buttons.

On most smartphones you can use the camera to see if your remote emits infrared
it shows up as purple. That way you can see if your remote constantly sends 
signals and if you can hold down a button or have to repeatedly press it.

Note: The IR21-21C might not be suitable for testing this way as my own phone
(Xiaomi Mi Mix 2S) could not see the small amount of light it puts out.
'''

analog_in = AnalogIn(board.IO8)

while True:
    val = analog_in.value
    # 60000 should filter out random noise rather than direct exposure to 
    # the IR-LED (IR21-21C)
    if val > 60000: 
        print(val)

    time.sleep(0.1)
