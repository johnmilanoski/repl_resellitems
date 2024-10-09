from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash
import logging

def create_admin_user():
    app = create_app()
    with app.app_context():
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

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
            logger.info("Admin user created successfully.")
            print("Admin user created successfully.")
        else:
            logger.info("Admin user already exists.")
            print("Admin user already exists.")

        # Verify admin user
        admin_user = User.query.filter_by(is_admin=True).first()
        if admin_user:
            logger.info(f"Admin user verified: {admin_user.username} (ID: {admin_user.id})")
        else:
            logger.error("Failed to verify admin user in the database")

if __name__ == '__main__':
    create_admin_user()
