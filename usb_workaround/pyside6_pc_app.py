from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
import sys
import time

class Window(QtWidgets.QColorDialog):
    def __init__(self):
        super().__init__()
        self.list_serial_ports()
        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
        self.serial = QSerialPort()
        self.serial.setPortName('COM6')
        self.serial.setBaudRate(QSerialPort.Baud115200)
        self.serial.open(QtCore.QIODevice.ReadWrite)
        self.last_update = time.time()

        self.currentColorChanged.connect(self.sendSerial)
        self.serial.errorOccurred.connect(self.handleError)

    def sendSerial(self):
        current_time = time.time()
        if current_time - self.last_update >= 0.1:
            color = self.currentColor().name(QtGui.QColor.NameFormat.HexArgb)
            # Skip the '#' and convert hex to int
            self.serial.write(color.encode('utf-8'))
        self.last_update = current_time

    def list_serial_ports(self):
        ports = QSerialPortInfo.availablePorts()
        for port in ports:
            print(port.portName())

    def handleError(self, error):
        if error != QSerialPort.NoError:
            print(f"An error occurred: {error}")

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.serial.close()


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
app.exec()
