from flask import Blueprint, request, jsonify

from app.utils.auth import get_current_user
from app.services.tweet_service import create_tweet, delete_tweet, get_feed


tweets_bp = Blueprint("tweets", __name__, url_prefix="/api/tweets")


@tweets_bp.route("", methods=["GET"])
def get_tweets():
    """
    Возвращает ленту твитов текущего пользователя.
    Сортировка: по убыванию количества лайков.
    """
    user = get_current_user()
    feed = get_feed(user.id)
    return jsonify({
        "result": True,
        "tweets": feed
    })


@tweets_bp.route("", methods=["POST"])
def post_tweet():
    """
    Создаёт новый твит.
    Тело запроса (JSON):
      {"tweet_data": "...", "tweet_media_ids": [1, 2, ...]}
    """
    user = get_current_user()
    data = request.get_json(silent=True) or {}

    tweet_data = data.get("tweet_data", "").strip()
    media_ids = data.get("tweet_media_ids", []) or []

    if not tweet_data:
        return jsonify({
            "result": False,
            "error_type": "ValidationError",
            "error_message": "tweet_data is required"
        }), 400

    tweet_id = create_tweet(user.id, tweet_data, media_ids)
    return jsonify({
        "result": True,
        "tweet_id": tweet_id
    })


@tweets_bp.route("/<int:tweet_id>", methods=["DELETE"])
def remove_tweet(tweet_id):
    """
    Удаляет твит. Только автор может удалить свой твит.
    """
    user = get_current_user()
    delete_tweet(tweet_id, user.id)
    return jsonify({"result": True})