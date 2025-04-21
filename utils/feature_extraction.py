import re

# Function to extract age from the report
def extract_age(report_text):
    age_pattern = r"AGE\s*[:\-]?\s*(\d+)\s*(?:Yrs|Years)"
    match = re.search(age_pattern, report_text)
    if match:
        return int(match.group(1))
    return None

# Function to extract glucose level
def extract_glucose(report_text):
    glucose_pattern = r"GLUCOSE\s*([\d\.]+)\s*(mg/dL)"
    match = re.search(glucose_pattern, report_text)
    if match:
        return float(match.group(1))
    return None

# Function to extract creatinine level
def extract_creatinine(report_text):
    creatinine_pattern = r"CREATININE\s*([\d\.]+)\s*(mg/dL)"
    match = re.search(creatinine_pattern, report_text)
    if match:
        return float(match.group(1))
    return None

# Function to extract sodium level
def extract_sodium(report_text):
    sodium_pattern = r"SODIUM\s*([\d\.]+)\s*(mmol/L)"
    match = re.search(sodium_pattern, report_text)
    if match:
        return float(match.group(1))
    return None

# Function to extract potassium level
def extract_potassium(report_text):
    potassium_pattern = r"POTASSIUM\s*([\d\.]+)\s*(mmol/L)"
    match = re.search(potassium_pattern, report_text)
    if match:
        return float(match.group(1))
    return None

# Function to extract liver function tests (e.g., ALT, AST)
def extract_liver_function_tests(report_text):
    alt_pattern = r"\(SGPT\-ALT\)\s*ALANINE\s*AMINO\s*TRANSFERASE\s*([\d\.]+)\s*(U/L)"
    ast_pattern = r"\(SGOT\-AST\)\s*ASPARTATE\s*AMINO\s*TRANSFERASE\s*([\d\.]+)\s*(U/L)"
    bilirubin_pattern = r"BILIRUBIN\-TOTAL\s*([\d\.]+)\s*(mg/dL)"
    
    alt = re.search(alt_pattern, report_text)
    ast = re.search(ast_pattern, report_text)
    bilirubin = re.search(bilirubin_pattern, report_text)
    
    return {
        "ALT": float(alt.group(1)) if alt else None,
        "AST": float(ast.group(1)) if ast else None,
        "Bilirubin": float(bilirubin.group(1)) if bilirubin else None
    }
# In utils/feature_extraction.py
def extract_important_features(report_text):
    # Logic to extract important features from the report
    features = some_processing_logic(report_text)
    return features

# Combine all extractions into a dictionary
def extract_features_from_report(report_text):
    features = {}
    features['age'] = extract_age(report_text)
    features['glucose'] = extract_glucose(report_text)
    features['creatinine'] = extract_creatinine(report_text)
    features['sodium'] = extract_sodium(report_text)
    features['potassium'] = extract_potassium(report_text)
    liver_tests = extract_liver_function_tests(report_text)
    features.update(liver_tests)
    return features
