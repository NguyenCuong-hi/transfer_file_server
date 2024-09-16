from resources.fm_trasfer_file_server import Ui_MainWindow
from service.thread_socket import ListeningThread
import sys
from list_host.thread_get_data_host import HostConnectionAccess
from config_server.setting_server import checking_init_file_setting
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir, QModelIndex
from PyQt5.QtWidgets import QFileSystemModel

current_dir = os.path.abspath(os.path.dirname(__file__))
PATH = os.path.abspath(os.path.join(current_dir))


def get_data_client():
    host_connection = HostConnectionAccess()
    return host_connection.get_data()


class FileTransferServer(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.host = None
        self.port = None
        self.clients = get_data_client()
        self.load_device_list(data=self.clients)
        self.tb_device.cellClicked.connect(self.on_click_tb_device)
        self.btn_add.clicked.connect(self.create_by)
        self.btn_update.clicked.connect(self.update_by)
        self.btn_delete.clicked.connect(self.delete_by)
        self.btn_reset.clicked.connect(self.reset_information)

        _, self.host, self.port,  host_db, username_db, password_db, port_db, schema = checking_init_file_setting(
            file_path=PATH + '/server.json')

        self.listening_thread = ListeningThread(host=self.host, port=self.port)
        self.listening_thread.start()

    def load_device_list(self, data):
        data_filtered = data.iloc[:, 1:]
        self.tb_device.setRowCount(len(data))
        self.tb_device.setColumnCount(len(data.columns))
        for i in range(len(data)):
            for j in range(len(data.columns)):
                value = str(data.iloc[i, j])
                self.tb_device.setItem(i, j, QtWidgets.QTableWidgetItem(value))

    def on_click_tb_device(self, row, column):
        row_data = []
        for col in range(self.tb_device.columnCount()):
            item = self.tb_device.item(row, col)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append("")
        print(f"%s: %s %s" % (row, column, row_data))

        self.txt_id.setText(row_data[0])
        self.txt_name.setText(row_data[1])
        self.txt_ip.setText(row_data[2])
        self.txt_port.setText(row_data[3])

    def create_by(self):
        client = [
            '',
            self.txt_name.toPlainText(),
            self.txt_ip.toPlainText(),
            self.txt_port.toPlainText(),
            ''
        ]

        clients = HostConnectionAccess()
        clients.create_by(client=client)

        self.clients = get_data_client()
        self.load_device_list(data=self.clients)

    def update_by(self):
        client = [
            self.txt_id.toPlainText(),
            self.txt_name.toPlainText(),
            self.txt_ip.toPlainText(),
            self.txt_port.toPlainText(),
            ''
        ]

        clients = HostConnectionAccess()
        clients.update_by(client=client, id=self.txt_id.toPlainText())

        self.clients = get_data_client()
        self.load_device_list(data=self.clients)

    def delete_by(self):
        clients = HostConnectionAccess()
        clients.delete_by(id=self.txt_id.toPlainText())

        self.clients = get_data_client()
        self.load_device_list(data=self.clients)

    def reset_information(self):
        self.txt_id.setText("")
        self.txt_name.setText("")
        self.txt_ip.setText("")
        self.txt_port.setText("")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = FileTransferServer()

    ui.show()
    sys.exit(app.exec_())
