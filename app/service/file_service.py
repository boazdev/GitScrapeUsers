import os
import sys

def extract_names_from_file(file_path):
    names_list = []
    file_path = os.path.join(sys.path[0],file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Split each row by commas
                parts = line.strip().split(',')
                # Extract names after the first comma (if any)
                if len(parts) > 1:
                    names = parts[1:]
                    names_list.extend(names)

    except FileNotFoundError:
        print(f"File not found: {file_path} currnet path:")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return names_list