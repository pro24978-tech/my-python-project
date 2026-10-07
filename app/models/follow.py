from app.extensions import db

class Follow(db.Model):
    """Модель подписки (кто на кого подписан)."""
    __tablename__ = "follows"

    # Составной первичный ключ (обе колонки вместе уникальны)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    following_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    # Связи с пользователями:
    # follower – кто подписывается
    # following – на кого подписываются
    follower = db.relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following"  # у пользователя будет список тех, на кого он подписан
    )
    following = db.relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="followers"  # у пользователя будет список его подписчиков
    )

    def __repr__(self):
        return f"<Follow {self.follower_id} -> {self.following_id}>"