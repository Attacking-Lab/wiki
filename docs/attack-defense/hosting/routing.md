# Attack-Defense Routing

Generally A/D routing approaches can be split into two categories:
those with a root node responsible for traffic shaping and SNAT, and
those with multiple routers that handle a fraction of the total network load.

## Star/Tree Topology

Tree routing is by far the simpler and more popular variety, which is demonstrated
by its use in all of the well-known A/D gameservers, such as
[MarkusBauer/saarctf-gameserver](https://github.com/MarkusBauer/saarctf-gameserver),
[enowars/EnoEngine](https://github.com/enowars/EnoEngine),
[fausecteam/ctf-gameserver](https://github.com/fausecteam/ctf-gameserver)
and their derivatives. Having a single traffic-shaping node means all
game logic can be configured and stored in a single place. Additionally,
any live changes to the game network (such as *network open*) can take place
by applying rules to a single machine without having to worry about
synchronization between routers.

## Mesh Networking

Mesh networking is generally more complicated, but lends itself to scenarios
where per-machine bandwidth and/or compute resources are limited, such that
the entire game traffic cannot be processed on a single node.

Another upside of mesh networking is that for cloud-hosted CTFs, a DoS
attack can only impact the teams associated with their router, since this
is the only public-facing element of the game network that a team will be
aware of (the scoreboard can be accessible through the game network and as such
would not be affected by DoS'ing the public IP). If the router-mapping is N-to-N,
which is practical for small CTFs, this allows direct attribution of attacks
against the infrastructure.

*[SNAT]: Source Network Address Translation
*[DoS]: Denial-of-Service
