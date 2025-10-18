# Aggregated Scoring

Competitions like [ECSC 2025](ecsc2025.md) that feature both Jeopardy
and Attack-Defense CTFs require a method of combining the scoreboards
for these distinctly different competitions without valuing one or
the other more highly.

The most common approach is to merge scoreboards by normalization and average.

```python
jeopardy: list[float] # team jeopardy scores
attackdefense: list[float] # team attack-defense scores
w = max(jeopardy) / max(attackdefense)
aggregated = [s1 + s2 * w for s1,s2 in zip(jeopardy, attackdefense)]
```

This has some obvious drawbacks. Most notably, the first few teams in an
Attack-Defense CTF with "classic" scoring typically have significantly more
points than the rest, unlike in Jeopardy. Also, when SLA is valued highly by
the scoring formula, this pratically constant score added to each team devalues
the Jeopardy challenges when merging.

This was the motivation for developing [ATKLABv2](atklabv2.md), which can be
used with the Jeopardy scoring fomula to dynamically weight the Attack-Defense
*challenges*, ideally mapping skill to points in the same way.

Another benefit of [ATKLABv2](atklabv2.md) is that the final NOP team score
can be used as a baseline measure for points which did not require any effort
by teams to be earned, since it can neither gain points from attack nor defense.

Thus, this score can be removed from each team's attack-defense score before
merging.

```python
nop = attackdefense[0]
w = max(jeopardy) / (max(attackdefense) - nop)
aggregated = [s1 + (s2 - nop) * w for s1,s2 in zip(jeopardy, attackdefense)]
```

It is highly unlikely for a playing team to earn less points than
NOP using this formula.
