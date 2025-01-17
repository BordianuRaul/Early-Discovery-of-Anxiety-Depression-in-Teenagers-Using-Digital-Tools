def calculate_heuristic_score(predictions, journal_scores=None):
    """
    Calculate the heuristic score based on predictions and journal sentiment scores.

    Args:
        predictions (list): List of sentiment predictions as integers or strings.
        journal_scores (list, optional): List of sentiment scores from journals as floats.

    Returns:
        dict: Heuristic score and emotional state.
    """
    # Scoring weights for each sentiment prediction
    weight_map = {
        0: -2,  # anxiety
        1: -3,  # depression
        2: 1    # normal
    }

    # Calculate the total score from predictions
    prediction_score = sum(weight_map.get(pred, 0) for pred in predictions)

    # Scale journal scores with a smaller weight to reduce their impact
    if journal_scores:
        scaled_journal_scores = [score * 2 for score in journal_scores]
        journal_score = sum(scaled_journal_scores)
    else:
        journal_score = 0

    total_score = prediction_score + journal_score

    # Adjust score thresholds for larger intervals
    if total_score > 5:  # Expanded interval for 'normal'
        emotional_state = 'normal'
    elif -5 <= total_score <= 5:  # Expanded interval for 'anxiety'
        emotional_state = 'anxiety'
    else:  # Only extreme negative scores lead to 'depression'
        emotional_state = 'depression'

    print("Prediction Score: {}".format(prediction_score))
    print("Journal Score: {}".format(journal_score))
    print("Total Score: {}".format(total_score))

    return {
        'score': total_score,
        'emotional_state': emotional_state
    }
