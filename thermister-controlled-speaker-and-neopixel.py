import board
import analogio
import digitalio
import math
import time
import neopixel

pixel_pin = board.NEOPIXEL
num_pixels = 1
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write = False)

color_cold = (0, 0, 255)
color_medium = (255, 215, 0)
color_hot = (255, 0, 0)

speaker_pin = board.IO17 
speaker = digitalio.DigitalInOut(speaker_pin)
speaker.direction = digitalio.Direction.OUTPUT

# Define the analog input pin
analog_in = analogio.AnalogIn(board.IO18)  

# Thermistor parameters (you may need to adjust these based on your thermistor's datasheet)
R0 = 10000  # Reference resistance at 25°C
T0 = 25     # Temperature at which R0 is specified (usually 25°C)
B = 3950    # Beta value from the thermistor datasheet

# Function to calculate temperature from resistance
def calculate_temperature(R):
    return 1 / ((1 / (T0 + 273.15)) + ((1 / B) * math.log(R / R0)))

while True:
    # Read the analog value from the thermistor
    raw_value = analog_in.value
    
    # Skip calculations if the raw value is too small (potential division by zero)
    if raw_value < 10:
        continue
    
    # Calculate the resistance of the thermistor
    R = (65535 / raw_value - 1) * 10000  # Assuming a 10k pull-up resistor
    
    # Calculate the temperature
    temperature = calculate_temperature(R)
    temperature = temperature - 271
    
    if temperature < 24:
        pixels.fill(color_cold)
        speaker.value = False
    elif temperature < 28:
        pixels.fill(color_medium)
        speaker.value = False
    else:
        pixels.fill(color_hot)
        speaker.value = True
    pixels.show()
    
    print("Temperature: {:.2f} °C".format(temperature))
    
    # Add a delay to avoid reading too frequently
    time.sleep(1)
