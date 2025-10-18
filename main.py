import string

def idstr(text):
    return "".join([c for c in text.lower().replace(" ", "_") if c in string.ascii_lowercase + string.digits + "-_+"])

def define_env(env):
    @env.macro
    def admon(summary, description, idname=None, classnames="custom", icon="url('graph-up.svg')", color_hex = None, open=False):
        style = f"--md-admonition-icon--custom: {icon}; "
        idname = idname or idstr(summary)
        if color_hex is not None:
            bgcolor_hex = f"{color_hex}19"
            style += f'--md-admonition-color--custom: #{color_hex}; --md-admonition-bgcolor--custom: #{bgcolor_hex}'
        return f'<details {"open" if open else ""} id={idname} style="{style}" class="{classnames}"><summary>{summary}</summary><p>{description}</p></details>'

    @env.macro
    def admon_flat(summary, description, idname=None, classnames="custom", color_hex = None, icon="url('graph-up.svg')"):
        style = f"--md-admonition-icon--custom: {icon}; "
        idname = idname or idstr(summary)
        if color_hex is not None:
            bgcolor_hex = f"{color_hex}19"
            style += f'--md-admonition-color--custom: #{color_hex}; --md-admonition-bgcolor--custom: #{bgcolor_hex}'
        return f'<div id={idstr(summary)} style="{style}" class="admonition {classnames}"><p class=admonition-title>{summary}</p><p>{description}</p></div>'

    @env.macro
    def tenet1_adm(description, **kwargs):
        return admon('Total score **MUST** increase with more flags captured',
                     description, idname="tenet1", **kwargs)

    @env.macro
    def tenet2_adm(description, **kwargs):
        return admon('Total score **MUST** decrease with more flags lost',
                     description, idname="tenet2", **kwargs)

    @env.macro
    def tenet3_adm(description, **kwargs):
        return admon('Flag value **MUST** diminish with more successful attacks',
                     description, idname="tenet3", **kwargs)

    @env.macro
    def tenet4_adm(description, **kwargs):
        return admon('Perfect SLA **MUST** be worth more than any attacker\'s *relative* gain',
                     description, idname="tenet4", **kwargs)

    @env.macro
    def tenet5_adm(description, **kwargs):
        return admon('The cost of downtime **MUST NOT** outweigh the benefits of patching',
                     description, idname="tenet5", **kwargs)

    @env.macro
    def tenet6_adm(description, **kwargs):
        return admon('SLA **SHOULD** decrease fairly with every missing flag in the *retention period*',
                     description, idname="tenet6", **kwargs)

    @env.macro
    def tenet7_adm(description, **kwargs):
        return admon('Flag value **SHOULD** be calculated independent of its flagstore',
                     description, idname="tenet7", **kwargs)


    env.variables["tenet1"] = tenet1_adm('The scoring formula **must** reward the effort and skill required to exploit more services, and thus to capture more flags.', icon="var(--inline-icon--graph-up)")
    env.variables["tenet2"] = tenet2_adm('The scoring formula **must** reward the effort and skill required to defend against attacks.',  icon="var(--inline-icon--graph-up)")
    env.variables["tenet3"] = tenet3_adm('The scoring formula **must** reward the effort and skill required to exploit a vulnerability in proportion to its difficulty, inferred from the number of successful exploits.', icon="var(--inline-icon--flag)")
    env.variables["tenet4"] = tenet4_adm('The scoring formula **must** reward participation in the CTF and therefore disincentivize intentionally shutting off services to prevent other teams from overtaking you.', icon="var(--inline-icon--shield-heart)")
    env.variables["tenet5"] = tenet5_adm('To accurately measure player effort and skill in exploiting and defending, the scoring formula **must not** put such a disproportionate emphasis on defense or SLA, e.g. by scaling attack points with either, that it disincentivizes patching.', icon="var(--inline-icon--shield-cross)")
    env.variables["tenet6"] = tenet6_adm('We define the *retention period* as the number of rounds N (>= 0) that a service must retain deployed flags for to receive full SLA. The scoring formula **should** award partial SLA points according to the fraction of flags retrieved and make this information available to the players.', icon="var(--inline-icon--shield-heart)")
    env.variables["tenet7"] = tenet7_adm('Vulnerabilities in services with many flagstores **should not** be worth less to exploit. The dynamic flag value calculation already ensures that more difficult exploits are rewarded.', icon="var(--inline-icon--flag)")

    env.variables["tenet1_faust2024"] = tenet1_adm("Attack points scale linearly with the amount of flags captured.", classnames="success")
    env.variables["tenet2_faust2024"] = tenet2_adm("Defense points scale linearly with the amount of flags lost.", classnames="success")
    env.variables["tenet3_faust2024"] = tenet3_adm("Flag values scales inversely with the amount of captures.", classnames="success")
    env.variables["tenet4_faust2024"] = tenet4_adm("In the worst-case, when every team exploits a service, more defense points are lost than gained from SLA.", classnames="failure", open=True)
    env.variables["tenet5_faust2024"] = tenet5_adm("The cost of downtime is similar to the cost of defense per round. Patches prevent loss of points over multiple rounds and are thus favorable to not patching.", classnames="success")
    env.variables["tenet6_faust2024"] = tenet6_adm("SLA points awarded from recovering services do not scale with amount of uptime in the *retention period*.", classnames="warning", open=True)
    env.variables["tenet7_faust2024"] = tenet7_adm("Flag value is not scaled to the number of flagstores and thus independent.", classnames="success")

    env.variables["tenet1_saar2024"] = tenet1_adm("Attack points scale linearly with the amount of flags captured.", classnames="success")
    env.variables["tenet2_saar2024"] = tenet2_adm("Defense points scale linearly with the amount of flags lost.", classnames="success")
    env.variables["tenet3_saar2024"] = tenet3_adm("Flag values scales inversely with the amount of captures.", classnames="success")
    env.variables["tenet4_saar2024"] = tenet4_adm("Depending on the number of flagstores, more points can be lost from defense than are gained from SLA.", classnames="failure", open=True)
    env.variables["tenet5_saar2024"] = tenet5_adm("The cost of downtime is similar to the cost of defense per round. Patches prevent loss of points over multiple rounds and are thus favorable to not patching.", classnames="success")
    env.variables["tenet6_saar2024"] = tenet6_adm("SLA points awarded from recovering services do not scale with amount of uptime in the *retention period*.", classnames="warning", open=True)
    env.variables["tenet7_saar2024"] = tenet7_adm("SLA points are typically not significantly larger than defense points.", classnames="success")

    env.variables["tenet1_enowars2024"] = tenet1_adm("Attack points scale linearly with the amount of flags captured.", classnames="success")
    env.variables["tenet2_enowars2024"] = tenet2_adm("Defense points scale non-linearly with the amount of flags lost. Beyond the first capture of a flag, the points lost due to defense do not increase.", classnames="failure", open=True)
    env.variables["tenet3_enowars2024"] = tenet3_adm("Flag values scales inversely with the amount of captures.", classnames="success")
    env.variables["tenet4_enowars2024"] = tenet4_adm("Based on the default constants for `ATTACK`, `SLA` and `DEF`, teams receive more SLA points than they lose through defense, but attackers may gain significantly more points than awarded through SLA.", classnames="failure", open=True)
    env.variables["tenet5_enowars2024"] = tenet5_adm("The cost of downtime is similar to the cost of defense per round. Patches prevent loss of points over multiple rounds and are thus favorable to not patching.", classnames="success")
    env.variables["tenet6_enowars2024"] = tenet6_adm("Independent of the amount of flags missing from the *retention period*, the service is awarded the same amount of SLA.", classnames="warning", open=True)
    env.variables["tenet7_enowars2024"] = tenet7_adm("Flag value is scaled to the amount of flagstore per service, not to the total amount of flagstores.", classnames="warning", open=True)

    env.variables["tenet1_ecsc2023"] = tenet1_adm("Attack points scale linearly with the amount of flags captured.", classnames="success")
    env.variables["tenet2_ecsc2023"] = tenet2_adm("Defense points scale non-linearly with the amount of attackers.", classnames="success")
    env.variables["tenet3_ecsc2023"] = tenet3_adm("Flag values scales inversely with the amount of captures.", classnames="success")
    env.variables["tenet4_ecsc2023"] = tenet4_adm("For the given constants, the *attacker's* relative gain will always be less than the points awarded from SLA and `BASE_DEF`.", classnames="success")
    env.variables["tenet5_ecsc2023"] = tenet5_adm("For the given constants, it would take significantly more rounds than the amount spent unavaiable to recover the losses of SLA, which disincentivizes patching.", classnames="failure", open=True)
    env.variables["tenet6_ecsc2023"] = tenet6_adm("SLA does not decrease fairly with the amount of missing flags in the retention period.", classnames="success")
    env.variables["tenet7_ecsc2023"] = tenet7_adm("Flag value is not scaled to the amount of flagstores, and thus independent of flagstore.", classnames="success")

    env.variables["tenet1_ecsc2024"] = tenet1_adm("Attack points scale linearly with the amount of flags captured.", classnames="success")
    env.variables["tenet2_ecsc2024"] = tenet2_adm("Defense points scale linearly with the amount of flags lost", classnames="success")
    env.variables["tenet3_ecsc2024"] = tenet3_adm("Flag values scales with the difference in score between attacker and victim, but not the difficulty of exploiting that specific vulnerability.", classnames="failure", open=True)
    env.variables["tenet4_ecsc2024"] = tenet4_adm("Perfect SLA is worth more than an attacker's gain, since turning off a service would mean a loss of competitiveness, which undermines the purpose of tactically disabling it.", classnames="success")
    env.variables["tenet5_ecsc2024"] = tenet5_adm("Attack points are scaled with SLA points, disincentivizing patching when gains from attacking are high.", classnames="failure", open=True)
    env.variables["tenet6_ecsc2024"] = tenet6_adm("The formula does not feature a retention period, and such the points are divided fairly.", classnames="success")
    env.variables["tenet7_ecsc2024"] = tenet7_adm("Flag value is not scaled to the amount of flagstores, and thus independent of flagstore.", classnames="success")

    env.variables["tenet1_ecsc2025"] = tenet1_adm("Attack points scale linearly with the amount of flags submitted.", classnames="success")
    env.variables["tenet2_ecsc2025"] = tenet2_adm("Defense points are awarded for rounds a team is not exploited, despite another team successfully exploiting that flagstore, proportional to the amount of flags available. Thus teams who have not patched lose more flags the more flagstores and flags from those flagstores are captured (in relation to a patched team).", classnames="success")
    env.variables["tenet3_ecsc2025"] = tenet3_adm("Each flag's value is inversely proportional to the number of captures.", classnames="success")
    env.variables["tenet4_ecsc2025"] = tenet4_adm("An attacker's marginal gain per service per team is `flagstores * base`, the same as the minimum gain for the defender from keeping it alive. Therefore, no points gained from turning off a service, especially not in regards to the other non-attacking players.", classnames="success")
    env.variables["tenet5_ecsc2025"] = tenet5_adm("The cost of downtime due to patching can be recovered in few subsequent rounds through defense points gained (see calculation in review section).", classnames="success")
    env.variables["tenet6_ecsc2025"] = tenet6_adm("Teams only lose SLA and DEF points relative to the amount of rounds each flag has been made unavaiable for.", classnames="success")
    env.variables["tenet7_ecsc2025"] = tenet7_adm("Flag value does not depend on the amount of flagstores in the service.", classnames="success")

    env.variables["tenet1_atklabv1"] = tenet1_adm("Score increases with attack, which scales with flags captured.", classnames="success")
    env.variables["tenet2_atklabv1"] = tenet2_adm("Score decreases with defense, which scales with flags lost.", classnames="success")
    env.variables["tenet3_atklabv1"] = tenet3_adm("A flag's value scales inversely with the number of captures.", classnames="success")
    env.variables["tenet4_atklabv1"] = tenet4_adm("The maximum points gained by any attack (`flagstores * 2`) is less than the minimum cost of downtime (`sla_max = flagstores * 2 + 1`).", classnames="success")
    env.variables["tenet5_atklabv1"] = tenet5_adm("The cost of downtime due to patching can be recovered in few subsequent rounds of prevented exploitation.", classnames="success")
    env.variables["tenet6_atklabv1"] = tenet6_adm("`sla_ratio` decreases fairly with every missing flag in the *validity period*.", classnames="success")
    env.variables["tenet7_atklabv1"] = tenet7_adm("Flag value does not depend on the amount of flagstores in the service.", classnames="success")

    env.variables["tenet1_atklabv2"] = tenet1_adm("Attack points scale linearly with the amount of flags submitted.", classnames="success")
    env.variables["tenet2_atklabv2"] = tenet2_adm("Defense points are awarded for rounds a team is not exploited, despite another team successfully exploiting that flagstore, proportional to the amount of flags available. Thus teams who have not patched lose more flags the more flagstores and flags from those flagstores are captured (in relation to a patched team).", classnames="success")
    env.variables["tenet3_atklabv2"] = tenet3_adm("Each flag's value is inversely proportional to the number of captures.", classnames="success")
    env.variables["tenet4_atklabv2"] = tenet4_adm("An attacker's marginal gain per service per team is `flagstores * base`, the same as the minimum gain for the defender from keeping it alive. Therefore, no points gained from turning off a service, especially not in regards to the other non-attacking players.", classnames="success")
    env.variables["tenet5_atklabv2"] = tenet5_adm("The cost of downtime due to patching can be recovered in few subsequent rounds through defense points gained (see calculation in review section).", classnames="success")
    env.variables["tenet6_atklabv2"] = tenet6_adm("Teams only lose SLA and DEF points relative to the amount of rounds each flag has been made unavaiable for.", classnames="success")
    env.variables["tenet7_atklabv2"] = tenet7_adm("Flag value does not depend on the amount of flagstores in the service.", classnames="success")
