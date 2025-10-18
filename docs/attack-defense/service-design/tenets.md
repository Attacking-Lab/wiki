# Service Tenets

In this section we use [RFC2119](https://www.ietf.org/rfc/rfc2119.txt) keywords to specify service / checker requirements.

## Service

{% set service_tenet1 = admon("A service **MUST** be able to keep track of flags for a specified number of rounds", "The service **must** keep track of flags for atleast one round to allow extraction through exploitation. Requiring flags to be stored for more than one round allows for use of [recovery periods](/attack-defense/scoring-formula/faust2024.md) and for players to investigate service artifacts related to network traffic before they are removed.", icon="var(--inline-icon--shield-heart)") %}
{% set service_tenet2 = admon("A service **MUST NOT** lose existing flags due to being restarted", "The service **must** not hold important data in volatile memory, as this makes the result of patching on SLA unnecessarily unpredictable and violates an assumption many players will make about service behavior.", icon="var(--inline-icon--shield-heart)") %}
{% set service_tenet3 = admon("A service **MUST** be able to handle game traffic with reasonable compute resources", "SLA **must** be a measure of the effort and skill of the players, not of the compute at their disposal. Ideally the players are able to achieve 100% SLA on organizer-provided vulnboxes.", icon="var(--inline-icon--storage)") %}
{% set service_tenet4 = admon("A service **MUST** have at least one, but **MAY** have multiple flag stores", "For each service to be exploitable, it **must** have atleast one vulnerability and therefore flag store. Multiple flag stores allows for more depth in service design and exploitation than a single flagstore with multiple vulnerabilities, since players will need to understand how data is stored in each flagstore, which may have a completely individual implementation.", icon="var(--inline-icon--flag)") %}
{% set service_tenet5 = admon("It **SHOULD NOT** be practical to reimplement a service within the timeframe of the contest", "For the CTF results to rank team skill and effort, all teams must participate and solve the same problems. This is not the case, when patching can be circumvented by replacing the service with a skeleton implementing just enough features to pass the SLA check and avoid exploitation.", icon="var(--inline-icon--shield-cross)") %}

1. {{ service_tenet1 }}
- {{ service_tenet2 }}
- {{ service_tenet3 }}
- {{ service_tenet4 }}
- {{ service_tenet5 }}

## Vulnerabilities

{% set vuln_tenet1 = admon("A service **MUST** have one or more vulnerabilities, and **SHOULD** have at least one complex one", "Each service **must** be exploitable, such is the nature of the competition, and thus have atleast one intended vulnerability. Atleast one complex vulnerability ensures the players' effort of analyzing each service in detail is rewarded.", icon="var(--inline-icon--shield)") %}
{% set vuln_tenet2 = admon("An unpatched vulnerability **MUST** be exploitable and result in a correct flag", "This is the definition of a service vulnerability.", icon="var(--inline-icon--shield-check)") %}
{% set vuln_tenet3 = admon("An unpatched vulnerability **SHOULD** be exploitable within the round time.", "Since the attack-defense format is designed around a round schedule, each action **should** complete within a single round for ease of reasoning about game state. Note, this tenet concerns vulnerability which can't be exploited within a single round, but **not due to computational bounds**. If the service is required to keep flags for more than one round, it is valid for exploits to take more than one round to retrieve the flag.", icon="var(--inline-icon--timer)") %}
{% set vuln_tenet4 = admon("An unpatched vulnerability **SHOULD** be exploitable over the course of the complete game", "Each vulnerability **should** be available throughout the course of the game to be able to accuartely reason about how team performance changes over time. This is also an assumption many players will make about vulnerability behavior.", icon="var(--inline-icon--clock)") %}
{% set vuln_tenet5 = admon("Every vulnerability **MUST** be patchable without breaking the checker", "Changes to the service necessary to fix a vulnerability **must not** impact the performance of the checker negatively.", icon="var(--inline-icon--destroy)") %}
{% set vuln_tenet6 = admon("A vulnerability **MUST** be exploitable with reasonable computing resources", "The contest **must** reflect the teams effort and skill, not the extent of their computing resources.", icon="var(--inline-icon--storage)") %}
{% set vuln_tenet7 = admon("A vulnerability **MUST** be exploitable with reasonable amounts of network traffic", "The contest **must** reflect the teams effort and skill, not the extent of their network bandwidth.", icon="var(--inline-icon--network)") %}
{% set vuln_tenet8 = admon("A service **SHOULD NOT** have unintended vulnerabilities", "For the organizers to prevent manipulation of vulnboxes by other teams via unintended remote-code execution, and accurately gauge the difficulty of each service to balance it against the scoring weight, they **must** be aware of every vulnerability in every service.", icon="var(--inline-icon--shield-cross)") %}
{% set vuln_tenet9 = admon("A service **MUST NOT** have vulnerabilities that allow only one attacker to extract a flag", "For the contest to measure team effort and skill, granted points **must not** depend on infrastructure factors which allow one team to exploit a race-condition more consistently others. This includes flag-deletion.", icon="var(--inline-icon--timer)") %}
{% set vuln_tenet10 = admon("A service **SHOULD** have atleast one vulnerability which is not easily replayable", "To prevent other teams from reversing exploits soley from the game traffic, atleast one vulnerability of each service **should not** produce traffic which can easily be correlated, to the extent possible.", icon="var(--inline-icon--search-graph)") %}
{% set vuln_tenet11 = admon("All vulnerabilities **SHOULD NOT** be exploited by a single team by the end of the game", "To ensure players stay entertained throuhgout the CTF, and accurately measure the range of teams' effort and skill, no team **should** reach the maximum amount of points possible by exploiting every vulnerability before the end of the contest.", icon="var(--inline-icon--shield-cross)") %}
{% set vuln_tenet12 = admon("Vulnerabilities **SHOULD** be exploitable and patchable with reasonable effort in the alloted time", "Patching a vulnerability **must not** require more time than is alloted in the contest while expending reasonable effort. Since team effort and skill is measured by scoreboard performance, and a service which cannot be exploited does not contribute to the scoreboard, this violates the purpose of the contest.", icon="var(--inline-icon--clock)") %}

1. {{ vuln_tenet1 }}
2. {{ vuln_tenet2 }}
3. {{ vuln_tenet3 }}
4. {{ vuln_tenet4 }}
5. {{ vuln_tenet5 }}
6. {{ vuln_tenet6 }}
7. {{ vuln_tenet7 }}
8. {{ vuln_tenet8 }}
9. {{ vuln_tenet9 }}
10. {{ vuln_tenet10 }}
11. {{ vuln_tenet11 }}
12. {{ vuln_tenet12 }}

## Checkers

{% set checker_tenet1 = admon("A checker **MUST** check whether a flag is retrievable, and fail iff the flag is not retrievable", "This is the definition of the Service-Level Agreement.", icon="var(--inline-icon--shield-heart)") %}
{% set checker_tenet2 = admon("A checker **MUST NOT** crash or return unexpected results under any circumstances", "For the competition to reflect the effort and skill of teams, their ability to patch vulnerabilities must be measured accurately, which is not possible if the checker is unable to do so.", icon="var(--inline-icon--destroy)") %}
{% set checker_tenet3 = admon("A checker **MUST NOT** rely on information stored in the service in rounds before the flag was inserted", "Players expect a checker to test the full functionality of a service every tick, independent of how the service performed last tick, thus relying on such stateful information **must** be avoided.", icon="var(--inline-icon--timer)") %}
{% set checker_tenet4 = admon("A checker **MUST** log sufficiently detailed information that operators can handle complaints from participants", "For organizers to properly attribute issues in the checker behavior and process user requests, which they **must**, the checker **must** provide logs that aid them in that task.", icon="var(--inline-icon--log)") %}
{% set checker_tenet5 = admon("A checker **MUST** check the functionality of a service sufficiently to prevent reimplementation", "The checker **must** check the service surface area sufficiently to prevent teams from reimplementing the required checks within the timeframe of the contest. This is the compliment requirement to [Service Tenet 5](#it_should_not_be_practical_to_reimplement_a_service_within_the_timeframe_of_the_contest).", icon="var(--inline-icon--timer)") %}
{% set checker_tenet6 = admon("A checker **SHOULD** not be easily identified by the examination of network traffic", "To accurately detect whether services are available to all players, which is a prerequisite for the fair evaluation of teams' effort and skill, the checker must be indistinguishable from other traffic, such that it can not be fingerprinted and treated separately.", icon="var(--inline-icon--search-graph)") %}
{% set checker_tenet7 = admon("A checker **SHOULD** use unusual, incorrect or pseudomalicious input to detect network filters", "Since patching in the contest is meant emulate the real-life equivalent, patches **should not** be based on specific user(-data) patterns, but on the interaction involved with the vulnerability.", icon="var(--inline-icon--destroy)") %}

1. {{ checker_tenet1 }}
2. {{ checker_tenet2 }}
3. {{ checker_tenet3 }}
4. {{ checker_tenet4 }}
5. {{ checker_tenet5 }}
6. {{ checker_tenet6 }}
7. {{ checker_tenet7 }}

<div style="height:10px"></div>

---

<small>
[Original checker specification](https://github.com/enowars/specification/blob/main/service_checker_tenets.md) by [ENOFLAG](https://github.com/enoflag)
</small>
