import json
import random
from argparse import ArgumentParser
from getpass import getpass
import sys
from traceback import print_exc
from typing import TYPE_CHECKING, List

import flask_migrate

from app import create_app, db
from app.models import Airplane, Airport, User

if TYPE_CHECKING:
    from flask import Flask


def drop_db(app: "Flask") -> None:
    print('Dropping database.')
    with app.app_context():
        flask_migrate.downgrade(revision='base')


def create_db(app: "Flask") -> None:
    print('Creating database.')
    with app.app_context():
        flask_migrate.upgrade()


def create_user(app: "Flask") -> None:
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


def populate_airports(app: "Flask") -> None:
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


def create_airplanes(app: "Flask", count: int = 500) -> None:
    print('Populating database with randomly generated airplanes')

    class AirplaneModel:
        def __init__(self, name, model, min_capacity, max_capacity, range) -> None:
            self.name = name
            self.model = model
            self.min_capacity = min_capacity
            self.max_capacity = max_capacity
            self.range = range
    # Create a list of common commercial plane models with their specifications
    models: List[AirplaneModel] = [
        AirplaneModel('Boeing 737', 'B737-800', min_capacity=189,
                      max_capacity=189, range=1995),
        AirplaneModel('Airbus A320', 'A320', min_capacity=140,
                      max_capacity=180, range=3300),
        AirplaneModel('Boeing 757', 'B757-200', min_capacity=200,
                      max_capacity=200, range=3915),
        AirplaneModel('Boeing 777', '777-200ER', min_capacity=314,
                      max_capacity=314, range=5845),
    ]

    with app.app_context():
        registration_numbers = []
        for _ in range(count):
            # Start with a random base model
            model = random.choice(models)
            # Create a random capacity based off of the models min and max capacity
            capacity = random.randint(model.min_capacity, model.max_capacity)
            while True:
                # Aircraft registration numbers in the US start with an N
                # and can end with a two letter code representing the airline.
                # There can be up to 3 numbers in between for a range of 1 to 999.
                # We will use RE for Red Eye as the last two letters.
                number = random.randint(1, 999)
                registration_number = f'N{number}RE'
                # Make sure we don't have any repeating registration numbers.
                if registration_number not in registration_numbers:
                    registration_numbers.append(registration_number)
                    break

            airplane = Airplane(
                model_name=model.name,
                model_code=model.model,
                range=model.range,
                capacity=capacity,
                registration_number=registration_number
            )
            db.session.add(airplane)
        db.session.commit()
    print(f'Successfully created {count} airplanes.')


if __name__ == '__main__':
    parser = ArgumentParser(description='Initialize the Red Eye database. If no arguments are given all functions will be run.')
    parser.add_argument('-c', '--create-user', action='store_true', help='Create an admin user.')
    parser.add_argument('-a', '--create-airports', action='store_true', help='Populate the database with airports from data/airports.json.')
    parser.add_argument('-b', '--create-airplanes', action='store_true', help='Populate the database with randomly generated airplanes.')
    parser.add_argument('-d', '--drop-tables', action='store_true', help='Drop all of the tables from the database and start fresh.')

    args = parser.parse_args()

    # If no args are given just do everything
    no_args = (len(sys.argv) == 1)

    app = create_app()

    if no_args or args.drop_tables:
        drop_db(app)

    # Always create the database regardless if tables were dropped.
    # This ensures it's completely up to date and will do nothing if it is.
    create_db(app)
    
    if no_args or args.create_user:
        create_user(app)
    
    if no_args or args.create_airports:
        populate_airports(app)

    if no_args or args.create_airplanes:
        create_airplanes(app)
