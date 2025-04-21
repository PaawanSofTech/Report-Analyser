import joblib

# Load your pre-trained model
model = joblib.load("cardiac_disease_model.pkl")

# Function to predict cardiac risk
def predict_cardiac_risk(features):
    preprocessed_features = preprocess_data(features)
    prediction = model.predict(preprocessed_features)
    return prediction
