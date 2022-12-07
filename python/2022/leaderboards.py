import json
import requests

SESSIONID = "53616c7465645f5f8560ccb8622b41b149bda67a0fdaa8b9ca7c4f1c96049aa1f53ab73883b3eacc8ae8d91467a4e1cc8fbcfdb0fcb52921b5797863118fe880"
USER_AGENT = ""

def download_leaderboard(year, leaderboard_code):
    uri = f'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_code}.json'
    print(f"Reading input from uri: {uri}")
    response = requests.get(uri, cookies={'session': SESSIONID}, headers={'User-Agent': USER_AGENT})
    filename = f"leaderboards\{year}_{leaderboard_code}.txt"
    print(f"Writing input to file: {filename}")
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
all_leaderboards = { "GLOBAL":"384496", "Singpore":"", "India":"", "Poland":"", "Switzerland":"", "UK":"", "US":"" }
 
for (leaderboard, code) in all_leaderboards.items():
    filename = download_leaderboard(YEAR, code)
result = get_stars_count(filename)
print(f"{leaderboard} leaderboard has {result} stars")