
from resources.fm_trasfer_file_server import Ui_MainWindow
from service.thread_socket import ListeningThread
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir, QModelIndex
from PyQt5.QtWidgets import QFileSystemModel

class FileTransferServer(Ui_MainWindow):
    def __init__(self):
         self.setupUi(MainWindow)


    def start_process_thread(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = FileTransferServer()

    MainWindow.show()
    sys.exit(app.exec_())