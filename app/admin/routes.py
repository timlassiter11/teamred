from flask import redirect, render_template, abort, request, url_for
from flask_login import current_user
from app import db
from app.admin import bp
from app.forms import UserEditForm
from app.models import User

@bp.before_request
def restrict_bp_to_admins():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login', next=url_for(request.endpoint)))

    if not current_user.admin:
        abort(403)

@bp.route('/')
def home():
    return render_template('admin/home.html')


@bp.route('/users')
def users():
    user_form = UserEditForm()
    return render_template(
        'admin/users.html',
        users=User.query.all(),
        user_form=user_form
    )

@bp.route('/users/<user_id>', methods=['POST'])
def user(user_id):
    user = User.query.get(int(user_id))
    if user is None:
        abort(404)

    user_form = UserEditForm()
    if user_form.validate_on_submit():
        if user_form.method.data == 'POST':
            user.email = user_form.email.data
            user.first_name = user_form.first_name.data
            user.last_name = user_form.last_name.data
            db.session.commit()
        elif user_form.method.data == 'DELETE':
            db.session.delete(user)
            db.session.commit()

    return redirect(url_for('admin.users'))
