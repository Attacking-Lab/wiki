# Traffic Mirroring

<span class=hltext>Traffic mirroring is a technique in which a team mirrors
traffic from their own service to another team, which has patched the service
and ranks lower than they are.</span>

This way, the mirroring team benefits from the gain of positive (or absence
of negative) defense points, while being able to focus their efforts on
other services.

The team receiving the mirrored traffic clearly benefits from this too, as
they can submit the mirroring team's flags, but as long as they rank lower
than the mirroring team, it is still in the mirroring team's interest to do so.

In competitions with *guest teams*, such as ECSC 2025, teams are incentivized
to mirror traffic on unpatched services to these teams, which will not affect
their ranking in the final scoreboard.

Since the team receiving the mirrored traffic typically notices this quickly
and it is easily verifiable by inspecting network traffic, <span class=hltext>
the easiest way to prevent this behavior is through a policy ban</span>.
Often it is already covered by the provision, that flag sharing is not allowed.
