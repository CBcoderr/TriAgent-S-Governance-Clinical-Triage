from hospital_ai.controller import HospitalAgentController

if __name__ == "__main__":
    controller = HospitalAgentController()

    # Example CLI test
    reasoning, result = controller.run_agent(
        patient_id="001",
        patient_name="Test Patient",
        symptoms="Mild fever and cough",
        labs="SpO2 97 HR 88",
        ecg_id=None,
        image_path=None
    )

    print("\n".join(reasoning))
    print("\nFINAL RESULT:\n")
    print(result)