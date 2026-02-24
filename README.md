# TriAgent-S  
### Agentic Clinical Triage Framework

TriAgent-S is a governance-aware clinical triage system built on **MedGemma 4B** and deployed on **DGX A100 (20GB MIG slice)**.

It integrates foundation model reasoning with deterministic safety controls, calibrated probability modeling, and longitudinal patient monitoring.

---

## Overview

Rather than producing a single diagnosis, TriAgent-S structures triage as a **decision pathway**.

The system:

- Generates calibrated disease likelihood distributions  
- Computes a deterministic severity index from vital signs  
- Applies shock override escalation independent of model output  
- Maintains longitudinal visit memory  
- Visualizes severity trends across encounters  
- Routes patients into **P1 / P2 / P3** triage levels  

This architecture prioritizes safe escalation under uncertainty rather than autonomous diagnosis.

---

## Core Architecture

TriAgent-S follows an **agentic design** in which MedGemma functions as a reasoning component inside a policy-constrained framework.

The model does not operate independently. Instead, it is embedded within:

- Deterministic rule enforcement  
- Severity scoring logic  
- Calibrated probability fusion  
- State persistence across visits  
- Conditional escalation routing  

---

## Project Structure

The system is modular to clearly separate reasoning, policy enforcement, state management, and interface layers.

```
TriAgent-S/
│
├── main.py                  # Application entry point
├── streamlit_app.py         # Clinical UI (frontend)
│
├── model_backend.py         # MedGemma loading & inference
├── controller.py            # Orchestrates full triage pipeline
├── scoring_engine.py        # Deterministic severity index
├── rule_engine.py           # Shock detection & escalation rules
├── resource_engine.py       # Triage level assignment logic
├── patient_database.py      # Longitudinal visit memory
├── tools.py                 # OCR & utility functions
│
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Execution Flow

The system operates in the following sequence:

1. **Patient Input**
   - Symptom text
   - Structured vital signs
   - Optional medical imaging
   - Previous visit history (if available)

2. **Preprocessing**
   - OCR extraction (if needed)
   - Structured data parsing
   - Shock criteria pre-check

3. **MedGemma Inference**
   - Generates disease likelihood distribution
   - Produces structured reasoning output

4. **Deterministic Severity Scoring**
   - Computes severity index from vitals
   - Independent of model probabilities

5. **Rule Engine**
   - Shock override escalation
   - Safety threshold enforcement

6. **Fusion & Routing**
   - Probability–severity integration
   - Assignment to P1 / P2 / P3 triage level

7. **Longitudinal Memory Update**
   - Stores visit state
   - Updates severity trend graph

8. **Physician Decision Interface**
   - Structured output
   - Escalation recommendations

---

## Deployment

**Tested on:**

- DGX A100  
- 20GB MIG slice  
- 4-bit quantized MedGemma 4B  

Designed for hospital-controlled infrastructure and privacy-preserving inference.

The system does not rely on external cloud APIs.

---

## Features

- Multimodal symptom + vitals intake  
- Calibrated disease probability distribution  
- Deterministic severity index  
- Shock override logic  
- Longitudinal severity trend visualization  
- Structured triage routing (P1 / P2 / P3)  
- On-prem GPU deployment  

---

## Setup

### Python Version
Python 3.10+ recommended.

### Install Dependencies

```
pip install -r requirements.txt
```

If using Tesseract OCR on Windows, set:

```
TESSERACT_PATH="C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## Disclaimer

This project is exploratory and educational.  
It is not a medical device and does not provide medical advice.
