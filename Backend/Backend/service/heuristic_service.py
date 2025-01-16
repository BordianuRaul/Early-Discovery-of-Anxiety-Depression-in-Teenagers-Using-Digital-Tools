def calculate_heuristic_score(predictions):
    """
    Calculate the heuristic score based on predictions.

    Args:
        predictions (list): List of sentiment predictions as integers or strings.

    Returns:
        dict: Heuristic score and emotional state.
    """
    # Scoring weights for each sentiment
    weight_map = {
        0: -2,  # anxiety
        1: -3, # depression
        2: 1  # normal
    }

    # Calculate the total score
    score = sum(weight_map.get(pred, 0) for pred in predictions)

    # Determine the emotional state
    if score > 3:
        emotional_state = 'normal'
    elif -3 <= score <= 3:
        emotional_state = 'anxiety'
    else:
        emotional_state = 'depression'

    print("Score is: {}".format(score))

    return {
        'score': score,
        'emotional_state': emotional_state
    }
