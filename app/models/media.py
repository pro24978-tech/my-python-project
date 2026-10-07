from app.extensions import db

class Media(db.Model):
    """Модель загруженного медиа-файла (картинки)."""
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)

    # Внешний ключ к твиту (может быть NULL, если файл загружен, но твит ещё не создан)
    tweet_id = db.Column(db.Integer, db.ForeignKey("tweets.id"), nullable=True)

    # Относительный путь к файлу (например, "uploads/abc123.jpg")
    file_path = db.Column(db.String(255), nullable=False)

    # Связь с твитом (обратная ссылка – tweet.media)
    tweet = db.relationship("Tweet", back_populates="media")

    def __repr__(self):
        return f"<Media {self.id} for tweet {self.tweet_id}>"