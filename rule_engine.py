def determine_triage(severity):

    if severity >= 80:
        return "P1 - Critical"

    elif severity >= 50:
        return "P2 - Urgent"

    else:
        return "P3 - Stable"
