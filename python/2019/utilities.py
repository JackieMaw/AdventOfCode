import requests

SESSIONID = "53616c7465645f5f3d5d09564a9bb8b931491c70f588a3870571f6355a33b53d67ce7b2f6aec80f9886d54e419789dfe"
USER_AGENT = ""

def download_input(year, day):
    uri = f'http://adventofcode.com/{year}/day/{day}/input'
    response = requests.get(uri, cookies={'session': SESSIONID}, headers={'User-Agent': USER_AGENT})
    #TODO - fix hard-coded path
    filename = f"2019\input\Input_{year}_{day}.txt"
    with open(filename, "w") as text_file:
        text_file.write(response.text)
    print(f"input downloaded: {filename}")

def get_strings(year, day):
    filename = f"2019\input\Input_{year}_{day}.txt"
    with open(filename, "r") as text_file:
        return [l.strip() for l in text_file.readlines()]

def get_integers(year, day):
    filename = f"2019\input\Input_{year}_{day}.txt"
    with open(filename, "r") as text_file:
        return [int(l.strip()) for l in text_file.readlines()]

def get_integers_csv(year, day):
    filename = f"2019\input\Input_{year}_{day}.txt"
    with open(filename, "r") as text_file:
        return [int(l.strip()) for l in text_file.read().split(",")]