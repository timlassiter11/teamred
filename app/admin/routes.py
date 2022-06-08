from app import db
from app.admin import bp
from app.forms import AdminUserEditForm, AirplaneForm, AirportForm
from app.models import Airplane, Airport, User
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import IntegrityError


@bp.before_request
def restrict_bp_to_admins():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login', next=url_for(request.endpoint)))

    if current_user.role != 'admin':
        abort(403)


@bp.route('/')
def home():
    return render_template('admin/home.html')


@bp.route('/users')
def users():
    user_form = AdminUserEditForm()
    return render_template(
        'admin/users.html',
        title='Users',
        users=User.query.all(),
        user_form=user_form
    )


@bp.route('/users/<user_id>', methods=['POST'])
def user(user_id):
    user = User.query.get(int(user_id))
    if user is None:
        abort(404)

    user_form = AdminUserEditForm()
    if user_form.validate_on_submit():
        if user_form.method.data == 'POST':
            user.email = user_form.email.data
            user.first_name = user_form.first_name.data
            user.last_name = user_form.last_name.data
            # TODO: Think about how changing the role from agent to user
            # would affect things such as agents sales. 
            user.role = user_form.role.data
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('User with that email already exists', category='danger')
        elif user_form.method.data == 'DELETE':
            db.session.delete(user)
            db.session.commit()

    return redirect(url_for('admin.users'))


@bp.route('/airports', methods=['GET'])
def airports():
    form = AirportForm()
    columns = _get_columns(Airport, ['id'])
    return render_template(
        'admin/table.html',
        title='Airports',
        form=form,
        table_name='Airport',
        url=url_for('api.airports'),
        columns=columns
    )


@bp.route('/airplanes', methods=['GET'])
def airplanes():
    form = AirplaneForm()
    columns = _get_columns(Airplane, ['id'])
    return render_template(
        'admin/table.html',
        title='Airplanes',
        form=form,
        table_name='Airplanes',
        url=url_for('api.airplanes'),
        columns=columns
    )


def _get_columns(model, exclude=[]):
    return [column.name for column in inspect(model).columns if column.name not in exclude]