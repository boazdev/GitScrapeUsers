import os
from pathlib import Path
import sys
import json

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

def read_json(file_path):
    #base_dir = Path(__file__).resolve().parent.parent

    file_path = os.path.join(sys.path[0],file_path)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except:
        try:
            print("linux folders")
            #file_path = os.path.join("code",file_path)
            #file_path = os.path.join(sys.path[0],file_path)
            file_path = '/code/app/data/heb_names.json'
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f'file exception: {e}')
            return None
    
def write_json(file_path, key, value):
    file_path = os.path.join(sys.path[0],file_path)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data[key] = value

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def write_json_data(file_path, input_data):
    file_path = os.path.join(sys.path[0],file_path)
    """ try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {} """
    
    
    with open(file_path, 'w') as file:
        json.dump(input_data, file, indent=4)