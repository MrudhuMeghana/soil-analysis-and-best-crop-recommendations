from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the model and scaler
model = joblib.load("crop_recommendation_model.pkl")
scaler = joblib.load("scaler.pkl")

# Crop mapping dictionary
crop_mapping = {
    1: 'rice',
    2: 'maize',
    3: 'jute',
    4: 'cotton',
    5: 'coconut',
    6: 'papaya',
    7: 'orange',
    8: 'apple',
    9: 'muskmelon',
    10: 'watermelon',
    11: 'grapes',
    12: 'mango',
    13: 'banana',
    14: 'pomegranate',
    15: 'lentil',
    16: 'blackgram',
    17: 'mungbean',
    18: 'mothbeans',
    19: 'pigeonpeas',
    20: 'kidneybeans',
    21: 'chickpea',
    22: 'coffee'
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from the form
        data = request.json
        input_features = [
            float(data["N"]),
            float(data["P"]),
            float(data["K"]),
            float(data["temperature"]),
            float(data["humidity"]),
            float(data["ph"]),
            float(data["rainfall"])
        ]

        # Scale the input features
        input_scaled = scaler.transform([input_features])

        # Get probabilities for all crops
        crop_probabilities = model.predict_proba(input_scaled)[0]

        # Get the top 3 crops with the highest probabilities
        top_3_indices = np.argsort(crop_probabilities)[-3:][::-1]
        top_3_crops = model.classes_[top_3_indices]
        top_3_probs = crop_probabilities[top_3_indices]

        # Map numerical labels to crop names
        recommendations = [
            {"crop": crop_mapping.get(crop, f"Unknown Crop {crop}"), "probability": round(prob * 100, 2)}
            for crop, prob in zip(top_3_crops, top_3_probs)
        ]

        return jsonify({"success": True, "recommendations": recommendations})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    
@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        feedback_data = request.json
        feedback_text = feedback_data.get("feedback")

        # Save feedback to a file
        with open("feedback.txt", "a") as f:
            f.write(feedback_text + "\n")

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)