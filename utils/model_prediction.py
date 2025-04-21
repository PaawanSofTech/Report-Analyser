import joblib
from utils.feature_extraction import extract_important_features
from utils.preprocessing import preprocess_features
from utils.preprocessing import preprocess_features


# Load the pre-trained model using joblib
def load_model():
    model = joblib.load('../model/cardiac_disease_model.pkl')  # Path to your pre-trained model
    return model

# Function to predict cardiac risk based on the extracted features
def predict_cardiac_risk(report_text):
    # Step 1: Extract important features from the report text
    features = extract_important_features(report_text)
    
    # Step 2: Preprocess the extracted features for the model
    processed_features = preprocess_features(features)
    
    # Step 3: Load the model and make a prediction
    model = load_model()
    prediction = model.predict(processed_features)
    
    # Return the prediction result
    return prediction
