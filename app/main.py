import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from app.config import Config
from app.extensions import db
from app.utils.errors import register_error_handlers


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    register_error_handlers(app)

    # ----- Раздача загруженных файлов -----
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        upload_dir = app.config.get("UPLOAD_FOLDER", "app/static/uploads")
        return send_from_directory(upload_dir, filename)

    # ----- Регистрация blueprints -----
    from app.api.media import media_bp
    from app.api.tweets import tweets_bp
    from app.api.likes import likes_bp
    from app.api.users import users_bp

    app.register_blueprint(media_bp)
    app.register_blueprint(tweets_bp)
    app.register_blueprint(likes_bp)
    app.register_blueprint(users_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)