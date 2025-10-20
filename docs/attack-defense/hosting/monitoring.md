# Attack-Defense Monitoring

Network monitoring is an especially important aspect of CTF hosting, since
players expect quick investigation into suspected misconduct and accurate
attribution. Depending on the volume of game traffic (influenced by the
round-time of the CTF and restricted by the per-team bandwidth limits) this
can be a non-trivial task.

## Star/Tree Topology

In a star/tree topology, the monitoring can take place on the central
node using the
[same monitoring tooling used for playing CTFs](/attack-defense/playing/monitoring.md),
although organizers need to ensure they can handle the higher network load
and traffic varieties (A/D tooling typically focuses on TCP).

## Mesh Networking

In a mesh network, the network traffic needs to be collected from each router
and either analyzed at the point of capture or sent to a central node for
processing. Since mesh networking is typically employed when network bandwidth
per machine is limited, routing traffic to a single machine is not feasible.

As far as we know, the only battle-hardened, open-source tool capable of
aggregating and analyzing packet contents from multiple nodes is
[Arkime](/attack-defense/playing/monitoring.md#arkimearkime).
