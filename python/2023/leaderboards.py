import json
import requests

SESSIONID = "GET_FROM_SESSION_COOKIE"

def get_leaderboard_json(year, leaderboard_code):
    uri = f'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_code}.json'
    print(f"Reading input from uri: {uri}")
    response = requests.get(uri, cookies={'session': SESSIONID})
    print(response.text)
    return response.text

def get_stars_count(leaderboard_json, goal) -> int:
    total_members = 0
    total_active_members = 0
    total_stars = 0
    count_goal = 0
    data = json.loads(leaderboard_json)
    members = data.get("members")
    try:
        for key in members.keys():
            total_members += 1
            num_stars = members[key]["stars"]
            if num_stars >= goal:
                count_goal += 1
            if num_stars >= 1:
                total_active_members += 1
            total_stars += min(goal, num_stars) 
    except Exception as exp:
        print("Exception {}".format(exp))
        return -1
    return (total_members, total_active_members, total_stars, count_goal)

def process_leaderboard(leaderboard, code):
    leaderboard_json = get_leaderboard_json(YEAR, code)
    (total_members, total_active_members, total_stars, count_goal) = get_stars_count(leaderboard_json, goal)
    return (leaderboard, total_members, total_active_members, total_stars, count_goal)

def sort_by_total_stars(stat):
    (_, _, _, total_stars, _) = stat
    return total_stars

def print_active_members(leaderboard_json):
    data = json.loads(leaderboard_json)
    members = data.get("members")
    for key in members.keys():
        num_stars = members[key]["stars"]
        if num_stars >= 1:
            print(f"{members[key]['name']}; ")

def print_active_members_for_leaderboard(code):
    leaderboard_json = get_leaderboard_json(YEAR, code)
    print_active_members(leaderboard_json)

# process leaderboards

YEAR = 2023
all_leaderboards = { "APAC":"1580364", "Switzerland":"212737", "EMEA":"825756", "AMER":"2328970" }
goal=50

stats = [process_leaderboard(leaderboard, code) for (leaderboard, code) in all_leaderboards.items()]
stats.sort(reverse=True, key=sort_by_total_stars)

for (leaderboard, total_members, total_active_members, total_stars, count_goal) in stats:
    print(f"{leaderboard} leaderboard has {total_active_members}/{total_members} active members achieving {total_stars} stars, with {count_goal} participants achieving at least {goal} stars")