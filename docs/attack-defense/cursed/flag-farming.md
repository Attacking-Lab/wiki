# Flag Farming

<span class=hltext>Flag farming is the practice of creating *puppet teams* — fake teams
whose sole purpose is collecting flags from the checker, to be submitted by
the offending team.</span>

Flag farming is a particularly difficult issue with purely online A/D CTFs,
since it is practically impossible to enforce a single team per player.

An offending team may register multiple puppet teams ahead of time and collect
flags from them during the CTF (after first-blood to avoid suspicion)
without ever knowing how to exploit the service.

Furthermore, to prevent other teams from exploiting their fake teams, offending
teams may use firewalls that filter outbound flags (or other filesystem-based techniques).
Even though services will not pass the SLA check this way, they will still
receive flags from the checker.
