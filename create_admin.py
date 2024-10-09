from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash

def create_admin_user():
    app = create_app()
    with app.app_context():
        admin_user = User.query.filter_by(is_admin=True).first()
        if admin_user is None:
            new_admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('adminpassword'),
                is_admin=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    create_admin_user()
