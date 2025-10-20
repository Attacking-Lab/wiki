# Checker Hold

A **checker hold** is a period of time during each tick that no tasks are
being processed by the checker, and thus no connections are open to the
teams' services that might be interrupted by a restart.

The motivation for a time window with no traffic comes from the fact that some
[scoring formulas](/attack-defense/scoring-formula/index.md) rely on large SLA
for disincentivizing metagame tactics. This puts a large burden on players who
patch their service, since they risk losing one round of SLA—or more if flags
could not be placed due to the downtime.

Since checker task scheduling is unpredictable by design, patching without
a guarantee is inherently unfair and does not properly measure skill.

In practice, the number of game rounds far exceeds the number of rounds of SLA
a team would lose due to patching. Since all teams are equally subject
to the randomness of the checker, it only needs to be considered for
high-stakes competitions.
