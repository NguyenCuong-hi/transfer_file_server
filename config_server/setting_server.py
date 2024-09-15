import json
import os


def reading_file_setting(file_setting):
    try:
        with open(file_setting, 'r') as f:
            settings = json.load(f)

        name = settings.get("name", "")
        ip = settings.get("ip", "")
        port = settings.get("port", "")

        database = settings.get("database", {})
        host_db = database.get("host", "")
        username_db = database.get("username", "")
        password_db = database.get("password", "")
        port_db = database.get("port", "")
        schema = database.get("schema", "")

        return name, ip, port, host_db, username_db, password_db, port_db, schema

    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_setting}")
        return False
    except json.JSONDecodeError:
        print("Lỗi khi đọc file JSON")
        return False


def write_file_setting(file_setting):
    settings = {
        "name": "Server",
        "ip": "172.0.0.1",
        "port": 80,
        "database": {
            "host": "172.0.0.1",
            "port": 3306,
            "username": "admin",
            "password": "admin",
            "schema": "test"
        }
    }

    name = settings['name']
    ip = settings['ip']
    port = settings['port']

    host_db = settings['database']['host']
    username_db = settings['database']['username']
    password_db = settings['database']['password']
    port_db = settings['database']['port']
    schema = settings['database']['schema']

    try:
        with open(file_setting, 'w') as f:
            json.dump(settings, f, indent=4)
        print(f"Đã ghi file thành công vào {file_setting}")
    except IOError:
        print("Lỗi khi ghi file")

    return name, ip, port, host_db, username_db, password_db, port_db, schema


def is_exist_file(file_path):
    return os.path.isfile(file_path)


def checking_init_file_setting(file_path):
    if is_exist_file(file_path=file_path):
        return reading_file_setting(file_setting=file_path)
    else:
        return write_file_setting(file_path)


def update_file_setting(file_setting, data):
    try:
        with open(file_setting, 'r') as f:
            settings = json.load(f)

        settings.update(data)
        with open(file_setting, 'w') as f:
            json.dump(settings, f, indent=4)

        print(f"Đã cập nhật thành công file: {file_setting}")

    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_setting}")
    except json.JSONDecodeError:
        print("Lỗi khi đọc hoặc ghi file JSON")
