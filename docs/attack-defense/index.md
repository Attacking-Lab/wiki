# Attack-Defense CTFs

**Attack-Defense** is a style of CTF in which teams host services and exploit
each other over a shared, private network.

The game progresses in fixed time intervals (**rounds**) lasting typically
between one and five minutes. Throughout each round, the organizers attempt
to place unique secrets (**flags**) in each service. Extracting these secrets
from other teams' services and submitting them to a flag server each round to
earn <b><abbr title="Attack">ATK</abbr> points</b> is the primary goal of the
game.

{{ admon_flat("flag stores", "A single service may store multiple unique flags
each round in different <b>flag stores</b>, and may have more than one intended
vulnerability to reach each one.", icon="var(--inline-icon--flag)") }}

To incentivize teams to keep their services available to other teams to exploit,
a series of checks is performed each round against every service of every team
by the organizers' **checkers**. These tests define the so-called *Service-Level
Agreement* (**SLA**); the functionality required for a team to earn
**SLA points** each round.

{{ admon_flat("attack info", "Checkers may also expose <a href=\"/attack-defense/game-design/attack-info/\">attack info</a> per
vulnerability each round to help guide players on what to exploit to collect flags for
a specific round.", icon="var(--inline-icon--info)") }}

Each round, a team receives <b><abbr title="Defense">DEF</abbr> points</b> for 
every service. The amount of points earned is highest when the service is
unexploited and decreases with the number of other teams exploiting it.

These points combine to calculate the team score using a
[scoring formula](scoring-formula/index.md), which can vary between CTFs.

Ultimately, there are 3 objectives each round to win the game:

1. Exploit other teams
2. Prevent other teams from exploiting you
3. Pass the SLA check
