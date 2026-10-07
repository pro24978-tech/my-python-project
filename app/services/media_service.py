import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from app.extensions import db
from app.models import Media


def save_uploaded_file(file):
    """
    Сохраняет загруженный файл в папку static/uploads,
    создаёт запись в таблице Media и возвращает media_id и URL.
    """
    # Генерируем уникальное имя файла
    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{original_filename}"

    # Путь для сохранения
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "app/static/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, unique_filename)

    # Сохраняем файл
    file.save(file_path)

    # Создаём запись в БД (пока без привязки к твиту)
    media = Media(file_path=f"uploads/{unique_filename}")  # относительный путь
    db.session.add(media)
    db.session.commit()

    return media.id, f"/uploads/{unique_filename}"