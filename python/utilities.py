import requests
from os.path import exists

SESSIONID = "53616c7465645f5f3d5d09564a9bb8b931491c70f588a3870571f6355a33b53d67ce7b2f6aec80f9886d54e419789dfe"
USER_AGENT = ""

def get_or_download_input(year, day):
    filename = f"input\Input_{year}_{day}.txt"
    if not(exists(filename)):
        download_input(year, day, filename)    
    with open(filename, "r") as text_file:
        return text_file.read().splitlines()

def get_input(year, day, postfix):
    filename = f"input\Input_{year}_{day}{postfix}.txt"
    with open(filename, "r") as text_file:
        return text_file.read().splitlines()

def download_input(year, day, filename):
    uri = f'http://adventofcode.com/{year}/day/{day}/input'
    response = requests.get(uri, cookies={'session': SESSIONID}, headers={'User-Agent': USER_AGENT})
    with open(filename, "w") as text_file:
        text_file.write(response.text)
    print(f"input downloaded: {filename}")

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