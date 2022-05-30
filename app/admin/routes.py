from app import db
from app.admin import bp
from app.forms import AdminUserEditForm, AirportForm
from app.models import Airport, User
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
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


@bp.route('/airports', methods=['GET', 'POST'])
def airports():
    airport_form = AirportForm()
    if airport_form.validate_on_submit():
        airport = Airport()
        airport_form.populate_obj(airport)
        db.session.add(airport)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Airport with that code already exists', category='danger')

    return render_template(
        'admin/airports.html',
        title='Airports',
        airports=Airport.query.all(),
        airport_form=airport_form
    )


@bp.route('/airports/<airport_id>', methods=['POST'])
def airport(airport_id):
    airport = Airport.query.get(int(airport_id))
    if airport is None:
        abort(404)

    airport_form = AirportForm()
    if airport_form.validate_on_submit():
        if airport_form.method.data == 'POST':
            airport.code = airport_form.code.data
            airport.name = airport_form.name.data
            airport.timezone = airport_form.timezone.data
            db.session.commit()
        elif airport_form.method.data == 'DELETE':
            db.session.delete(airport)
            db.session.commit()

    return redirect(url_for('admin.airports'))
