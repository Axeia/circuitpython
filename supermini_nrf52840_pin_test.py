import board
import digitalio

'''
 Note that this is for the SuperMini NRF52840 board (or Nice!Nano)
 as a quick way to validate if all the pins are working. 

 Short any of the data pins to ground and it should spit out the pin
 number in the serial.

 The SuperMini NRF52840 is a clone of the Nice!Nano and uses the exact
 same pins. To adapt this to any other board figure out which pins it has with:
 import board
 print(dir(board))
'''

# Get a list of all pin names in the board module
all_pins = [
    'P0_06', 'P0_08', 'P0_17', 'P0_20', 'P0_22', 'P0_24', 'P1_00', 'P0_11', 'P1_04', 'P1_06',
    'P0_31', 'P0_29', 'P0_02', 'P1_15', 'P1_13', 'P1_11', 'P0_10', 'P0_09',
    'P1_01', 'P1_02', 'P1_07'
]

pins = []

# Set up all pins as inputs with pull-ups
for pin_name in all_pins:
    pin = getattr(board, pin_name)
    p = digitalio.DigitalInOut(pin)
    p.direction = digitalio.Direction.INPUT
    p.pull = digitalio.Pull.UP
    pins.append(p)

while True:
    # Check each pin. If it's pulled low (connected to GND), print its name.
    for i, pin in enumerate(pins):
        if not pin.value:
            print(f"Pin {all_pins[i]} is shorted to ground.")
