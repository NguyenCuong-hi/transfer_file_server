import socket
from PyQt5.QtCore import QThread, pyqtSignal
import threading
import select


class ListeningThread(QThread):
    transfer_progress = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.running = True
        self.server_socket = None

    def run(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            server_socket.setblocking(False)
            self.transfer_progress.emit(f"Listening on {self.host}:{self.port}...")

            while self.running:
                try:
                    ready_to_read, _, _ = select.select([server_socket], [], [], 1)
                    if ready_to_read:
                        client_socket, client_address = server_socket.accept()
                        self.transfer_progress.emit(f"Connected to {client_address}")

                        client_thread = threading.Thread(target=self.handle_client,
                                                         args=(client_socket, client_address))
                        client_thread.start()
                except Exception as e:
                    self.transfer_progress.emit(f"Error: {str(e)}")

            server_socket.close()
            self.transfer_progress.emit("Server stopped.")
        except Exception as e:
            self.transfer_progress.emit(f"Server error: {str(e)}")

        finally:
            if self.server_socket:
                self.server_socket.close()
            self.transfer_progress.emit("Server stopped.")

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                self.transfer_progress.emit(f"Received from {client_address}: {data}")

                response = "Data received"
                client_socket.send(response.encode('utf-8'))

        except Exception as e:
            self.transfer_progress.emit(f"Error handling client {client_address}: {str(e)}")
        finally:
            client_socket.close()
            self.transfer_progress.emit(f"Connection with {client_address} closed.")
