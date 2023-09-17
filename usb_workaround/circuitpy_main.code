import board
import busio
import traceback
import usb_cdc

uart = busio.UART(board.TX, board.RX, baudrate=115200)

# Redirect print statements to UART as we can't see the usual REPL output
def print(*args, **kwargs):
    uart.write(' '.join(map(str, args)).encode())
    uart.write(b'\n')

print('Testing UART print')

while(True):
    try:
        if usb_cdc.data.in_waiting > 0:  # if data is available to read
            # read the incoming data
            data = usb_cdc.data.read(usb_cdc.data.in_waiting)
            print(data)  # print the incoming data
        pass
    #Redirect errors to uart
    except Exception as e:
        error_message = ''.join(traceback.format_exception(None, e, e.__traceback__))
        uart.write(error_message.encode())
