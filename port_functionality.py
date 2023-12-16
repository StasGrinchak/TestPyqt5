import serial.tools.list_ports

def get_com_ports():
    com_ports = list(serial.tools.list_ports.comports())
    return [port.device for port in com_ports]

com_ports = get_com_ports()

if com_ports:
    print("Доступные COM-порты:")
    for port in com_ports:
        print(port)
else:
    print("COM-порты не найдены.")


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class SerialCommunicationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.serial_port = QSerialPort()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # COM порт
        com_label = QLabel("COM порт:")
        self.com_combobox = QComboBox(self)
        self.populate_com_ports()
        layout.addWidget(com_label)
        layout.addWidget(self.com_combobox)

        # Baud rate
        baud_label = QLabel("Baud rate:")
        self.baud_combobox = QComboBox(self)
        baud_rates = ['9600', '19200', '38400', '57600', '115200']
        self.baud_combobox.addItems(baud_rates)
        layout.addWidget(baud_label)
        layout.addWidget(self.baud_combobox)

        # Введення та виведення даних
        self.input_text = QLineEdit(self)
        self.output_label = QLabel("Виведення даних:")
        layout.addWidget(self.input_text)
        layout.addWidget(self.output_label)

        # Кнопка для взаємодії з пристроєм
        send_button = QPushButton('Відправити дані', self)
        send_button.clicked.connect(self.send_data)
        layout.addWidget(send_button)

        self.setLayout(layout)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Serial Communication App')
        self.show()

    def populate_com_ports(self):
        # Заповнення доступних COM-портів
        com_ports = [info.portName() for info in QSerialPortInfo.availablePorts()]
        self.com_combobox.addItems(com_ports)

    def send_data(self):
        # Взаємодія з пристроєм
        port_name = self.com_combobox.currentText()
        baud_rate = int(self.baud_combobox.currentText())
        input_data = self.input_text.text()

        self.serial_port.setPortName(port_name)
        self.serial_port.setBaudRate(baud_rate)

        if self.serial_port.open(QSerialPort.WriteOnly):
            self.serial_port.write(input_data.encode())
            self.serial_port.close()

            # Оновлення виведення даних
            self.output_label.setText(f"Виведення даних: {input_data}")
        else:
            print(f"Не вдалося відкрити COM-порт {port_name}.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialCommunicationApp()
    sys.exit(app.exec_())




# import usb.core

# devices = usb.core.find(find_all=True)

# for device in devices:
#     lag = device.serial_number
#     print("VID: {}, PID: {:04x}".format(device.bus, device.idProduct))