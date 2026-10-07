import os
import sys
sys.path.append(os.path.dirname(__file__))

from app.extensions import db
from app.models.user import User
from app.config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def seed_users():
    with app.app_context():
        if User.query.first() is not None:
            print("Пользователи уже есть в БД. Пропускаем.")
            return

        users = [
            {
                "name": "Alice",
                "api_token": "alice_token_123",
                "profile": {
                    "pic": "https://i.pravatar.cc/150?img=1",
                    "nickname": "alice_wonder",
                    "description": "I love microblogging!"
                }
            },
            {
                "name": "Bob",
                "api_token": "bob_token_456",
                "profile": {
                    "pic": "https://i.pravatar.cc/150?img=2",
                    "nickname": "bob_builder",
                    "description": "Building stuff."
                }
            },
            {
                "name": "Charlie",
                "api_token": "charlie_token_789",
                "profile": {
                    "pic": "https://i.pravatar.cc/150?img=3",
                    "nickname": "charlie_brown",
                    "description": "Peanuts fan."
                }
            }
        ]

        for user_data in users:
            user = User(
                name=user_data["name"],
                api_token=user_data["api_token"],
                profile=user_data["profile"]
            )
            db.session.add(user)

        db.session.commit()
        print(f"Добавлено {len(users)} пользователей.")

if __name__ == "__main__":
    seed_users()