from hospital_ai.model_backend import ModelBackend
from hospital_ai.scoring_engine import compute_severity
from hospital_ai.rule_engine import determine_triage
from hospital_ai.resource_engine import icu_recommendation
from hospital_ai.patient_database import update_patient


class AgentController:

    def __init__(self):
        self.model = ModelBackend()

    # ----------------------------------------
    # Deterministic Risk Logic (Symptoms Only)
    # ----------------------------------------
    def calculate_risk(self, symptoms):

        risk = 20
        text = symptoms.lower()

        # Respiratory distress
        if "shortness of breath" in text:
            risk += 25

        if "oxygen 84" in text or "spo2 84" in text:
            risk += 35

        # Neurological red flags
        if "confusion" in text:
            risk += 25

        if "unconscious" in text:
            risk += 35

        # Hemodynamic instability
        if "hypotension" in text or "bp 80" in text:
            risk += 30

        # Cardiac
        if "chest pain" in text:
            risk += 20

        # Severe fever mention
        if "high fever" in text:
            risk += 15

        return min(risk, 100)

    # ----------------------------------------
    # Disease Probability Logic
    # ----------------------------------------
    def compute_disease_distribution(self, symptoms):

        text = symptoms.lower()

        probs = {
            "Dengue": 10,
            "Malaria": 10,
            "Pneumonia": 20,
            "Sepsis": 10,
            "Tuberculosis": 10
        }

        # Respiratory bias
        if "cough" in text or "shortness of breath" in text:
            probs["Pneumonia"] += 30

        # Neurological/sepsis bias
        if "confusion" in text:
            probs["Sepsis"] += 20

        # Chronic cough bias
        if "weight loss" in text:
            probs["Tuberculosis"] += 20

        total = sum(probs.values())

        # Normalize to 100
        for k in probs:
            probs[k] = int((probs[k] / total) * 100)

        return probs

    # ----------------------------------------
    # Main Agent
    # ----------------------------------------
    def run_agent(
        self,
        patient_id,
        patient_name,
        symptoms,
        lab_report=None,
        ecg=None,
        xray=None
    ):

        images = []

        if lab_report is not None:
            images.append(lab_report)

        if ecg is not None:
            images.append(ecg)

        if xray is not None:
            images.append(xray)

        # LLM used only for reasoning text
        prompt = f"""
Provide concise clinical reasoning for the following case.

Patient ID: {patient_id}
Patient Name: {patient_name}

Symptoms:
{symptoms}

Be medically realistic and brief.
"""

        reasoning = self.model.generate(prompt, images)

        # Deterministic triage pipeline
        risk_score = self.calculate_risk(symptoms)
        severity = compute_severity(risk_score)
        triage = determine_triage(severity)
        action = icu_recommendation(triage)
        disease_probs = self.compute_disease_distribution(symptoms)

        # Update patient history
        trend = update_patient(patient_id, patient_name, severity)

        return {
            "triage": triage,
            "probable_condition": max(disease_probs, key=disease_probs.get),
            "clinical_reasoning": reasoning,
            "recommended_action": action,
            "severity_score": severity,
            "risk_score": risk_score,
            "disease_probabilities": disease_probs,
            "trend": trend,
            "explainability": [
                "Risk score calculated from symptom-based severity rules.",
                "Disease probabilities derived from weighted symptom mapping.",
                "Multimodal inputs (Lab/ECG/X-ray) available to model for reasoning."
            ]
        }
