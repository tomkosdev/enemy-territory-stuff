#!/usr/bin/env python3

import re
import sys
import os

def extract_maps_from_file(input_file):
    with open(input_file, 'r') as file:
        content = file.read()

    lines = content.split()
    filtered = [line for line in lines if line.startswith("etmain/")]

    extracted = [line.split('/', 1)[1] for line in filtered]

    excluded_patterns = ["pak0", "pak1", "pak2", "zzz", "mp_bin"]
    cleaned = [
        line for line in extracted
        if not any(re.search(pattern, line) for pattern in excluded_patterns)
    ]

    unique_sorted = sorted(set(line.strip() for line in cleaned))
    return [line + ".pk3" for line in unique_sorted]

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage:")
        print("  python script.py <input_file> [output_file]")
        sys.exit(1)

    input_file = os.path.abspath(sys.argv[1])

    if not os.path.isfile(input_file):
        print(f"Error: File not found: '{input_file}'")
        sys.exit(1)

    maps = extract_maps_from_file(input_file)

    GREEN = '\033[92m'
    RESET = '\033[0m'

    if len(sys.argv) == 3:
        output_file = os.path.abspath(sys.argv[2])
        with open(output_file, 'w') as f:
            f.write("\n".join(maps))
        print(f"{GREEN}Processed '{input_file}' and saved list of maps to '{output_file}'.{RESET}")
    else:
        print(f"{GREEN}List of maps from '{input_file}':{RESET}")
        print("\n".join(maps))

if __name__ == "__main__":
    main()
