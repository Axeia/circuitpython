from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtNetwork
import sys
import time

'''
Please note that this script is meant to be ran on a PC with full fledged python,
it goes hand in hand with neopixel_wifi_listener.py

Also note the PySide6 dependencies above, so don't forget to run:
pip install pyside6
Don't forget to change the IP address on line #37 to suit your local environment either
''' 
class Window(QtWidgets.QColorDialog):
    def __init__(self):
        super().__init__()
        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
        self.last_update = time.time()
        self.currentColorChanged.connect(self.sendColor)


    def sendColor(self):
        print('Sending color')
        current_time = time.time()
        if current_time - self.last_update >= 0.1:
            color = self.currentColor().name(QtGui.QColor.NameFormat.HexArgb)
            self.sendPacket(color)
            print('Sent packet')
        self.last_update = current_time

    def sendPacket(self, color: str):
        # Create a new TCP socket
        socket = QtNetwork.QTcpSocket()

        # Connect the socket to the server
        socket.connectToHost('192.168.1.186', 12345)

        # Wait for the connection to be established
        if not socket.waitForConnected(1000):
            print("Error:", socket.errorString())
            sys.exit(1)

        # Send some data
        socket.write(color.encode('utf-8'))

        # Wait for the data to be sent
        if not socket.waitForBytesWritten(1000):
            print("Error:", socket.errorString())

        # Close the socket
        socket.close()

app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
app.exec()
