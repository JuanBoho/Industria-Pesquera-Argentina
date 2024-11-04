import json


def read_json(file_path='data/ref_data.json') -> dict:
    """Reads json data file as dict"""

    with open(file_path, 'r') as f:
        data = json.load(f)
    
    return data


DATA = read_json('data/ref_data.json')

def get_data(key='') -> dict:
    return DATA.get(key, {})




if __name__ == "__main__":
    pass