from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QTextEdit, QMessageBox, QTabWidget, QWidget, QVBoxLayout
from PyQt5.QtSerialPort import QSerialPortInfo


class MainWindow(QMainWindow):
    def __init__(self, serial_port_manager):
        super().__init__()

        self.serial_manager = serial_port_manager
        self.init_ui()

    def init_ui(self):
        # Interface elements
        self.tabs = QTabWidget(self)
        self.addTabButton = QPushButton("Add Terminal", self)
        self.macroComboBox = QComboBox(self)
        self.sendMacroButton = QPushButton("Send Macro", self)

        self.macroComboBox.addItem("Macro 1", "Hello World!")
        self.macroComboBox.addItem("Macro 2", "How are you?")

        # Connecting event handlers
        self.addTabButton.clicked.connect(self.add_terminal_tab)
        self.sendMacroButton.clicked.connect(self.send_macro)

        # Placement of interface elements
        self.setGeometry(100, 100, 600, 400)
        self.tabs.setGeometry(10, 10, 580, 340)
        self.addTabButton.setGeometry(10, 360, 120, 30)
        self.macroComboBox.setGeometry(140, 360, 120, 30)
        self.sendMacroButton.setGeometry(270, 360, 120, 30)

        # Add an initial terminal tab
        self.add_terminal_tab()

    def add_terminal_tab(self):
        index = self.tabs.count() + 1
        tab = QWidget()
        layout = QVBoxLayout(tab)

        port_label = QLabel("COM Port:", tab)
        port_combo = QComboBox(tab)

        baud_rate_label = QLabel("Baud Rate:", tab)
        baud_rate_combo = QComboBox(tab)

        open_port_button = QPushButton("Open Port", tab)
        close_port_button = QPushButton("Close Port", tab)

        data_text_edit = QTextEdit(tab)

        termination_label = QLabel("Termination:", tab)
        termination_combo = QComboBox(tab)
        termination_combo.addItem("CR/LF", "\r\n")
        termination_combo.addItem("LF", "\n")
        termination_combo.addItem("CR", "\r")

        send_data_button = QPushButton("Send Data", tab)

        layout.addWidget(port_label)
        layout.addWidget(port_combo)
        layout.addWidget(baud_rate_label)
        layout.addWidget(baud_rate_combo)
        layout.addWidget(open_port_button)
        layout.addWidget(close_port_button)
        layout.addWidget(data_text_edit)
        layout.addWidget(termination_label)
        layout.addWidget(termination_combo)
        layout.addWidget(send_data_button)

        self.tabs.addTab(tab, f"Terminal {index}")

        # Filling COM ports and baud rate
        ports = [portInfo.portName() for portInfo in QSerialPortInfo.availablePorts()]
        baud_rates = ['9600', '19200', '38400', '57600', '115200']

        port_combo.addItems(ports)
        baud_rate_combo.addItems(baud_rates)

        # Connecting event handlers for this tab
        open_port_button.clicked.connect(lambda: self.open_port_clicked(index))
        close_port_button.clicked.connect(lambda: self.close_port_clicked(index))
        send_data_button.clicked.connect(lambda: self.send_data_clicked(index))

    def open_port_clicked(self, index):
        port_name = self.tabs.widget(index).findChild(QComboBox, "port_combo").currentText()
        baud_rate = int(self.tabs.widget(index).findChild(QComboBox, "baud_rate_combo").currentText())

        if not self.serial_manager.serial_ports[index].isOpen():
            if self.serial_manager.open_port(port_name, baud_rate):
                self.tabs.widget(index).findChild(QPushButton, "open_port_button").setEnabled(False)
                self.tabs.widget(index).findChild(QPushButton, "close_port_button").setEnabled(True)
        else:
            QMessageBox.information(self, 'Port Opened', 'Port is already opened.')

    def close_port_clicked(self, index):
        if self.serial_manager.serial_ports[index].isOpen():
            if self.serial_manager.close_port(index):
                self.tabs.widget(index).findChild(QPushButton, "open_port_button").setEnabled(True)
                self.tabs.widget(index).findChild(QPushButton, "close_port_button").setEnabled(False)
        else:
            QMessageBox.information(self, 'Port Closed', 'Port is already closed.')

    def send_data_clicked(self, index):
        data = self.tabs.widget(index).findChild(QTextEdit, "data_text_edit").toPlainText()
        termination = self.tabs.widget(index).findChild(QComboBox, "termination_combo").currentData()
        self.serial_manager.set_termination(termination)
        self.serial_manager.send_data(index, data)

    def send_macro(self):
        selected_index = self.tabs.currentIndex()
        if selected_index >= 0:
            macro_text = self.macroComboBox.currentData()
            self.send_data_clicked(selected_index, "", macro_text)