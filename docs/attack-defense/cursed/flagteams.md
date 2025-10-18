# Flag Teams

<span class=hltext>Flag teams are fake teams created for the sole purpose
of collecting flags from the checker, to be submitted by the offending team.</span>

Flag teams are a particularly difficult issue with purely online A/D CTFs,
since it is practically impossible to enforce a single team per player.

An offending team may register multiple flag teams ahead of time and collect
flags from them during the CTF (after first-blood to avoid suspicion)
without ever knowing how to exploit the service.

Furthermore, to prevent other teams from exploiting their fake teams, they may
use firewalls that filter outbound flags (or other filesystem based techniques).
The services do not pass the SLA check, but the checker will still be able to
deploy flags for the offending team to submit.
