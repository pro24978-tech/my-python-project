from flask import request, abort
from app.extensions import db
from app.models import User


def get_current_user():
    """
    Получает пользователя по api-key из заголовка запроса.
    Если ключ не передан или пользователь не найден, возвращает 401.
    """
    api_key = request.headers.get("api-key")

    if not api_key:
        abort(401, description="Missing api-key header")

    user = User.query.filter_by(api_token=api_key).first()

    if not user:
        abort(401, description="Invalid api-key")

    return user