from flask import Blueprint, request, jsonify

from app.utils.auth import get_current_user
from app.services.media_service import save_uploaded_file


media_bp = Blueprint("media", __name__, url_prefix="/api")


@media_bp.route("/medias", methods=["POST"])
def upload_media():
    """
    Загружает медиа-файл.
    Ожидает multipart/form-data с полем 'file'.
    Возвращает {"result": true, "media_id": int}.
    """
    # Проверяем, что пользователь авторизован (api-key в заголовке)
    get_current_user()

    if "file" not in request.files:
        return jsonify({
            "result": False,
            "error_type": "ValidationError",
            "error_message": "No file provided"
        }), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({
            "result": False,
            "error_type": "ValidationError",
            "error_message": "Empty filename"
        }), 400

    media_id, url = save_uploaded_file(file)

    return jsonify({
        "result": True,
        "media_id": media_id
    })