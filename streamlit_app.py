import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from hospital_ai.controller import AgentController
from hospital_ai.patient_database import get_patient

st.set_page_config(layout="wide")
st.title("Multimodal Clinical Decision Support System")

controller = AgentController()

st.subheader("Patient Information")

col1, col2 = st.columns(2)

with col1:
    patient_id = st.text_input("Patient ID")

    existing = get_patient(patient_id) if patient_id else None

    if existing:
        st.success("Existing patient detected.")
        patient_name = st.text_input("Patient Name", value=existing["name"])
    else:
        patient_name = st.text_input("Patient Name")

with col2:
    st.write("")  # spacer for symmetry

# -------------------------
# Symptoms
# -------------------------

symptoms = st.text_area("Patient Symptoms", height=180)

# -------------------------
# Upload Sections
# -------------------------

st.subheader("Upload Clinical Data (Optional)")

lab_report = st.file_uploader(
    "Upload Lab Report",
    type=["png", "jpg", "jpeg", "pdf"],
    key="lab"
)

ecg = st.file_uploader(
    "Upload ECG",
    type=["png", "jpg", "jpeg"],
    key="ecg"
)

xray = st.file_uploader(
    "Upload X-ray",
    type=["png", "jpg", "jpeg"],
    key="xray"
)

# -------------------------
# Run Agent
# -------------------------

if st.button("Run AI Agent"):

    if not patient_id or not patient_name or not symptoms:
        st.error("Please fill all required fields.")
    else:

        with st.spinner("AI analyzing patient data..."):

            result = controller.run_agent(
                patient_id,
                patient_name,
                symptoms,
                lab_report,
                ecg,
                xray
            )

        st.success("Analysis Complete")

        st.subheader("Triage Level")
        st.write(result["triage"])

        st.subheader("Probable Condition")
        st.write(result["probable_condition"])

        st.subheader("Clinical Reasoning")
        st.write(result["clinical_reasoning"])

        st.subheader("Recommended Action")
        st.write(result["recommended_action"])

        # Severity Gauge
        st.subheader("Clinical Severity Score")

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["severity_score"],
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 40], "color": "green"},
                    {"range": [40, 70], "color": "orange"},
                    {"range": [70, 100], "color": "red"},
                ],
            },
        ))

        st.plotly_chart(gauge, use_container_width=True)

        # Disease Probability
        st.subheader("Disease Probability Distribution")

        diseases = result["disease_probabilities"]

        bar = px.bar(
            x=list(diseases.keys()),
            y=list(diseases.values()),
            labels={"x": "Disease", "y": "Probability (%)"}
        )

        st.plotly_chart(bar, use_container_width=True)

        # Trend
        st.subheader("Patient Severity Trend")

        trend = result["trend"]

        line = px.line(
            x=list(range(1, len(trend) + 1)),
            y=trend,
            labels={"x": "Visit Number", "y": "Severity Score"}
        )

        st.plotly_chart(line, use_container_width=True)

        # Explainability
        st.subheader("Explainability")

        for item in result["explainability"]:
            st.write("•", item)
