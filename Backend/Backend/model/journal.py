class Journal:
    def __init__(self, user_id: int, content: str, sentiment_score: float = 0.0):
        self.user_id = user_id
        self.content = content
        self.sentiment_score = sentiment_score