from getpass import getpass

from app import create_app, db
from app.models import User

if __name__ == '__main__':
    first_name = input('First Name: ')
    last_name = input('Last Name: ')
    email = input('Email: ')
    password = getpass()

    app = create_app()
    with app.app_context():
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            admin=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print('Successfully created user')