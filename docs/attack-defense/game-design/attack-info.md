# Attack Info

<span class=hltext>Attack info is information provided by the checker,
necessary for exploiting a flagstore without causing excessive network
or service load.</span>

Attack info is made available for the round following the one in which the
flags are deployed, typically through an API. Below we have documented
some of the common API interfaces.

## FAUST CTF 2024

```sh
curl http://scoreboard/teams.json
```
```json
{
    "teams": [
        # team ids
        123, 456, 789,
        ..
    ],
    "flag_ids": {
        # service name : service info
        "service1": {
            # team id : attack infos for validity period
            "123": ["abc123", "def456"],
            "124": ["xxx", "yyy"],
            ..
        },
        ..
    }
}
```

## saarCTF 2024

```sh
curl http://scoreboard/attack.json
```
```json
{
    "teams": [
        # team infos
        {
            "id": 1,
            "name": "NOP",
            "ip": "10.42.1.2"
        },
        ..
    ],
    "flag_ids": {
        # service name : service info
        "fooserv": {
            # team vulnbox ip : team info
            "10.42.1.2": {
                # round id : attack info
                "123": ["info_flag1", "info_flag2"]
                ..
            },
            ..
        },
        "barserv": {
            "10.42.1.2": {
                # as string if only one flagstore
                "123": "info_single"
            },
            ..
        }
    }
}
```

