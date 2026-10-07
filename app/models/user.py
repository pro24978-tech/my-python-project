from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    api_token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    profile = db.Column(db.JSON, nullable=False, default=dict)

    # Связи с твитами, подписками, лайками
    tweets = db.relationship("Tweet", back_populates="author", lazy="dynamic")

    # Подписки (followers – кто подписан на этого пользователя,
    #           following – на кого подписан этот пользователь)
    followers = db.relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        lazy="dynamic"
    )
    following = db.relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        lazy="dynamic"
    )

    # Лайки пользователя
    likes = db.relationship("Like", back_populates="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.name}>"