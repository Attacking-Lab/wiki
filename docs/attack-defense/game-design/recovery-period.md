# Recovery Period

<span class=hltext>The recovery period is the set of rounds from which a flag
needs to available in the current round, so that the service is not marked as
*recovering*.</span>

The recovery period is ideally smaller than or equal to the validity period,
the set of rounds in which a flag can still be submitted for points.

Often CTFs set the recovery period lower than the validity period though,
allowing players to reduce the impact of an exploiot by reducing the retention
time for flags stored in their services.
