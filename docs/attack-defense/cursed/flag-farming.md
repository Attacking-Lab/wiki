# Flag Farming

<span class=hltext>Flag farming is the process of registering fake teams
for the sole purpose of collecting flags from the checker, to be submitted
by the offending team.</span>

Flag farming is a particularly difficult issue with online A/D CTFs,
since it is practically impossible to enforce a single team per player.

An offending team may register multiple fake teams ahead of time and collect
flags from them during the CTF without ever knowing how to exploit the service.

Furthermore, to prevent other teams from exploiting their fake teams, offending
teams may use firewalls that filter outbound flags (or other filesystem-based techniques).
Even though services will not pass the SLA check this way, they will still
receive flags from the checker.

Organizers must have proper monitoring and traffic capture infrastructure
to investigate such cases in a timely manner, such that disputes may
be settled and the winners declared shortly after end of the CTF.
