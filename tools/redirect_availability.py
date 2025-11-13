#!/usr/bin/env python3

import urllib.request
import urllib.error
import sys
import os

file_url = "http://<URL>/etmain/"

if len(sys.argv) != 2:
    print("Usage: python script.py <rotation_file>")
    sys.exit(1)

file_path = sys.argv[1]

file_path = os.path.abspath(file_path)

def check_file_availability(url):
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return True
            else:
                return False
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        else:
            print(f"HTTP error occurred: {e.code} {e.reason}")
            return False
    except urllib.error.URLError as e:
        print(f"Failed to reach server: {e.reason}")
        return False

def read_files_names(path):
    with open(path, "r") as file:
        for line in file:
            yield line.strip()

available_maps = []
unavailable_maps = []

for line in read_files_names(file_path):
    new_path = file_url + line
    is_available = check_file_availability(new_path)
    if is_available:
        available_maps.append(line)
    else:
        unavailable_maps.append(line)

for element in unavailable_maps:
    print(f"\033[31m{element:<40} is not available.\033[0m")

for element in available_maps:
    print(f"\033[32m{element:<40} downloaded successfully.\033[0m")

print("")
print("\033[31mUnavailable maps: \033[0m" + str(len(unavailable_maps)))
print("\033[32mAvailable maps: \033[0m" + str(len(available_maps)))

