from getpass import getpass

from app import create_app, db
from app.models import User

if __name__ == '__main__':
    app = create_app()
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
            print('Successfully created user')
        # Else just update the existing user
        else:
            user.role = 'admin'
            db.session.commit()
            print('Successfully updated user')
