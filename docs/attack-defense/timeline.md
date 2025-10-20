# Attack-Defense Timeline

Compared to Jeopardy-style CTFs, which typically last from 24 to 72 hours,
an Attack-Defense CTF can be played in a single session, lasting around **8 hours**.
This is because the need to constantly monitor traffic and respond quickly to
enemy attacks is much more stressful than solving challenges on your own time
in a Jeopardy CTF. It also gives players the much-needed time to sleep.

A typical CTF has the following timeline:

![game timeline](timeline.svg)
**Network Closed**: Traffic to other teams is blocked in the a few
minutes of the game, the network is **down**. This gives players
the opportunity to find vulnerabilities and patch services before they have a
chance to be exploited. During this time, the checkers are inactive; neither ATK,
DEF, nor SLA points are awarded. The scoreboard may also be unavailable.

**Network Open**: Eventually, the network is **opened** and the first
round of the CTF begins. At this point, both checkers and enemy players can
start communicating with the services of your vulnbox. Crucially, this happens
at the same time to prevent easily profiling the behavior of the checker
early on in the CTF.

**Scoreboard Freeze**: Some CTFs prevent the scoreboard from updating near the
end of the competition. Apart from delaying the announcement of the winner for
dramatic effect, this also gives teams a final opportunity to deploy exploits
without the scoreboard alarming other teams of their attack.
