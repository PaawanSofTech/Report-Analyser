import re
import numpy as np
import pickle
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Load the models
random_forest_model = pickle.load(open('random_forest_model.pkl', 'rb'))
simple_imputer = pickle.load(open('simple_imputer.pkl', 'rb'))

# Extracting age from the report
def extract_age(report_text):
    age_pattern = r"AGE\s*[:\-]?\s*(\d+)\s*(?:Yrs|Years)"
    match = re.search(age_pattern, report_text)
    return int(match.group(1)) if match else None

# Function to extract glucose level
def extract_glucose(report_text):
    glucose_pattern = r"GLUCOSE\s*([\d\.]+)\s*(mg/dL)"
    match = re.search(glucose_pattern, report_text)
    return float(match.group(1)) if match else None

# Function to extract creatinine level
def extract_creatinine(report_text):
    creatinine_pattern = r"CREATININE\s*([\d\.]+)\s*(mg/dL)"
    match = re.search(creatinine_pattern, report_text)
    return float(match.group(1)) if match else None

# Function to extract sodium level
def extract_sodium(report_text):
    sodium_pattern = r"SODIUM\s*([\d\.]+)\s*(mmol/L)"
    match = re.search(sodium_pattern, report_text)
    return float(match.group(1)) if match else None

# Function to extract potassium level
def extract_potassium(report_text):
    potassium_pattern = r"POTASSIUM\s*([\d\.]+)\s*(mmol/L)"
    match = re.search(potassium_pattern, report_text)
    return float(match.group(1)) if match else None

# Extract liver function tests (ALT, AST)
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

# Function to combine all feature extractions into a dictionary
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

# Function to predict disease using the extracted features
def process_and_predict(report_text):
    # Extract features
    extracted_features = extract_features_from_report(report_text)
    
    # Convert to numpy array for model input
    features_array = np.array(list(extracted_features.values())).reshape(1, -1)
    
    # Handle missing values using SimpleImputer
    features_array_imputed = simple_imputer.transform(features_array)
    
    # Prediction
    prediction = random_forest_model.predict(features_array_imputed)
    return prediction[0]
