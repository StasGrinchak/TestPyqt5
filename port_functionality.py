from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class SerialPortManager:
    def __init__(self):
        self.serial_port = QSerialPort()
        self.serial_port.setReadBufferSize(1024)

    def open_port(self, port_name, baud_rate):
        # Closing the port if it is already open
        if self.serial_port.isOpen():
            self.serial_port.close()

        # Setting the port parameters
        self.serial_port.setPortName(port_name)
        self.serial_port.setBaudRate(baud_rate)
        self.serial_port.setDataBits(QSerialPort.Data8)
        self.serial_port.setParity(QSerialPort.NoParity)
        self.serial_port.setStopBits(QSerialPort.OneStop)

        # Opening the port
        if self.serial_port.open(QSerialPort.ReadWrite):
            return True
        else:
            return False

    def close_port(self):
        # Close the port
        if self.serial_port.isOpen():
            self.serial_port.close()
            return True
        else:
            return False

    def send_data(self, data):
        # Send data to device
        if self.serial_port.isOpen():
            data = data.encode('utf-8')
            self.serial_port.write(data)
            return True
        else:
            return False

    def read_data(self):
        # Receiving data from the port
        if self.serial_port.isOpen():
            data = self.serial_port.readAll()
            return bytes(data).decode('utf-8')
        else:
            return None

    def set_termination(self, termination):
        # Set the end-of-line character
        self.termination = termination


class MainWindow(QMainWindow):
    def __init__(self, serial_port_manager):
        super().__init__()

        self.serial_manager = serial_port_manager
        self.init_ui()

    def init_ui(self):
        # Interface elements
        self.port_label = QLabel("COM Port:", self)
        self.port_combo = QComboBox(self)

        self.baud_rate_label = QLabel("Baud Rate:", self)
        self.baud_rate_combo = QComboBox(self)

        self.open_port_button = QPushButton("Open Port", self)
        self.close_port_button = QPushButton("Close Port", self)
        self.send_data_button = QPushButton("Send Data", self)

        self.data_text_edit = QTextEdit(self)

        self.termination_label = QLabel("Termination:", self)
        self.termination_combo = QComboBox(self)
        self.termination_combo.addItem("CR/LF", "\r\n")
        self.termination_combo.addItem("LF", "\n")
        self.termination_combo.addItem("CR", "\r")

        # Placement of interface elements
        self.setGeometry(100, 100, 400, 300)

        self.port_label.setGeometry(10, 10, 80, 25)
        self.port_combo.setGeometry(100, 10, 100, 25)

        self.baud_rate_label.setGeometry(10, 40, 80, 25)
        self.baud_rate_combo.setGeometry(100, 40, 100, 25)

        self.open_port_button.setGeometry(10, 80, 120, 30)
        self.close_port_button.setGeometry(140, 80, 120, 30)

        self.data_text_edit.setGeometry(10, 120, 250, 70)

        self.termination_label.setGeometry(10, 200, 80, 25)
        self.termination_combo.setGeometry(100, 200, 100, 25)

        self.send_data_button.setGeometry(10, 240, 250, 30)

        # Filling COM ports and baud rate
        ports = [portInfo.portName() for portInfo in QSerialPortInfo.availablePorts()]
        baud_rates = ['9600', '19200', '38400', '57600', '115200']

        self.port_combo.addItems(ports)
        self.baud_rate_combo.addItems(baud_rates)

        # Connecting event handlers
        self.open_port_button.clicked.connect(self.open_port_clicked)
        self.close_port_button.clicked.connect(self.close_port_clicked)
        self.send_data_button.clicked.connect(self.send_data_clicked)

    def open_port_clicked(self):
        port_name = self.port_combo.currentText()
        baud_rate = int(self.baud_rate_combo.currentText())

        if not self.serial_manager.serial_port.isOpen():
            if self.serial_manager.open_port(port_name, baud_rate):
                self.open_port_button.setEnabled(False)
                self.close_port_button.setEnabled(True)
        else:
            QMessageBox.information(self, 'Th port is open', 'The port is already open!')
            
    def close_port_clicked(self):
        if self.serial_manager.serial_port.isOpen():
            self.serial_manager.close_port()
            self.open_port_button.setEnabled(True)
            self.close_port_button.setEnabled(False)
        else:
            QMessageBox.information(self, 'The port is closed', 'The port is already closed!')

    def send_data_clicked(self):
        data = self.data_text_edit.toPlainText()
        termination = self.termination_combo.currentData()
        self.serial_manager.set_termination(termination)
        self.serial_manager.send_data(data)


if __name__ == '__main__':
    app = QApplication([])

    serial_manager = SerialPortManager()
    window = MainWindow(serial_manager)

    window.show()
    app.exec_()




# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox
# from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


# class SerialCommunicationApp(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.serial_port = QSerialPort()
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # COM ports
#         com_label = QLabel("COM port:")
#         self.com_combobox = QComboBox(self)
#         self.populate_com_ports()
#         layout.addWidget(com_label)
#         layout.addWidget(self.com_combobox)

#         # Baud rate
#         baud_label = QLabel("Baud rate:")
#         self.baud_combobox = QComboBox(self)
#         baud_rates = ['9600', '19200', '38400', '57600', '115200']
#         self.baud_combobox.addItems(baud_rates)
#         layout.addWidget(baud_label)
#         layout.addWidget(self.baud_combobox)

#         # Введення та виведення даних
#         self.input_text = QLineEdit(self)
#         self.output_label = QLabel("Outputting data:")
#         layout.addWidget(self.input_text)
#         layout.addWidget(self.output_label)

#         # Кнопка для взаємодії з пристроєм
#         send_button = QPushButton('Send data', self)
#         send_button.clicked.connect(self.send_data)
#         layout.addWidget(send_button)

#         self.setLayout(layout)
#         self.setGeometry(300, 300, 400, 300)
#         self.setWindowTitle('Serial Communication App')
#         self.show()

#     def populate_com_ports(self):
#         # Заповнення доступних COM-портів
#         com_ports = [info.portName() for info in QSerialPortInfo.availablePorts()]
#         self.com_combobox.addItems(com_ports)

#     def send_data(self):
#         # Взаємодія з пристроєм
#         port_name = self.com_combobox.currentText()
#         baud_rate = int(self.baud_combobox.currentText())
#         input_data = self.input_text.text()

#         self.serial_port.setPortName(port_name)
#         self.serial_port.setBaudRate(baud_rate)

#         if self.serial_port.open(QSerialPort.WriteOnly):
#             self.serial_port.write(input_data.encode())
#             self.serial_port.close()

#             # Оновлення виведення даних
#             self.output_label.setText(f"Виведення даних: {input_data}")
#         else:
#             print(f"Не вдалося відкрити COM-порт {port_name}.")


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = SerialCommunicationApp()
#     sys.exit(app.exec_())