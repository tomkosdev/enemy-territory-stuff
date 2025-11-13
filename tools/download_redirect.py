import socket
import os

file_url = "<URL>"
file_path = "rotation.txt"
download_folder = "downloads/"

GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
MAP_NAME_WIDTH = 40  # Fixed width for map name

def check_and_download_file(host, path, filename):
    try:
        conn = socket.create_connection((host, 80), timeout=5)
        request = f"HEAD /etmain/{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        conn.sendall(request.encode())
        response = conn.recv(1024).decode()
        conn.close()

        filename_display = filename.ljust(MAP_NAME_WIDTH)

        if "200 OK" in response:
            conn = socket.create_connection((host, 80), timeout=5)
            request = f"GET /etmain/{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            conn.sendall(request.encode())
            response = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                response += chunk
            conn.close()

            file_content = response.split(b"\r\n\r\n", 1)[1]
            os.makedirs(download_folder, exist_ok=True)

            with open(download_folder + filename, "wb") as file:
                file.write(file_content)

            print(f"{GREEN}{filename_display} downloaded successfully.{RESET}")
        else:
            print(f"{RED}{filename_display} is not available.{RESET}")

    except Exception as e:
        filename_display = filename.ljust(MAP_NAME_WIDTH)
        print(f"{RED}{filename_display} is not available. Error: {e}{RESET}")

def read_files_names(path):
    with open(path, "r") as file:
        for line in file:
            trimmed_line = line.strip()
            if trimmed_line:
                yield trimmed_line

for filename in read_files_names(file_path):
    check_and_download_file(file_url, filename, filename)
