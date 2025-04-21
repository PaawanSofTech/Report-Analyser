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

# Function to extract AST (Aspartate Aminotransferase) level
def extract_ast(report_text):
    ast_pattern = r"\(SGOT\-AST\)\s*ASPARTATE\s*AMINO\s*TRANSFERASE\s*([\d\.]+)\s*(U/L)"
    match = re.search(ast_pattern, report_text)
    if match:
        return float(match.group(1))
    return None

# Function to extract ALT (Alanine Aminotransferase) level
def extract_alt(report_text):
    alt_pattern = r"\(SGPT\-ALT\)\s*ALANINE\s*AMINO\s*TRANSFERASE\s*([\d\.]+)\s*(U/L)"
    match = re.search(alt_pattern, report_text)
    if match:
        return float(match.group(1))
    return None

# Function to extract bilirubin (total) level
def extract_bilirubin(report_text):
    bilirubin_pattern = r"BILIRUBIN\-TOTAL\s*([\d\.]+)\s*(mg/dL)"
    match = re.search(bilirubin_pattern, report_text)
    if match:
        return float(match.group(1))
    return None

# Function to extract liver function test (e.g., ALT, AST)
def extract_liver_function_tests(report_text):
    alt = extract_alt(report_text)
    ast = extract_ast(report_text)
    bilirubin = extract_bilirubin(report_text)
    return {
        "ALT": alt,
        "AST": ast,
        "Bilirubin": bilirubin
    }

# Combine all extractions
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
