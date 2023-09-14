import os
import wifi
import socketpool
import board
import neopixel

'''
Requires a board with WiFi (should be pretty much any S3 board)
Requires a neopixel to control

This is the code that goes hand in hand with neopixel-wifi-controller.py
This script runs on the circuitpython board, the controller code runs on a PC

This script simply listens out and received the data from the controller
and changes its Neopixel accordingly.
'''

# Set up the NeoPixel
pixel_pin = board.NEOPIXEL # NeoPixel pin
num_pixels = 1 # Number of NeoPixels
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

print()
print(f"Connecting to WiFi...")
#  connect to your SSID
wifi.radio.connect(
    # Make sure these are set in settings.toml
    os.getenv('CIRCUITPY_WIFI_SSID'),  # WiFi identifier (name)
    os.getenv('CIRCUITPY_WIFI_PASSWORD')  # WiFi password
)
print(f"Connected to SSID {os.getenv('CIRCUITPY_WIFI_SSID')}")

# Set up a session with the socket pool
pool = socketpool.SocketPool(wifi.radio)

# Create a TCP server socket
server_socket = pool.socket(pool.AF_INET, pool.SOCK_STREAM)

print(f'Please connect to: {wifi.radio.ipv4_address}')
# Bind the socket to an address and port
server_socket.bind((str(wifi.radio.ipv4_address), 12345))
# Listen for incoming connections
server_socket.listen(1)

while True:
    # Accept a connection
    client_socket, addr = server_socket.accept()

    # Try to receive data from the client
    try:
        data = bytearray(1024)
        num_bytes = client_socket.recv_into(data)
    except OSError as e:
        if e.args[0] == 11:  # EAGAIN
            continue  # No data available, try again later
        else:
            raise  # Some other error occurred

    hex_color_code = data[:num_bytes].decode('utf-8')
    brightness, r, g, b = [int(hex_color_code[i:i+2], 16) for i in (1, 3, 5, 7)]

    pixels.fill((r, g, b))
    pixels.brightness = brightness / 255
    pixels.show()
    # Print the received data
    print(hex_color_code)
    print(f'r{r} g{g} b{b} a{brightness}')

    # Close the client socket
    client_socket.close()
