# ENOWARS 2024 Scoring Formula

<!--
<div class=page-badges>
<a href="https://github.com/attacking-lab/scoring-playground" class=badge-formula></a>
</div>
-->

Scoring formula for [Enowars 8](https://8.enowars.com)
organized by [ENOFLAG](https://enoflag.de).
<div style="margin-bottom:-1em"></div>

## Summary

The total score of each team is calculated from offense, defense, and SLA components of every team for each of their services and rounds played.

The checker returns one of three results for each service:
`up`, `recovering`, and `down`. The result is `up` if all SLA checks pass, and
`down` if some SLA checks do not pass. A service is considered
`recovering` if flags for one round in the *retention period* could not be
recovered, but the latest round passed SLA checks.

The following Python pseudo-code captures the [team score calculation](https://github.com/enowars/EnoEngine/blob/66310c0/EnoDatabase/EnoDb.Scoring.cs):[^1]


``` python3
SLA = 100.0
ATTACK = 1000.0
DEF = -50.0

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
                    attack += ATTACK / captures[flag] \
                        / len(service.flagstores) / len(rnd.services)

                if (flag := flagstore.lost) is not None:
                    defense -= DEF / len(service.flagstores) \
                        / len(rnd.services)

            if service.checker_result == "up":
                sla += SLA
            elif service.checker_result == "recovering":
                sla += 0.5 * SLA
    return (attack, defense, sla)
```

[^1]: We've removed the per-service weights applied to attack, defense, and SLA points from the formula since historically they were rarely changed and typically set to 1.

## Review

- Only small differences to [FaustCTF 2024](../faust2024/) and [SaarCTF 2024](../saar2024/),
  inherits most of the same strengths (simple, easy to implement) and
  weaknesses (score recalculation).
- Flag value is scaled by the number of flag stores of each service, not
  the total number of flagstores, thereby violating
  [Tenet 7](../tenets/#flag_value_should_be_calculated_independent_of_its_flagstore)


## Tenets

1. {{ tenet1_enowars2024 }}
2. {{ tenet2_enowars2024 }}
3. {{ tenet3_enowars2024 }}
4. {{ tenet4_enowars2024 }}
5. {{ tenet5_enowars2024 }}
6. {{ tenet6_enowars2024 }}
7. {{ tenet7_enowars2024 }}
