from datetime import datetime
from app.extensions import db

class Tweet(db.Model):
    """Модель твита (сообщения пользователя)."""
    __tablename__ = "tweets"  # Имя таблицы в БД

    # Первичный ключ
    id = db.Column(db.Integer, primary_key=True)

    # Внешний ключ к таблице users (автор твита)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Текст твита (обязательное поле)
    content = db.Column(db.Text, nullable=False)

    # Дата и время создания (автоматически проставляется при вставке)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с моделью User (обратная ссылка – author.tweets)
    author = db.relationship("User", back_populates="tweets")

    # Связи с медиа и лайками (будут добавлены позже)
    media = db.relationship("Media", back_populates="tweet", lazy="dynamic")
    likes = db.relationship("Like", back_populates="tweet", lazy="dynamic")

    def __repr__(self):
        return f"<Tweet {self.id} by user {self.author_id}>"