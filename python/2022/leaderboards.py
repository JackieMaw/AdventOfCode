import json
import requests

SESSIONID = "53616c7465645f5f511ed419e8ad25692462aa7eb9415640eed6fd74e6329a6060f5de44b990cb75042374476541572f35dbf43c1052f29a6581973b7346dc73"
USER_AGENT = ""

def download_leaderboard(year, leaderboard_code):
    uri = f'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_code}.json'
    #print(f"Reading input from uri: {uri}")
    response = requests.get(uri, cookies={'session': SESSIONID}, headers={'User-Agent': USER_AGENT})
    filename = f"leaderboards\{year}_{leaderboard_code}.txt"
    #print(f"Writing input to file: {filename}")
    with open(filename, "w", encoding='utf-8') as text_file:
        text_file.write(response.text)
    return filename

def get_stars_count(json_file_name: str) -> int:
    """
    Sum all the stars in a leaderboard json
    Arguments:
        json_file_name: json file absolute path string
    
    Returns:
        Sum of all the stars gathered by the members of the leaderboard.
    """
    result = 0
    with open(json_file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        members = data.get("members")
        try:
            for key in members.keys():
                result += members[key]["stars"]
        except Exception as exp:
            print("Exception {}".format(exp))
            return -1
    return result

# process leaderboards

YEAR = 2022
all_leaderboards = { "GLOBAL":"384496", "Singpore":"1580364", "India":"639163", "Poland":"392146", "Switzerland":"212737", "UK":"825756", "US":"984566" }
 
for (leaderboard, code) in all_leaderboards.items():
    filename = download_leaderboard(YEAR, code)
    result = get_stars_count(filename)
    print(f"{leaderboard} leaderboard has {result} stars")