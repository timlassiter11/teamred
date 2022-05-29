from flask import render_template
from app.errors import bp


@bp.app_errorhandler(Exception)
def handle_error(error):
    code = error.code
    return render_template(
        'errors/error.html', 
        error_text=error.name, 
        error_code=code
    ), code
