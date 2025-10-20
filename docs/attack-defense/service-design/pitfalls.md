# Common Pitfalls

## DoS (Denial of Service)

- **Watch out for amplification techniques**; service functionality that could be used to overwhelm the system with a relatively low amount of network traffic.

## Exploitation/patchability

- **Consider lateral movement**; ensure attackers' access to multiple flag stores is possible only when explicitly intended and the exploit conditions are sufficiently restrictive.
- **Try to balance the difficulty to exploit and patch**; vulnerabilities that are difficult to patch but easy to exploit are preferred. This is because the reverse case reduces traffic between teams and disincentivizes core A/D strategies such as reverse-engineering exploits from traffic monitoring.

## Checkers

- **Prevent checker fingerprinting**; randomize functionality checks, use randomized user data, and vary user-agents.
- **Perform all available checks every round**; unreliable checkers deny players consistent feedback for patches.
- **Check the service thoroughly**; the goal is for teams to patch services, not re-implement SLA-compatible skeletons.


<div style="height: 10px"></div>

---

<small>
Inspired by [lavish'](https://github.com/lavish) [CTF-Doc](https://github.com/lavish/CTF-Doc/blob/main/SERVICE.md)
</small>
