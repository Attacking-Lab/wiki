# ATKLAB v1 Scoring Formula

<div class=page-badges>
<a href="https://github.com/attacking-lab/scoring-playground" class=badge-formula></a>
</div>

Scoring formula designed by <span class=hltext>Attacking-Lab</span> with an emphasis for simplicity.
<div style="margin-bottom:-1em"></div>

## Summary

Each team's score is calculated from `offense`, `defense` and `sla`
components of each of their services in all rounds played.

The checker returns one of three results for each service:
`OK`, `RECOVERING` and `DOWN`:

- A service is considered `OK` if all flags could be successfully deployed and
retrieved, and all other checks were successful.
- A service is considered `DOWN` if any checks for the current round failed.
- A service is considered `RECOVERING` if not all flags which are still
*valid*, that is they can be submitted for points in the current round, could
be retrieved by the checker. In this case SLA points are awarded relative to
the ratio of flags which could be recovered (`sla_ratio`), as proposed in
[Tenet 7](../tenets/#sla_should_decrease_fairly_with_every_missing_flag_in_the_retention_period).

The following python pseudo-code captures the
[team score calculation](https://github.com/Attacking-Lab/scoring-playground/tree/main/src/scoring_playground/scoring/atklabv1.py):

``` python3
@dataclass
class CTFInfo:
	team_count: int # includes NOP team
	retention_rounds: int

@dataclass
class RoundStateFlagstore:
	lost: str | None # flag of the current round if stolen by any team
    active: list[str] # flags of this flagstore deployed in the retention period
    captures: list[str] # flags of this flagstore captured from other teams

@dataclass
class RoundStateService:
    flagstores: list[RoundStateFlagstore]
    checker_result: Literal["up"] | Literal["recovering"] | Literal["down"]

    @property
    def max_sla(self) -> int:
        return 2 * len(self.flagstores) + 1

@dataclass
class RoundState:
    services: list[RoundStateService]

def score(rounds: list[RoundState], ctf: CTFInfo, captures: dict[str, int]):
    attack = defense = sla = 0
    for rnd in rounds:
        for service in rnd.services:
            if service.checker_result == "up":
                sla += 1
            for flagstore in service.flagstores:
                sla_ratio = len(flagstore.active) / ctf.retention_rounds
                if service.checker_result != "down":
                    sla += 2 * sla_ratio

                if (flag := flagstore.lost) is not None:
                    defense -= (1 + captures[flag] / ctf.team_count) / 2

                for flag in flagstore.captures:
                    attack += (1 + 1 / captures[flag]) / 2
    return (attack, defense, sla)
```

## Review

- Any round that a service is unavailable, the corresponding team loses
  SLA equal to `sla_max` for that round. Additionally, since some flags
  could not be deployed, the team will receive partial SLA for subsequent
  rounds in the retention period, at most
  `(retention_rounds - 1) / retention_rounds * sla_max`. Therefore,
  the total cost of a service becoming unavailable for `n` rounds is
  at least `sla_max` and at most
  `n * sla_max + (retention_rounds - 1) / retention_rounds * 2 =~ n * sla_max + 2`,
  both of which are greater than the maximum relative gain of an attacker
  (`len(flagstores) * 2`).
- To incentivize defense and reduce the relative cost of patching, defense
  points start at `-0.5` for a single attacker and scale linearly to `-1` with
  the number of captures thereafter.
- When a service becomes unavaiable due to patching,
  the lost points can only be recovered relative to the unpatched state if the
  service will be unsuccessfully attacked for (at worst with `len(flagstores) = 1`)
  `(n * sla_max + 2) / (len(flagstores) / 2) - n = 5 * n + 4` rounds *more* than the
  patching made the service unavaiable for.
  Patching should reasonably result in at most a few rounds of downtime (e.g. `2`),
  the lost points can be recovered in only a few rounds of subsequent uptime (`6 * 2 + 4 = 16`). Additionally, the *checker hold* makes it feasible for
  *valid* patches to be deployed with zero downtime deterministically.
- Captured flags' value scales with the number of captures, therefore this
  formula suffers from the same quirk as [FaustCTF 2024](../faust2024) and similar,
  which is that the attack score may decrease over time, confusing players.
  To mitigate this, the scoreboard displays both the *expected* and *realized*
  attack points.

## Tenets

1. {{ tenet1_atklabv1 }}
2. {{ tenet2_atklabv1 }}
3. {{ tenet3_atklabv1 }}
4. {{ tenet4_atklabv1 }}
5. {{ tenet5_atklabv1 }}
6. {{ tenet6_atklabv1 }}
7. {{ tenet7_atklabv1 }}


