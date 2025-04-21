import joblib
import json

# Load trained components
model = joblib.load('random_forest_model.pkl')
tfidf = joblib.load('tfidf_ext')
imputer = joblib.load('simple_imputer.pkl')

def predict_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    text_vector = tfidf.transform([data['report_text']])
    prediction = model.predict(text_vector)

    # Append prediction to JSON
    data["predicted_disease"] = prediction[0]

    return data
