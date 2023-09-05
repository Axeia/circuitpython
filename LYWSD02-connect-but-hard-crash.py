import time
from adafruit_ble.uuid import VendorUUID
from adafruit_ble import BLERadio
from adafruit_ble.advertising import Advertisement

ble = BLERadio()

# Stop any previous scans
ble.stop_scan()

# Scan for the LYWSD02 device
print("Scanning for LYWSD02 device...")
lywsd02_device = None
while not lywsd02_device:
    for advertisement in ble.start_scan(Advertisement):
        if advertisement.complete_name == "LYWSD02":
            lywsd02_device = advertisement
            break

# Stop scanning
ble.stop_scan()
xiaomi_clock_uuid_str = 'EBE0CCB0-7A0A-4B0C-8A1A-6FF2997DA3A6'
# see https://github.com/h4/lywsd02/blob/master/lywsd02/client.py 
# for characteristic UUIDs


if lywsd02_device:
    # Connect to the LYWSD02 device
    print("Connecting to LYWSD02 device...")
    lywsd02_connection = ble.connect(lywsd02_device, timeout=10)

    if lywsd02_connection.connected:
        # Print out the services advertised by the LYWSD02 device
        print("\nLYWSD02 device services:")
        print(f"\n{lywsd02_connection}")
        if VendorUUID(xiaomi_clock_uuid_str) in lywsd02_connection:
            print(f'found {xiaomi_clock_uuid_str}')
        else:
            print(f'Could not find {xiaomi_clock_uuid_str}')

        # Wait for a while to allow services to be printed
        time.sleep(2)
else:
    print("LYWSD02 device not found")
