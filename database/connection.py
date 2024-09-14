import pyodbc

DATABASE_PATH = r'E:/Workspaces/transfer_file_server/database/FILE_TRANSFERS.accdb'
CONNECTION_STRING = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' 
                     r'DBQ=' + DATABASE_PATH + ';')

class ConnectionAccess():
    def __init__(self):
        pass

    def get_connection(self):
        conn = None
        try:
            conn = pyodbc.connect(CONNECTION_STRING)
            print(f"Connection success !")
            return conn.cursor()
        except pyodbc.Error as e:
            print(f"Error: {e}")
        return None
    
    def close_connection(self, conn):
        if conn:
            conn.close()
            print("Connection closed!")


if __name__ == '__main__':
    # connnection_interface = ConnectionAccess()
    # con = connnection_interface.get_connection()
    print(pyodbc.drivers())