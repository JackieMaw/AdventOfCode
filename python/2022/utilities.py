import requests
from os.path import exists

SESSIONID = "53616c7465645f5f8560ccb8622b41b149bda67a0fdaa8b9ca7c4f1c96049aa1f53ab73883b3eacc8ae8d91467a4e1cc8fbcfdb0fcb52921b5797863118fe880"
USER_AGENT = ""

def get_or_download_input(year, day):
    filename = f"input\Input_{year}_{day}.txt"
    if not(exists(filename)):
        download_input(year, day, filename)    
    with open(filename, "r") as text_file:
        return text_file.read().splitlines()

def get_input(year, day, postfix):
    filename = f"input\Input_{year}_{day}{postfix}.txt"
    print(f"Reading input from file: {filename}")
    with open(filename, "r") as text_file:
        return text_file.read().splitlines()

def download_input(year, day, filename):
    uri = f'http://adventofcode.com/{year}/day/{day}/input'
    print(f"Reading input from uri: {uri}")
    response = requests.get(uri, cookies={'session': SESSIONID}, headers={'User-Agent': USER_AGENT})
    print(f"Writing input to file: {filename}")
    with open(filename, "w") as text_file:
        text_file.write(response.text)

def get_strings(raw_input):
    return [l for l in raw_input]

def get_strings_csv(raw_input):
    result = []
    for line in raw_input:
        inner_result = []
        for l in line.split(","):   
            inner_result.append(l)
        result.append(inner_result)
    return result

def get_integers(raw_input):
    return [int(l) for l in raw_input]

def get_integers_csv(raw_input):
    return [int(l) for l in raw_input[0].split(",")]
