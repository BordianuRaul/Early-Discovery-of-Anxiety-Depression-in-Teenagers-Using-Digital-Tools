import joblib

# Load the model once to avoid reloading it multiple times
MODEL_PATH = "./AI_model/model_3_class_classifier_random_forests2.joblib"

# Load the model during app initialization
model = joblib.load(MODEL_PATH)


"""
    Predicts sentiments for a list of strings.
    Args:
        text_list (list): List of strings to classify.
    Returns:
        list: Predicted sentiments (0 = Depression, 1 = Anxiety, 2 = Normal).
    """
def predict_sentiment(text_list):
    # Ensure input is in the expected format (e.g., a list of strings)
    if not isinstance(text_list, list) or not all(isinstance(text, str) for text in text_list):
        raise ValueError("Input must be a list of strings.")

    # Use the loaded model to predict
    predictions = model.predict(text_list)

    # Convert predictions to a list
    return predictions.tolist()