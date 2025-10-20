# FaustCTF 2024 Scoring Formula

<div class=page-badges>
<a href="https://github.com/attacking-lab/scoring-playground" class=badge-dataset></a>
</div>

Scoring formula for [FaustCTF 2024](https://2024.faustctf.net/) organized by
[FAUST](https://faust.cs.fau.de/).
<div style="margin-bottom:-1em"></div>

## Summary

The total score of each team is calculated from `offense`, `defense`, and `sla`
components of every team for each of their services and rounds played.

The checker returns one of three results for each service:
`up`, `recovering`, and `down`. The result is `up` if all SLA checks pass, and
`down` if some SLA checks do not pass. A service is considered
`recovering` if flags for one round in the *retention period* could not be
recovered, but the latest round passed SLA checks.

The following Python pseudo-code captures the [team score calculation](https://github.com/fausecteam/ctf-gameserver/blob/7d031ba/src/ctf_gameserver/controller/scoring.py):

``` python3
type CheckerResult = Literal["up"] | Literal["recovering"] | Literal["down"]

@dataclass
class RoundStateFlagstore:
	lost: str | None # flag of the current round if stolen by any team
    captures: list[str] # flags of this flagstore captured from other teams

@dataclass
class RoundStateService:
    flagstores: list[RoundStateFlagstore]
    checker_result: CheckerResult
    team_results: list[CheckerResult]

@dataclass
class RoundState:
    services: list[RoundStateService]

def score(rounds: list[RoundState], owner: dict[str, str],
          captures: dict[str, int]):
    attack = defense = sla = 0
    for rnd in range(len(rounds)):
        for service in rnd.services:
            for flagstore in service.flagstores:
                for flag in flagstore.captures:
                    if owner[flag] != "NOP":
                        attack += 1 + 1 / captures[flag]

                if (flag := flagstore.lost) is not None:
                    defense -= captures[flag] ** 0.75

            if service.checker_result == "up":
                teams_up = rnd.team_results.count("up")
                teams_rec = rnd.team_results.count("recovering")
                sla += (len(teams_up) + 0.5 * len(teams_rec)) \
                    * len(rnd.team_results) ** 0.5
    return (attack, defense, sla)
```

## Review

- Scoring is easy to understand and reason about
- Since `total_captures_of(flag)` is independent of round time, it may change
  after a previous attack score has been calculated, meaning efficient
  recalculation of team score each round is somewhat non-trivial.
  Additionally, score recalculation may cause total attack points to
  decrease from one round to the next, which tends to confuse new players.
- In the worst-case, when all teams capture flags of a service, the defense
  points `(N_Teams - 1)^0.75` lost outweigh the SLA points
  `(N_Teams)^0.5` gained for that service, thus violating
  [Tenet 4](../tenets/#perfect_sla_must_be_worth_more_than_any_attackers_relative_gain)


## Tenets

1. {{ tenet1_faust2024 }}
2. {{ tenet2_faust2024 }}
3. {{ tenet3_faust2024 }}
4. {{ tenet4_faust2024 }}
5. {{ tenet5_faust2024 }}
6. {{ tenet6_faust2024 }}
7. {{ tenet7_faust2024 }}

