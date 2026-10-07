from flask import Blueprint, jsonify

from app.utils.auth import get_current_user
from app.extensions import db
from app.models import Tweet, Like


likes_bp = Blueprint("likes", __name__, url_prefix="/api/tweets")


@likes_bp.route("/<int:tweet_id>/likes", methods=["POST"])
def like_tweet(tweet_id):
    """
    Ставит лайк на твит. Если лайк уже есть — ничего не делает.
    """
    user = get_current_user()

    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        raise LookupError("Tweet not found")

    existing = Like.query.filter_by(user_id=user.id, tweet_id=tweet_id).first()
    if existing:
        return jsonify({"result": True})

    like = Like(user_id=user.id, tweet_id=tweet_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({"result": True})


@likes_bp.route("/<int:tweet_id>/likes", methods=["DELETE"])
def unlike_tweet(tweet_id):
    """
    Убирает лайк с твита. Если лайка нет — ничего не делает.
    """
    user = get_current_user()

    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        raise LookupError("Tweet not found")

    like = Like.query.filter_by(user_id=user.id, tweet_id=tweet_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()

    return jsonify({"result": True})