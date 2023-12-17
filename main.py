from PyQt5.QtWidgets import QApplication
from gui import MainWindow
from port_functionality import SerialPortManager


if __name__ == '__main__':
    app = QApplication([])

    serial_manager = SerialPortManager()
    window = MainWindow(serial_manager)

    window.show()
    app.exec_()