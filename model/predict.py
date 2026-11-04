import joblib
import pandas as pd
from pathlib import Path

MODEL_VERSION = "1.0.0"
model_path = Path(__file__).parent / 'xgb_model.joblib'
threshold_path = Path(__file__).parent / 'best_threshold'
if not threshold_path.exists():
    threshold_path = Path(__file__).parent / 'best_threshold.joblib'

model = joblib.load(model_path)
threshold = joblib.load(threshold_path)


def predict(data):
    try:
        # Convert the input data to a DataFrame
        input_data = pd.DataFrame(data)
        
        # Make predictions using the loaded model
        probability = model.predict_proba(input_data)[:, 1][0]  # Get the probability of the positive class
        prediction = int(probability >= threshold)  # Apply the threshold to get the binary prediction
        
        # Return the prediction and probability
        return {
            'default_probability': probability,
            'default_prediction': prediction,
            'threshold': threshold,
            'Result': "High Risk" if prediction == 1 else "Low Risk"
        }
    except Exception as e:
        raise ValueError(f"Error during prediction: {e}")