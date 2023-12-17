from PyQt5.QtSerialPort import QSerialPort


class SerialPortManager:
    def __init__(self):
        self.serial_ports = []
        self.termination = b'\r\n'

    def open_port(self, port_name, baud_rate):
        serial_port = QSerialPort()
        serial_port.setReadBufferSize(1024)

        if serial_port.isOpen():
            serial_port.close()

        serial_port.setPortName(port_name)
        serial_port.setBaudRate(baud_rate)
        serial_port.setDataBits(QSerialPort.Data8)
        serial_port.setParity(QSerialPort.NoParity)
        serial_port.setStopBits(QSerialPort.OneStop)

        if serial_port.open(QSerialPort.ReadWrite):
            self.serial_ports.append(serial_port)
            return True
        else:
            return False

    def close_port(self, index):
        if 0 <= index < len(self.serial_ports):
            serial_port = self.serial_ports[index]
            if serial_port.isOpen():
                serial_port.close()
                del self.serial_ports[index]
                return True
        return False

    def send_data(self, index, data):
        if 0 <= index < len(self.serial_ports):
            serial_port = self.serial_ports[index]
            if serial_port.isOpen():
                data = (data + self.termination).encode('utf-8')
                serial_port.write(data)
                return True
        return False

    def read_data(self, index):
        if 0 <= index < len(self.serial_ports):
            serial_port = self.serial_ports[index]
            if serial_port.isOpen():
                data = serial_port.readAll()
                return bytes(data).decode('utf-8')
        return None

    def set_termination(self, termination):
        self.termination = termination