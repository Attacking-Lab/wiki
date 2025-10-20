# Attack-Defense Strategy

This section outlines some strategies for playing A/D CTFs, ranked from least to most
advanced.


### Taking Inventory

Gathering information about each service at the start of the CTF, and
using this to assign players and prioritize work will maximize your
expected return from searching for vulnerabilities.

Tools like [CTFNote](https://github.com/TFNS/CTFNote) were made specifically
to help with this task.


### Low Hanging Fruit

Because exploits deployed early can collect points over the entire CTF,
taking a basic overview of each service and identifying *low-hanging fruit*
before the network opens is essential. Moreover, vulnerabilities found can
be patched before other players have the chance to exploit them.


### Attack vs Defense

Since most [scoring formulas](/attack-defense/scoring/index.md) favor attack over defense,
players should prioritize writing exploits over patching, except in those cases
where writing the exploit is disproportionately difficult.
Conversely, teams should prioritize implementing exploits that are easy to
write but difficult to patch.


### Attack Replay & Obfuscation

Most exploits can be stolen by observing network traffic, and reversing an
exploit this way is often easier than finding it yourself. Some
[monitoring tools](attack-defense/paying/monitoring), notably
[Tulip](https://github.com/OpenAttackDefenseTools/tulip), will even automate
part of the process, providing a `Copy as Pwntools` button for generating
Python scripts using [pwntools](https://github.com/Gallopsled/pwntools)
which mimic the recorded traffic.

Because of this, it can pay off to obfuscate your exploit traffic,
especially when the vulnerability is difficult to find and has not yet
been exploited.


### Checker Fingerprinting

Capturing game traffic directly after network open can help differentiate
checker from exploit traffic at a later stage in the game. As long as the
service is not immediately exploited, early-game traffic is less likely to
originate from other players. This traffic capture may prove useful at a later
stage of the game to differentiate checker from exploit traffic.

If the checker behaves in a way that players can detect without being
able to replicate it themselves (e.g., using a specific private key
for a crypto service), it allows teams to build so-called **Superman-Defenses**,
preventing any non-checker requests from reaching the service.

