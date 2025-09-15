# medical_data.py
# Sample data for medical_tools

ADVICE=(
        "This is demo triage only, not a diagnosis. "
        "If symptoms are severe (chest pain, trouble breathing, etc.) seek emergency care."
    )

SAMPLE_LAB_REFERENCES = {
    "CBC": {"WBC": "4.5-11 x10^9/L", "Hb": "13.5-17.5 g/dL (M)"},
    "LFT": {"ALT": "7-56 U/L", "AST": "10-40 U/L"},
    "KFT": {"Urea": "15-40 mg/dL", "Creatinine": "0.6-1.2 mg/dL"},
    "TSH": {"TSH": "0.4-4.0 mIU/L"},
    "LIPID": {"Total Cholesterol": "<200 mg/dL", "LDL": "<100 mg/dL", "HDL": ">40 mg/dL"},
    "BLOOD SUGAR": {"Fasting": "70-99 mg/dL", "PP": "<140 mg/dL"},
    "URINE": {"pH": "4.6-8.0", "Protein": "Negative"},
}

SAMPLE_SYMPTOM_CONDITIONS = {
    "cough": [
        {"condition": "Common cold", "prob": "possible"},
        {"condition": "Bronchitis", "prob": "possible"},
        {"condition": "Asthma", "prob": "possible"},
        {"condition": "COVID-19", "prob": "possible"},
    ],
    "fever": [
        {"condition": "Influenza", "prob": "possible"},
        {"condition": "COVID-19", "prob": "possible"},
        {"condition": "Malaria", "prob": "possible"},
        {"condition": "Dengue", "prob": "possible"},
    ],
    "headache": [
        {"condition": "Migraine", "prob": "possible"},
        {"condition": "Tension headache", "prob": "possible"},
        {"condition": "Sinusitis", "prob": "possible"},
        {"condition": "Common cold", "prob": "possible"},
    ],
    "runny nose": [
        {"condition": "Allergic rhinitis", "prob": "possible"},
        {"condition": "Common cold", "prob": "possible"},
        {"condition": "Sinusitis", "prob": "possible"},
    ],
    "stomach pain": [
        {"condition": "Gastritis", "prob": "possible"},
        {"condition": "Appendicitis", "prob": "possible"},
        {"condition": "Food poisoning", "prob": "possible"},
    ],
    "fatigue": [
        {"condition": "Anemia", "prob": "possible"},
        {"condition": "Hypothyroidism", "prob": "possible"},
        {"condition": "Diabetes", "prob": "possible"},
    ],
    "chest pain": [
        {"condition": "Heart attack", "prob": "possible"},
        {"condition": "Angina", "prob": "possible"},
        {"condition": "Anxiety", "prob": "possible"},
    ],
    "shortness of breath": [
        {"condition": "Asthma", "prob": "possible"},
        {"condition": "COPD", "prob": "possible"},
        {"condition": "Heart failure", "prob": "possible"},
    ],
    "rash": [
        {"condition": "Allergic reaction", "prob": "possible"},
        {"condition": "Measles", "prob": "possible"},
        {"condition": "Chickenpox", "prob": "possible"},
    ],
    "joint pain": [
        {"condition": "Arthritis", "prob": "possible"},
        {"condition": "Dengue", "prob": "possible"},
        {"condition": "Lupus", "prob": "possible"},
    ],
}
