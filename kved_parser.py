import json
from pprint import pprint

def read_file(path: str) -> dict:
    with open('kved.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
