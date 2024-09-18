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
            # server_socket.setblocking(True)
            self.transfer_progress.emit(f"Listening on {self.host}:{self.port}...")

            while self.running:
                try:
                    # ready_to_read, _, _ = select.select([server_socket], [], [], 1)
                    # if ready_to_read == True:
                    client_socket, client_address = server_socket.accept()
                    self.transfer_progress.emit(f"Connected to {client_address}")

                    # client_thread = threading.Thread(target=self.handle_client,
                    #                                  args=(client_socket, client_address))
                    # client_thread.start()

                    self.handle_client(client_socket=client_socket, client_address=client_address)
                except Exception as e:
                    self.transfer_progress.emit(f"Error: {str(e)}")
                    print(f"Error: {str(e)}")

            server_socket.close()
            self.transfer_progress.emit("Server stopped.")
        except Exception as e:
            self.transfer_progress.emit(f"Server error: {str(e)}")

        finally:
            if self.server_socket:
                self.server_socket.close()
            self.transfer_progress.emit("Server stopped.")

    def handle_client(self, client_socket, client_address):
        file_name = client_socket.recv(100).decode()
        file_size = client_socket.recv(100).decode()
        # if file_info == 'PING':
        #     print(f"Ping received from {client_address}, no action taken.")
        #     client_socket.close()
        #     return
        try:
            # file_name, file_size = file_info.split('|')
            with open(file_name, 'w', encoding='utf-8') as f:
                total_received = 0

                while total_received < file_size:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    self.transfer_progress.emit(f"Received from {client_address}: {data}")
                    f.write(data)
                    total_received += len(data)
                    print(f"Received data from{client_address}: {data}")
                    f.close()
                    client_socket.close()
        except Exception as e:
            self.transfer_progress.emit(f"Error handling client {client_address}: {str(e)}")
            print(f"Error handling client {client_address}: {str(e)}")
        finally:
            client_socket.close()
            self.transfer_progress.emit(f"Connection with {client_address} closed.")
            print(f"Connection with {client_address} closed.")
