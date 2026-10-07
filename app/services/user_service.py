from app.extensions import db
from app.models import User, Follow

def get_user_by_id(user_id):
    """Возвращает пользователя по id или None."""
    return User.query.get(user_id)

def get_user_profile(user_id):
    """
    Возвращает информацию о профиле пользователя:
    id, name, followers (список), following (список).
    """
    user = User.query.get(user_id)
    if not user:
        raise LookupError("User not found")

    # Получаем подписчиков (тех, кто подписан на user)
    followers = []
    for follow in Follow.query.filter_by(following_id=user_id).all():
        follower = User.query.get(follow.follower_id)
        if follower:
            followers.append({"id": follower.id, "name": follower.name})

    # Получаем подписки (тех, на кого подписан user)
    following = []
    for follow in Follow.query.filter_by(follower_id=user_id).all():
        followed = User.query.get(follow.following_id)
        if followed:
            following.append({"id": followed.id, "name": followed.name})

    return {
        "id": user.id,
        "name": user.name,
        "followers": followers,
        "following": following
    }

def follow_user(follower_id, following_id):
    """
    Подписывает пользователя follower_id на following_id.
    Если подписка уже существует — ничего не делает.
    """
    if follower_id == following_id:
        raise ValueError("You cannot follow yourself")

    existing = Follow.query.filter_by(
        follower_id=follower_id,
        following_id=following_id
    ).first()
    if existing:
        return False  # уже подписан

    follow = Follow(follower_id=follower_id, following_id=following_id)
    db.session.add(follow)
    db.session.commit()
    return True

def unfollow_user(follower_id, following_id):
    """
    Отписывает пользователя follower_id от following_id.
    Если подписки нет — ничего не делает.
    """
    follow = Follow.query.filter_by(
        follower_id=follower_id,
        following_id=following_id
    ).first()
    if not follow:
        return False

    db.session.delete(follow)
    db.session.commit()
    return True