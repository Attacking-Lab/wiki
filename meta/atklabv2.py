from math import log
from sys import argv
import json

def jeopardy(solves: int, teams: int,
             max_score: float = 10, min_score: float = 0.5,
             fp_ratio: float = 0.20, fp_weight: float = 0.5):
    score_ratio = min_score / max_score
    solve_ratio = (max(1, solves) - 1) / (teams - 1 / fp_ratio)
    rate = log(log(fp_weight, score_ratio), fp_ratio)
    return max_score * (score_ratio ** (solve_ratio ** rate))

def attack(victims: int, attackers: int, teams: int):
    return jeopardy(attackers, teams)

def defense(victims: int, attackers: int, teams: int):
    return jeopardy(teams - victims, teams) * teams / attackers

def sla(flagstores: int):
    return flagstores * 10

teams = 40
attackers = 5
flagstores = 3

data = []
if argv[1] == "jeopardy":
    for i in range(1, teams + 1):
        data.append({"solves": i, "points": jeopardy(i, teams)})
    print(json.dumps(data))
elif argv[1] == "single":
    for i in range(1, teams):
        data.append({"victims": i, "points": attack(i, attackers, teams) + defense(i, attackers, teams), "category": "attack"})
        data.append({"victims": i, "points": defense(i, attackers, teams), "category": "defense"})
    print(json.dumps(data))
elif argv[1] == "all":
    for i in range(1, teams):
        data.append({"victims": i, "points": attack(i, attackers, teams) + defense(i, attackers, teams), "category": "attack"})
        data.append({"victims": i, "points": defense(i, attackers, teams) * attackers, "category": "defense"})
        data.append({"victims": i, "points": sla(flagstores), "category": "sla"})
    print(json.dumps(data))
else:
    print(attack(1, attackers, teams))
    print(jeopardy(38, 40)*38)
