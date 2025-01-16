import joblib

# Load the model once to avoid reloading it multiple times
MODEL_PATH = "./AI_model/model_3_class_classifier_random_forests_3.joblib"

# Load the model during app initialization
model = joblib.load(MODEL_PATH)

def predict_sentiment(text_list):
    # Ensure input is in the expected format (e.g., a list of strings)
    if not isinstance(text_list, list) or not all(isinstance(text, str) for text in text_list):
        raise ValueError("Input must be a list of strings.")

    # Use the loaded model to predict
    predictions = model.predict(text_list)

    # Convert predictions to a list
    return predictions.tolist()