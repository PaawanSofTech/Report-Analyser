import json
import re

# Function to parse the extracted text into a structured dictionary
def parse_text_to_json(text):
    # Example: Let's assume the report contains patient info in a regular format
    parsed_data = {}

    # Extract Patient ID (Example format: "Patient ID: 12345")
    patient_id_match = re.search(r"Patient ID:\s*(\d+)", text)
    if patient_id_match:
        parsed_data['patient_id'] = patient_id_match.group(1)

    # Extract Name (Example format: "Name: John Doe")
    name_match = re.search(r"Name:\s*([\w\s]+)", text)
    if name_match:
        parsed_data['name'] = name_match.group(1)

    # Extract Age (Example format: "Age: 45")
    age_match = re.search(r"Age:\s*(\d+)", text)
    if age_match:
        parsed_data['age'] = int(age_match.group(1))

    # Extract Diagnosis (Example format: "Diagnosis: Cardiac Arrest")
    diagnosis_match = re.search(r"Diagnosis:\s*([\w\s]+)", text)
    if diagnosis_match:
        parsed_data['diagnosis'] = diagnosis_match.group(1)

    # Extract Symptoms (Example format: "Symptoms: Chest pain, shortness of breath")
    symptoms_match = re.search(r"Symptoms:\s*([\w\s,]+)", text)
    if symptoms_match:
        parsed_data['symptoms'] = symptoms_match.group(1).split(", ")

    # Extract Date of report (Example format: "Report Date: 2025-04-20")
    date_match = re.search(r"Report Date:\s*(\d{4}-\d{2}-\d{2})", text)
    if date_match:
        parsed_data['report_date'] = date_match.group(1)

    # You can add more fields as needed

    return parsed_data

# Function to save the structured data to a JSON file
def save_to_json(parsed_data, filename="report_data.json"):
    with open(filename, 'w') as json_file:
        json.dump(parsed_data, json_file, indent=4)

