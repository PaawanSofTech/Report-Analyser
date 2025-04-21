import json
import uuid
from datetime import datetime

def save_to_json(text, age, gender, output_path="report.json"):
    report_data = {
        "report_id": str(uuid.uuid4()),
        "patient_age": age,
        "patient_gender": gender,
        "report_text": text,
        "timestamp": datetime.now().isoformat()
    }
    with open(output_path, "w") as f:
        json.dump(report_data, f, indent=4)
    return output_path
