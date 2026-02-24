TriAgent-S
Agentic Clinical Triage Framework

TriAgent-S is a governance-aware clinical triage system built on MedGemma 4B and deployed on DGX A100 (20GB MIG slice).
It combines foundation model reasoning with deterministic safety controls and longitudinal patient monitoring.

Overview

Rather than producing a single diagnosis, TriAgent-S structures triage as a decision pathway.

The system:

Generates calibrated disease likelihood distributions

Computes a deterministic severity index from vital signs

Applies shock override escalation independent of model output

Maintains longitudinal visit memory

Visualizes severity trends across encounters

Routes patients into P1 / P2 / P3 triage levels

This architecture prioritizes safe escalation under uncertainty rather than autonomous diagnosis.

Core Architecture

The system follows an agentic design where MedGemma acts as a reasoning component inside a policy-constrained framework.

Key modules:

model_backend.py → MedGemma inference layer

scoring_engine.py → Deterministic severity index computation

rule_engine.py → Shock detection & escalation rules

controller.py → Probability–severity fusion and triage routing

patient_database.py → Longitudinal visit memory

streamlit_app.py → Clinical interface

Deployment

Tested on:

DGX A100

20GB MIG slice

4-bit quantized MedGemma 4B

Designed for hospital-controlled infrastructure and privacy-preserving inference.

Features

Multimodal symptom + vitals input

Calibrated disease probability distribution

Severity-based escalation logic

Longitudinal severity trend graph

Structured physician routing

On-prem GPU deployment

Disclaimer

This project is exploratory and educational.
It is not a medical device and does not provide medical advice.
