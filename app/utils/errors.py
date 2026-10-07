from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """
    Регистрирует обработчики ошибок для приложения.
    Все ошибки возвращаются в едином формате:
    {"result": false, "error_type": ..., "error_message": ...}
    """

    @app.errorhandler(401)
    def handle_401(e):
        return jsonify({
            "result": False,
            "error_type": "Unauthorized",
            "error_message": str(e.description) if hasattr(e, "description") else "Unauthorized"
        }), 401

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({
            "result": False,
            "error_type": "NotFound",
            "error_message": str(e.description) if hasattr(e, "description") else "Not Found"
        }), 404

    @app.errorhandler(PermissionError)
    def handle_permission(e):
        return jsonify({
            "result": False,
            "error_type": "PermissionDenied",
            "error_message": str(e)
        }), 403

    @app.errorhandler(LookupError)
    def handle_lookup(e):
        return jsonify({
            "result": False,
            "error_type": "NotFound",
            "error_message": str(e)
        }), 404

    @app.errorhandler(ValueError)
    def handle_value(e):
        return jsonify({
            "result": False,
            "error_type": "ValidationError",
            "error_message": str(e)
        }), 400

    @app.errorhandler(Exception)
    def handle_generic(e):
        # Если это HTTPException, отдаём его код
        if isinstance(e, HTTPException):
            return jsonify({
                "result": False,
                "error_type": e.name,
                "error_message": e.description
            }), e.code
        # Иначе — 500
        return jsonify({
            "result": False,
            "error_type": "InternalServerError",
            "error_message": str(e)
        }), 500