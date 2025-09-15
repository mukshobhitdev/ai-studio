from agents import function_tool
from data.medical_data import SAMPLE_SYMPTOM_CONDITIONS, SAMPLE_LAB_REFERENCES, ADVICE

@function_tool
def symptom_checker(symptoms: str) -> dict:
    symptoms_lower = symptoms.lower()
    possible = None
    for key in SAMPLE_SYMPTOM_CONDITIONS:
        if key in symptoms_lower:
            possible = SAMPLE_SYMPTOM_CONDITIONS[key]
            break
    if not possible:
        possible = [{"condition": "Sorry, I have no information available for possible conditions for this", "prob": "unknown"}]
    return {"symptoms": symptoms, "possible_conditions": possible, "disclaimer": ADVICE}

@function_tool
def lab_reference(test_name: str) -> dict:
    return {"test": test_name, "reference": SAMPLE_LAB_REFERENCES.get(test_name.upper(), "Not found in sample records")}
