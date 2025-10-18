# SaarCTF 2024 Scoring Formula

<div class=page-badges>
<a href="https://github.com/attacking-lab/scoring-playground" class=badge-dataset></a>
</div>

Scoring formula for [SaarCTF 2024](https://ctf.saarland/) organized by
[saarsec](https://saarsec.rocks/).
<div style="margin-bottom:-1em"></div>

## Summary

The total score of each team is calculated from `offense`, `defense` and `sla`
components of every team for each of their services and rounds played.

The checker returns one of three results for each service:
`up` and `down`. The result is `up` if all SLA checks pass, and
`down` if some SLA checks do not pass.

Additionally, the game server tracks the status of the vulnbox' VPN
connection as, assigning either `online` or `offline` status accordingly.

The following python pseudo-code captures the [team score calculation](https://github.com/MarkusBauer/saarctf-gameserver/blob/2ae48d1/controlserver/scoring/algorithm.py#L54):

``` python3
type CheckerResult = Literal["up"] | Literal["down"]
type VpnStatus = Literal["online"] | Literal["offline"]

@dataclass
class RoundStateFlagstore:
	lost: str | None # flag of the current round if stolen by any team
    captures: list[str] # flags of this flagstore captured from other teams

@dataclass
class RoundStateService:
    flagstores: list[RoundStateFlagstore]
    checker_result: CheckerResult
    team_results: list[CheckerResult]
    team_vpn: list[VpnStatus]
    scoreboard: dict[str, int]

@dataclass
class RoundState:
    services: list[RoundStateService]

def score(rounds: list[RoundState], owner: dict[str, str],
          captures: dict[str, int]):
    attack = defense = sla = 0
    for rnd in range(len(rounds)):
        for service in rnd.services:
            teams_online = searvice.team_vpn.count("online")
            for flagstore in service.flagstores:
                for flag in flagstore.captures:
                    attack += 1 + captures[flag] ** -0.5 \
                        + rnd.scoreboard[owner[flag]] ** -0.5

                if (flag := flagstore.lost) is not None:
                    defense -= (captures[flag] / teams_online) ** 0.3 \
                        * teams_online ** 0.5

            if service.checker_result == "up":
                sla += teams_online ** 0.5
    flags_per_round = sum(len(s.flagstores) for s in rounds[0].services)
    return (attack / flags_per_round, defense / flags_per_round, sla)
```

The final worth of a flag is only calculated once its validity is over.
That means, everyone that submits a flag while it is still valid receives
the same amount of points.


## Review

- Only small differences to the [FaustCTF 2024](faust2024) scoring formula,
  inherits most of the same strengths (simple, easy to implement) and
  weaknesses (score recalculation).
- SLA is scaled using the number of *online* teams, which allows manipulation
  by registering fake teams ahead of time and connecting / disconnecting
  from the VPN depending on your own service status.
- Attack and defense points are scaled by the number of flagstores, but SLA
  is not scaled by the number of services. For consistent scoring, SLA
  should be normalized such that SLA weight does not depend on the number
  services deployed.
- Defense points scale with SLA, such that perfect SLA will always be worth
  atleast as much as the defense points lost. However, since the *attacker*
  still gains points when in the worst-case `sla + defense == 0`, this formula
  violates [Tenet 4](../tenets/#perfect_sla_must_be_worth_more_than_any_attackers_relative_gain).


## Tenets

1. {{ tenet1_saar2024 }}
2. {{ tenet2_saar2024 }}
3. {{ tenet3_saar2024 }}
4. {{ tenet4_saar2024 }}
5. {{ tenet5_saar2024 }}
6. {{ tenet6_saar2024 }}
7. {{ tenet7_saar2024 }}
