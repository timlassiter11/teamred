import json
from getpass import getpass
from traceback import print_exc
from typing import TYPE_CHECKING

import flask_migrate

from app import create_app, db
from app.models import Airport, User

if TYPE_CHECKING:
    from flask import Flask


def create_db(app: "Flask"):
    print('Creating database.')
    with app.app_context():
        flask_migrate.upgrade()


def create_user(app: "Flask"):
    print('Creating admin user.')
    try:
        with app.app_context():
            email = input('Email: ')
            user: User = User.query.filter_by(email=email).first()
            # If the user doesn't exist create it
            if user is None:
                password = getpass()
                first_name = input('First Name: ')
                last_name = input('Last Name: ')
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    role='admin'
                )
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                print('Successfully created admin user.')
            # Else just update the existing user
            else:
                print(
                    f'User already exists... changing role from {user.role} to admin.')
                user.role = 'admin'
                db.session.commit()
                print('Successfully updated user.')
    except KeyboardInterrupt:
        print('\nCreate user cancelled.')


def populate_airports(app: "Flask"):
    print('Populating database with airports from data/airports.json.')

    with open('data/airports.json') as f:
        data = f.read()
        json_data = json.loads(data)

    with app.app_context():
        for aiport in json_data:
            db.session.add(Airport(
                code=aiport['code'],
                name=aiport['name'],
                timezone=aiport['tz']
            ))
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            print('Error adding airports')
            print_exc()
        else:
            print('Successfully added all airports.')


if __name__ == '__main__':
    app = create_app()

    create_db(app)
    create_user(app)
    populate_airports(app)
