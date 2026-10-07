from flask import Blueprint, jsonify

from app.utils.auth import get_current_user
from app.services.user_service import get_user_profile, follow_user, unfollow_user


users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/me", methods=["GET"])
def get_me():
    """
    Возвращает информацию о текущем пользователе:
    id, name, followers, following.
    """
    user = get_current_user()
    profile = get_user_profile(user.id)
    return jsonify({
        "result": True,
        "user": profile
    })


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Возвращает информацию о пользователе по id.
    (Не упомянут в ТЗ, но полезен; можно использовать для профиля.)
    """
    profile = get_user_profile(user_id)
    return jsonify({
        "result": True,
        "user": profile
    })


@users_bp.route("/<int:user_id>/follow", methods=["POST"])
def follow(user_id):
    """Подписаться на пользователя."""
    user = get_current_user()
    follow_user(user.id, user_id)
    return jsonify({"result": True})


@users_bp.route("/<int:user_id>/follow", methods=["DELETE"])
def unfollow(user_id):
    """Отписаться от пользователя."""
    user = get_current_user()
    unfollow_user(user.id, user_id)
    return jsonify({"result": True})