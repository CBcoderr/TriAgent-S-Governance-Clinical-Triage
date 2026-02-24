def icu_recommendation(triage):

    if "P1" in triage:
        return "Immediate ICU admission and specialist intervention"

    elif "P2" in triage:
        return "Urgent monitoring and inpatient admission"

    else:
        return "Outpatient care and monitoring"
