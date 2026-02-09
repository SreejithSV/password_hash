import json
from services.hash_service import md5_hash

def generate_rainbow(passwords):
    table = {}

    for pwd in passwords:
        table[md5_hash(pwd)] = pwd

    with open("data/rainbow_table.json", "w") as f:
        json.dump(table, f)

    return len(table)

def lookup(hash_value):
    with open("data/rainbow_table.json") as f:
        table = json.load(f)

    return table.get(hash_value)
