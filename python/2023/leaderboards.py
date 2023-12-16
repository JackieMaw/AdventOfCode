import json
import requests

class MemberSummary():

    def __init__(self, member_info):
        self.name = member_info["name"]
        self.id = member_info["id"]
        self.stars = member_info["stars"]
        self.local_score = member_info["local_score"]
        self.last_star_ts = member_info["last_star_ts"]

class LeaderboardSummary():

    def __init__(self, leaderboard_name, member_summaries):
        self.leaderboard_name = leaderboard_name
        self.member_summaries = member_summaries

    def get_total_stars(self):
        return sum(member_summary.stars for member_summary in self.member_summaries)
    
    def get_count_members(self):
        return len(self.member_summaries)
    
    def get_count_active_members(self):
        return sum(1 for member_summary in self.member_summaries if member_summary.stars > 0)
    
    def get_count_members_achieved_goal(self, goal):
        return sum(1 for member_summary in self.member_summaries if member_summary.stars > goal)
    
    def print_summary(self, goal):
        print(f"{self.leaderboard_name} leaderboard has {self.get_count_active_members()}/{self.get_count_members()} active members achieving {self.get_total_stars()} stars, with {self.get_count_members_achieved_goal(goal)} participants achieving at least {goal} stars")
        print("TOP 10")
        self.member_summaries.sort(reverse=True, key=sort_by_local_score)
        for member_summary in self.member_summaries[:20]:
            print(f'    {member_summary.name} {member_summary.stars} {member_summary.local_score}')

def get_session_id():
    with open("session_id_ubs_admin.txt", "r") as text_file:
        return text_file.read()

def get_leaderboard_json(year, leaderboard_code):
    uri = f'https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_code}.json'
    print(f"Reading input from uri: {uri}")
    response = requests.get(uri, cookies={'session': get_session_id()})
    print(response.text)
    return response.text

def get_leaderboard_summary(leaderboard_name, leaderboard_json) -> int:
    data = json.loads(leaderboard_json)
    members = data.get("members")
    member_summaries = [MemberSummary(members[key]) for key in members.keys() if members[key]["name"] not in IGNORED_MEMBERS]
    return LeaderboardSummary(leaderboard_name, member_summaries)

def extract_leaderboard_summary(leaderboard_name, code):
    leaderboard_json = get_leaderboard_json(YEAR, code)
    return get_leaderboard_summary(leaderboard_name, leaderboard_json)

def sort_by_local_score(member_summary : MemberSummary):
    return member_summary.local_score

def sort_by_total_stars(leaderboard_summary):
    return leaderboard_summary.get_total_stars()

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


def get_sum(leaderboard_summaries):
    (sum_leaderboard, sum_total_members, sum_total_active_members, sum_total_stars, sum_count_goal) = ("ALL", 0, 0, 0, 0)
    for leaderboard_summary in leaderboard_summaries:
        sum_total_members += leaderboard_summary.get_count_members()
        sum_total_active_members += leaderboard_summary.get_total_active_members()
        sum_total_stars += leaderboard_summary.get_total_stars()
        sum_count_goal += leaderboard_summary.get_count_goal()
    return (sum_leaderboard, sum_total_members, sum_total_active_members, sum_total_stars, sum_count_goal)
    

# process leaderboards

YEAR = 2023
all_leaderboards = { "APAC":"1580364", "Switzerland":"212737", "EMEA":"825756", "AMER":"2328970", "GLOBAL_TOP_100":"2087277" }
goal=28
IGNORED_MEMBERS = {"UBS Admin"}

leaderboard_summaries = [extract_leaderboard_summary(leaderboard, code) for (leaderboard, code) in all_leaderboards.items()]
leaderboard_summaries.sort(reverse=True, key=sort_by_total_stars)

#leaderboard_summaries.append(get_sum(leaderboard_summaries))

for leaderboard_summary in leaderboard_summaries:
    leaderboard_summary.print_summary(goal)