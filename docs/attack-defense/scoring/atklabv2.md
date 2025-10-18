# ATKLAB v2 Scoring Formula

<div class=page-badges>
<a href="https://github.com/attacking-lab/scoring-playground" class=badge-formula></a>
</div>

Scoring formula designed by <span class=hltext>Attacking-Lab</span> with an emphasis on fairness and defense.

Also a great lesson in [Second-system Syndrome](https://en.wikipedia.org/wiki/Second-system_effect) (/hj).
<div style="margin-bottom:-1em"></div>

## Summary

In Jeopardy CTFs, dynamic scoring is used to infer the difficulty
of a challenge based on the number of teams that can solve it. This scoring
formula applies the same concept to A/D.

In effect, each round is treated as a Jeopardy CTF with the following *challenges*:

- For each flag you capture, you receive **ATK points** based on the number
  of teams that capture that flag.
- For each service and each flag store, you receive **DEF points** for each
  actively exploiting team that did not capture your flag, proportional to the
  number of teams whose flags that team did capture.

Additionally, you gain a **fixed amount of SLA points** for each deployed flag
that is still *valid* (submittable for points) and retrievable from the service,
as long as the checker status is <span class=hl-success>`SUCCESS`</span>
or <span class=hl-recovering>`RECOVERING`</span>.

## Checker Status

The checker returns one of the following results for each service:

- <span class=hl-success>`SUCCESS`</span> if all flags could be successfully deployed and
retrieved, and functionality checks were successful.
- <span class=hl-recovering>`RECOVERING`</span> if all checks for the current round succeed,
  but flags from the past 4 rounds are missing.
- <span class=hl-mumble>`MUMBLE`</span> if any functionality checks for the current round failed.
- <span class=hl-offline>`OFFLINE`</span> if the checker failed to establish a connection to the service.
- <span class=hl-error>`INTERNAL_ERROR`</span> if an internal error occurred.

## Implementation

The implementation may be evaluated against
real CTF data using <a href="https://github.com/attacking-lab/scoring-playground">our simulator</a>.

### Dynamic Scoring

We deterime a flexible dynamic scoring formula, which allows the organizers
to set three fixed points `(1, max_score)`, `(fp_ratio * teams, fp_weight)`
and `(teams, min_score)`.

```python3
def jeopardy(solves: int, teams: int,
             max_score: float = 10, min_score: float = 0.5,
             fp_ratio: float = 0.20, fp_weight: float = 0.50):
    score_ratio = min_score / max_score
    solve_ratio = (max(1, solves) - 1) / (teams - 1 / fp_ratio)
    rate = log(log(fp_weight, score_ratio), fp_ratio)
    return max_score * (score_ratio ** (solve_ratio ** rate))
```

??? "Implementation Details"

    - `solves`: The number of teams which have solved this specific *challenge*.
    - `teams`: The number of participating teams.
    - `max_score`: The maximum score when the number of solves is one.
    - `min_score`: The minimum score when the number of solves is the number of teams.
    - `fp_ratio`: The ratio of teams for setting the third fixed point.
    - `fp_weight`: The fraction of the max score to award at the third fixed point.
    - `log(x, base)`: Takes the logarithm of `x` to base `base`.

When called with default parameters as `jeopardy(solves, 40)`, this results in the following:

```vegalite 
{
  "data": {
    "url": "/assets/data/atklabv2_jeopardy.json"
  },
  "padding": {
    "right": 30
  },
  "height": 300,
  "autosize": "fit",
  "mark": {
    "type": "line",
    "tooltip": true,
    "color": "#bb86fce0",
    "point": {
        "filled": true,
        "color": "#bb86fce0"
    }
},
  "encoding": {
    "x": {"field": "solves", "type": "nominal", "axis": {"labelAngle": 0}},
    "y": {"field": "points", "type": "quantitative"}
  },
  "background": "#1f1f1f"
}
```

### Attack Points

To determine **ATK points**, the gameserver updates the number of submissions
of all valid flags, based on the number of flags submitted each round,
and recalculates the value of each flag based on the number of teams who were
able to capture it.

```python3
def attack_flag(num_submissions: int, teams: int):
    return jeopardy(num_submissions, teams)
```

??? "Implementation Details"

    **Context**: This function is called per active <span class=hltext>attacker</span> and for every <span class=hltext>victim</span>, for each <span class=hltext>service</span> and <span class=hltext>flagstore</span> to calculate the value of the stolen <span class=hltext>flag</span>.

    - `num_submissions`: The number of submissions of <span class=hltext>flag</span>.
    - `teams`: The number of participating teams.

Additional ATK points are awarded to each attacking team based on the DEF points
that other teams earn from defending against their attacks. This prevents
scenarios where defenders gain more DEF points from an attack than the attacker -
in other words, failed exploit attempts do not negatively affect the attacker ranking.

```python3
def attack(live_round: int, flag_round: int,
           max_victims: int, num_victims: int, num_attackers: int):
    checker_status = defaultdict(lambda: "SUCCESS")
    flag_avail_in = defaultdict(lambda: defaultdict(lambda: True))
    pts = defense(live_round, flag_round, checker_status, flag_avail_in,
                  max_victims, num_victims, num_attackers, True)
    for flag in flags_stolen:
        pts += attack_flag(flag.num_submissions)
    return pts
```

??? "Implementation Details"

    **Context**: Each <span class=hltext>round</span>, this function is called per <span class=hltext>attack</span>, for the <span class=hltext>service</span> and <span class=hltext>flagstore</span> bein attacked by an <span class=hltext>attackers</span>, to calculate the value of the entire attack over all victims.

    - `flag.num_submissions`: The number of submissions for the <span class=hltext>flag</span> of the current victim.
    - `flags_stolen`: The flags stolen for this <span class=hltext>service</span> and <span class=hltext>flagstore</span> by the attacker that were deployed in `flag_round`.
    - `max_victims`: The number of teams who are not the attacker or NOP, that have atleast one service not in <span class=hl-offline>`OFFLINE`</span> state in the current round.
    - `num_victims`: The number of teams exploited by the attack which points are currently being calculated for.
    - `num_attackers`: The number of teams attacking this <span class=hltext>service</span> and <span class=hltext>flagstore</span>, and obtaining flags stored in <span class=hltext>flag_round</span>.

The scores of teams who have captured flags previously are updated to reflect
the decreased value of those flags by new submissions.

The NOP team does not gain attack points.

### Defense Points

To determine **DEF points**, the gameserver updates the amount of captures
of every flag which is still valid each round. For every team, the points
gained from defending against a specific attacker are calculated based on
the number of teams that were not exploited by them in that flag store
in that round. This is meant to reflect that some exploits are much more
difficult to defend against than others and reward teams that can construct
solid defenses.

These points are then scaled by the number of active teams (excluding the
attacking team and NOP), and divided by the number of attackers for that flag store.
Defense points are only awarded for *active* attackers, i.e., those teams
that submit at least one flag from that flag store and round. If no teams are
exploited, no teams receive DEF points.


```python3
def defense_raw(max_victims: int, num_victims: int,
                num_attackers: int, exploited: bool):
    if exploited or num_victims == 0:
        return 0
    pts = jeopardy(max_victims - num_victims, max_victims)
    return pts * max_victims / num_attackers
```

??? "Implementation Details"

    **Context**: Each <span class=hltext>round</span>, this function is called per <span class=hltext>service</span> and <span class=hltext>flag store</span>, for each active <span class=hltext>attacker</span> and for every <span class=hltext>team</span>, to update the value of teams defending / not defending the <span class=hltext>attack</span>.

    - `max_victims`: The number of teams who are not the attacker or NOP, that have atleast one service not in <span class=hl-offline>`OFFLINE`</span> state in the current round.
    - `num_victims`: The number of teams exploited by the attack which points are currently being calculated for.
    - `num_attackers`: The number of teams submitting flags from this <span class=hltext>service</span> and <span class=hltext>flag store</span> deployed in a specific <span class=hltext>round</span>.
    - `exploited`: Is this <span class=hltext>team</span> currently being exploited?

The defense points are scaled this way so that defenders are still able
to earn a similar amount of points to a small number of attacking teams,
and that being the first to attack a flagstore does not give so many points
that it is impossible for other teams to catch up.

To ensure that deleting flags in your own service is not a viable strategy for
earning DEF points, we award the defense points for a flag spread across all
rounds for which this flag must be retrievable. If a flag is unavailable
in a specific round, no defense points are awarded for that flag in that
round. Intuitively, this reflects the idea that defense points should be
gained for successful defending; if no flags are at risk, no reward is
earned.

```python3
def defense(live_round: int, flag_round: int, checker_status: dict[int, str],
            flag_avail_in: dict[int, dict[tuple[int, int, int, int], bool],
            max_victims: int, num_victims: int, num_attackers: int,
            exploited: bool, flag_rounds_valid: int = 5):
    pts = 0
    max_round = max(live_round + 1, flag_round + flag_rounds_valid)
    for rnd in range(flag_round, max_round):
        if checker_status[rnd] not in {"SUCCESS", "RECOVERING"}:
            continue
        if flag_avail_in[rnd][flag_round, team, service, flagstore]:
            pts += defense_raw(max_victims, num_victims, num_attackers, exploited)
    return pts / flag_rounds_valid
```

??? "Implementation Details"

    **Context**: Each <span class=hltext>round</span>, this function is called per <span class=hltext>service</span> and <span class=hltext>flag store</span>, for each active <span class=hltext>attacker</span> and for every <span class=hltext>team</span>, to update the value of teams defending / not defending the <span class=hltext>attack</span>.

    - `live_round`: The round of the game in which the defense points are being updated.
    - `flag_round`: The round of the game in which the flag being stolen was deployed.
    - `checker_status`: The status of the checker for this service for each round of the game.
    - `flag_avail_in`: A mapping for which flags were retrievable from a specific specific round (first key), depending on the team, service, flagstore and round they were deployed in. **Remember:** each round the checker checks that valid flags can be retrieved.
    - `max_victims`: The number of teams who are not the attacker or NOP, that have atleast one service not in <span class=hl-offline>`OFFLINE`</span> state in the current round.
    - `num_victims`: The number of teams exploited by the attack which points are currently being calculated for.
    - `num_attackers`: The number of teams attacking this <span class=hltext>service</span> and <span class=hltext>flagstore</span>, and obtaining flags stored in <span class=hltext>flag_round</span>.
    - `exploited`: Is this <span class=hltext>team</span> being exploited by the attack which points are currently being calculated for?
    - `flag_rounds_valid`: The number of rounds each flag is valid for.

Here, `live_round` is eventually large enough that the flag's *final* defense
value is calculated, taking into account the availability in all rounds the
flag is submittable for points.

At the end of the game, some flags need to be retained for fewer rounds.
This means that protecting these flags earns proportionally fewer points over time,
as there was also less time for other teams to capture them. However, the
total number of flags you need to protect (and thus the defense points
that can be earned in each round) does not change at the end of the game.

The NOP team does not gain defense points.

### SLA Points

To determine **SLA points**, the gameserver calculates the ratio between the
number of valid flags retrievable from a service and the number of rounds
a flag is valid for.

```python3
def sla(checker_status: str, flags_avail: int,
        max_score: int = 10, flag_rounds_valid: int = 5):
    if checker_status == "SUCCESS":
        return max_score * flagstores
    elif checker_status == "RECOVERING":
        return max_score * flags_avail / flag_rounds_valid
    else:
        return 0
```

??? "Implementation Details"

    **Context**: Each <span class=hltext>round</span>, this function is called per <span class=hltext>team</span> and per <span class=hltext>service</span>.

    - `checker_status`: The status returned by the checker for <span class=hltext>team</span> and <span class=hltext>service</span>.
    - `flags_avail`: The number of flags available in the last 5 rounds from all flagstores of <span class=hltext>service</span> for <span class=hltext>team</span>.
    - `max_score`: The maximum value of each *challenge*, see `jeopardy(..)` definition.
    - `flag_rounds_valid`: The number of rounds each flag is valid for.

This means that at the start of the CTF, SLA points ramp up from zero to `max_score`
over the first five rounds, as the validity period is five rounds long.


### Total Points

The total score is the sum of the **ATK**, **DEF** and **SLA** components.

For a typical attacking scenario involving `40` teams and `5` attackers,
for a service with `3` flagstores that is consistently available and exploited
by each attacker, and using the suggested `jeopardy(..)` dynamic scoring formula
with default parameters, we would see the following `attack(..)` for *attackers*,
`defense(..)` for *defenders* and `sla(..)` for *both*:

```vegalite 
{
  "data": {
    "url": "/assets/data/atklabv2_all.json"
  },
  "padding": {
    "right": 30
  },
  "height": 300,
  "autosize": "fit",
  "mark": {
    "type": "line",
    "tooltip": true,
    "color": "#bb86fce0",
    "point": {
        "filled": true,
        "color": "#bb86fce0"
    }
},
  "encoding": {
    "x": {"field": "victims", "type": "nominal", "axis": {"labelAngle": 0}},
    "y": {"field": "points", "type": "quantitative"},
    "color": {"field": "category", "type": "nominal", "scale": {"scheme": "set1"}}
  },
  "background": "#1f1f1f"
}
```

<span class=hltext>*Well, isnt there a problem here?? If teams gain more points from
defending, why attack at all??*</span>

First of all, it's important to note that points from attacking only need to be
larger than the defense gained from a single attack for the attack to be
profitable to the attacker.<br>This is still the case by design (showing defense / attack gained from one victim):

```vegalite 
{
  "data": {
    "url": "/assets/data/atklabv2_single.json"
  },
  "padding": {
    "right": 30
  },
  "height": 300,
  "autosize": "fit",
  "mark": {
    "type": "line",
    "tooltip": true,
    "color": "#bb86fce0",
    "point": {
        "filled": true,
        "color": "#bb86fce0"
    }
},
  "encoding": {
    "x": {"field": "victims", "type": "nominal", "axis": {"labelAngle": 0}},
    "y": {"field": "points", "type": "quantitative"},
    "color": {"field": "category", "type": "nominal", "scale": {"scheme": "set1"}}
  },
  "background": "#1f1f1f"
}
```

Second, the edge cases where the defenders are getting more points are:

1. when a single (or very few) teams are being successfully attacked by a
   large amount of attackers, the attack is worth less, since it is only able
   to exploit a few teams, while a defending team needs to prevent a lot of
   (potentially different) attacks.
2. when almost all teams are being successfully attacked, successfully
   defending means being the first to build a working patch (without
   being able copy it from network behavior of another team), which is
   especially difficult and should be rewarded accordingly.

With the given formula, defending against all attackers becomes more econimical
than (but does not disincentivize) attacking once the number of attackers
for a specific flagstore exceeds roughly one fourth the number of participating teams.


## Review

- Since the capture count of each stored flag determines its worth,
  attackers are rewarded based on how difficult it is to exploit each specific
  team.
- The same goes for defense; a patch is rewarded based on the number of other
  teams that could not defend against the exploiting team. If a
  vulnerability is harder to patch or a specific exploit is harder to defend
  against, successfully doing so earns more defense points.
- Any round that a service is offline or malfunctioning, the corresponding
  team loses points relative to the amount of flags they did not make available
  to other players. If the team is not defending, it is `flagstores * max_score`.
  If the team is defending, it is more.
- Teams only lose SLA and DEF points relative to the amount of rounds each flag
  has been made unavaiable for. Since the points from defending are spread across the
  rounds in which the flag is being checked, and recovering points are awarded
  according to the amount of flags avialable, patching does not cost the
  full defense / sla for the rounds in which a team is recovering after patching.
- A service should be unavailable for at most a few (let's say 3) rounds due
  to (unsuccesful) patching. We find that the points lost are
  `flagstores * base + (flagstores - 1) * (teams - 2) * base` per round,
  assuming all other flagstores are patched, and that the minimum gain from
  the additional patched flagstore is `(teams - 2) * jeopardy(teams - 2)` per round,
  assuming all other teams apart from NOP have patched and are attacking.
  The unrealistic scenarion aside (all teams only successfully attacking you in
  a single flagstore while you are the only team to have all other flagstores patched),
  the number of subsequent rounds rounds a team would have to be available
  for following 3 rounds of downtime is at most 60 rounds. This is a lot,
  but would be far lower in practice - e.g. roughly one round if the other
  flagstores are not earning defense points.

## Tenets

1. {{ tenet1_atklabv2 }}
2. {{ tenet2_atklabv2 }}
3. {{ tenet3_atklabv2 }}
4. {{ tenet4_atklabv2 }}
5. {{ tenet5_atklabv2 }}
6. {{ tenet6_atklabv2 }}
7. {{ tenet7_atklabv2 }}

<!---
## Evaluation

To determine if the formula has a positive effect on defense weight and merging,
we compare it to the scoring formula used in ECSC 2024. Since the scoring
formula influences player behavior, we evaluate both the scoring data
from ECSC 2024 (which uses the [ECSC 2024](ecsc2024.md) formula)
and ECSC 2025 (which uses the ATKLABv2-derived [ECSC 2025](ecsc2025.md) formula

The following shows the top 5 teams for ECSC 2024:

<div class="grid cards" markdown>

```vegalite 
{
  "data": {
    "url": "/assets/data/atklabv2_single.json"
  },
  "padding": {
    "right": 30
  },
  "height": 300,
  "autosize": "fit",
  "mark": {
    "type": "line",
    "tooltip": true,
    "color": "#bb86fce0",
    "point": {
        "filled": true,
        "color": "#bb86fce0"
    }
},
  "encoding": {
    "x": {"field": "rounds", "type": "nominal", "axis": {"labelAngle": 0}},
    "y": {"field": "points", "type": "quantitative"},
    "color": {"field": "category", "type": "nominal", "scale": {"scheme": "dark2"}}
  },
  "background": "#1f1f1f"
}
```

```vegalite 
{
  "data": {
    "url": "/assets/data/atklabv2_single.json"
  },
  "padding": {
    "right": 30
  },
  "height": 300,
  "autosize": "fit",
  "mark": {
    "type": "line",
    "tooltip": true,
    "color": "#bb86fce0",
    "point": {
        "filled": true,
        "color": "#bb86fce0"
    }
},
  "encoding": {
    "x": {"field": "victims", "type": "nominal", "axis": {"labelAngle": 0}},
    "y": {"field": "points", "type": "quantitative"},
    "color": {"field": "category", "type": "nominal", "scale": {"scheme": "set1"}}
  },
  "background": "#1f1f1f"
}
```

</div>

When merged this results in the following scoreboards:

<div class="grid cards" markdown>
<div>
1. Test<br>
2. arstrst<br>
</div>

<div>
1. Test<br>
2. arstrst<br>
</div>
</div>

The following shows the two scoring formulas for ECSC 2025:


When merged this results in the following scoreboards:


One other positive outcome of the new scoring formula, is that teams near the
top of the scoreboard are closer together, which makes the game more exciting.
-->

## Player FAQ

??? question "Why is our team *losing* defense / attack points?"

    Teams may appear to *lose* defense or attack points when the value of the attacks
    they defended against or the flags they submitted decreases. This calculation
    is retroactive as flags may be submitted up to 4 rounds *after* the round
    in which they are deployed.

??? question "Why are the defense points not zero in a round our service status is neither <span class=hl-success>`SUCCESS`</span> or <span class=hl-recovering>`RECOVERING`</span>?"

    Most likely, a team was attacking your service before it went down and submitted
    (at least some of) those flags in the round before it went down. These flags
    are only considered in the next round, and you are then awarded
    defense points for defending against this exploit from the previous round
    retroactively.
    Crucially, you do not gain defense points for any flag stores not retrievable
    in the round in which your service was down.

??? question "Why are the defense points zero in the first round after our service is available if we didnt get exploited?"

    The defense points may be zero in this round because no other team is
    attacking the flag store yet. Attackers typically rely on
    <a href="https://wiki.attacking-lab.com/attack-defense/#attack_info:~:text=attack%20info">attack info</a>,
    which is only released in the subsequent round. If your service was
    unavailable for multiple rounds before this one, then no team will have
    attack info to attack the service with in the first round it is available.


<!--
## Considerations

??? question "Why not allow attacks against NOP team to count attacks as active, even if the flags themselves dont give any points?"

    Allowing attacks against NOP team to keep attacks 'active', thereby giving
    attackers ATK points even if there are no player victims left, has the
    benefit of removing the edge-case where a single victim team is incentivized
    to turn off their service (since the attacker would not be getting their
    base attack score otherwise).

    Counting NOP for active attacks has the same downside as counting NOP flags
    though, which is that teams can gain points without the risk of having
    their exploit stolen. Whether the risk of abusing this tactic is higher
    than that of a team being the only one attacked by all other teams and turning
    off their service, depends on the size and nature of the competition.
-->
