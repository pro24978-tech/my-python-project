from app.extensions import db

class Like(db.Model):
    """Модель лайка (кто лайкнул какой твит)."""
    __tablename__ = "likes"

    # Составной первичный ключ (пользователь + твит)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweets.id"), primary_key=True)

    # Связи с пользователем и твитом
    user = db.relationship("User", back_populates="likes")
    tweet = db.relationship("Tweet", back_populates="likes")

    def __repr__(self):
        return f"<Like user {self.user_id} -> tweet {self.tweet_id}>"