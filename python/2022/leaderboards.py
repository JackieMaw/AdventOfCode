import json
import requests

SESSIONID = "53616c7465645f5f511ed419e8ad25692462aa7eb9415640eed6fd74e6329a6060f5de44b990cb75042374476541572f35dbf43c1052f29a6581973b7346dc73"
USER_AGENT = ""

def get_leaderboard_json(year, leaderboard_code):
    uri = f'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_code}.json'
    #print(f"Reading input from uri: {uri}")
    response = requests.get(uri, cookies={'session': SESSIONID}, headers={'User-Agent': USER_AGENT})
    return response.text

def get_stars_count(leaderboard_json, goal) -> int:
    total_active_members = 0
    total_stars = 0
    count_goal = 0
    data = json.loads(leaderboard_json)
    members = data.get("members")
    try:
        for key in members.keys():
            num_stars = members[key]["stars"]
            if num_stars >= goal:
                count_goal += 1
            if num_stars >= 1:
                total_active_members += 1
            total_stars += min(goal, num_stars) 
    except Exception as exp:
        print("Exception {}".format(exp))
        return -1
    return (total_active_members, total_stars, count_goal)

def process_leaderboard(leaderboard, code):
    leaderboard_json = get_leaderboard_json(YEAR, code)
    (total_active_members, total_stars, count_goal) = get_stars_count(leaderboard_json, goal)
    return (leaderboard, total_active_members, total_stars, count_goal)

def sort_by_total_stars(stat):
    (_, _, total_stars, _) = stat
    return total_stars

# process leaderboards

YEAR = 2022
all_leaderboards = { "GLOBAL":"384496", "Singapore":"1580364", "India":"639163", "Poland":"392146", "Switzerland":"212737", "UK":"825756", "US":"984566" }
goal=26

stats = [process_leaderboard(leaderboard, code) for (leaderboard, code) in all_leaderboards.items()]
stats.sort(reverse=True, key=sort_by_total_stars)

for (leaderboard, total_active_members, total_stars, count_goal) in stats:
    print(f"{leaderboard} leaderboard has {total_active_members} active members achieving {total_stars} stars, with {count_goal} participants achieving at least {goal} stars")