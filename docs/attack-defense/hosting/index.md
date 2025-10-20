# Hosting Attack-Defense CTFs

Basic [gameplay](/attack-defense/index.md#gameplay) knowledge is required for this section.

## Infrastructure

The basic components required to host an Attack-Defense CTF are a **scoreboard**,
a **flag submission**, the teams services (**vulnboxes**) and their
**checkers**. Typically, there is also some component which orchestrates
the checkers, queries the flag submission and computes team scores, but since
a connection to the game network is not required it is not included here.

<div style="height:1em"></div>
![game Infrastructure](infra.svg)
<div style="height:1em"></div>

In cloud-hosted competitions, teams communicate with services in the game network
by joining the organizer's virtual private network, typically facilitated
through [Wireguard](https://www.wireguard.com).


