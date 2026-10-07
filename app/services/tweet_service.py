from app.extensions import db
from app.models import Tweet, Media, Like, Follow, User

def create_tweet(author_id, content, media_ids=None):
    """
    Создаёт новый твит. Если переданы media_ids, привязывает их к твиту.
    Возвращает id созданного твита.
    """
    if not content:
        raise ValueError("Tweet content cannot be empty")

    tweet = Tweet(author_id=author_id, content=content)
    db.session.add(tweet)
    db.session.flush()  # получаем tweet.id до коммита

    # Привязываем медиа, если есть
    if media_ids:
        for media_id in media_ids:
            media = Media.query.get(media_id)
            if media and media.tweet_id is None:  # медиа ещё не привязано
                media.tweet_id = tweet.id

    db.session.commit()
    return tweet.id


def delete_tweet(tweet_id, user_id):
    """
    Удаляет твит, если он принадлежит пользователю.
    Возвращает True, если удаление успешно.
    """
    tweet = Tweet.query.get(tweet_id)
    if not tweet:
        raise LookupError("Tweet not found")

    if tweet.author_id != user_id:
        raise PermissionError("You can only delete your own tweets")

    # Сначала отвязываем/удаляем медиа, привязанные к твиту
    Media.query.filter_by(tweet_id=tweet_id).delete()
    # Удаляем лайки
    Like.query.filter_by(tweet_id=tweet_id).delete()

    db.session.delete(tweet)
    db.session.commit()
    return True


def get_feed(user_id):
    """
    Возвращает список твитов от пользователей, на которых подписан user_id.
    Сортировка: по убыванию количества лайков.
    Каждый твит содержит: id, content, attachments, author, likes.
    """
    # Получаем id тех, на кого подписан пользователь
    following_ids = [
        f.following_id
        for f in Follow.query.filter_by(follower_id=user_id).all()
    ]
    # Включаем и свои твиты (по желанию; в ТЗ сказано "от пользователей, которых он фоловит",
    # но обычно в ленте есть и свои. Если нужно строго — уберите user_id из списка)
    following_ids.append(user_id)

    # Получаем твиты этих пользователей
    tweets = Tweet.query.filter(Tweet.author_id.in_(following_ids)).all()

    # Формируем результат и сортируем по лайкам
    result = []
    for tweet in tweets:
        likes = Like.query.filter_by(tweet_id=tweet.id).all()
        likes_list = []
        for like in likes:
            like_user = User.query.get(like.user_id)
            if like_user:
                likes_list.append({
                    "user_id": like_user.id,
                    "name": like_user.name
                })

        attachments = [
            f"/{m.file_path}" for m in Media.query.filter_by(tweet_id=tweet.id).all()
        ]

        author = User.query.get(tweet.author_id)
        result.append({
            "id": tweet.id,
            "content": tweet.content,
            "attachments": attachments,
            "author": {
                "id": author.id,
                "name": author.name
            },
            "likes": likes_list
        })

    # Сортировка по количеству лайков (по убыванию)
    result.sort(key=lambda t: len(t["likes"]), reverse=True)
    return result