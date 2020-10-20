# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Users(UserMixin, db.Model):
    """
    Create an Users table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    fundraisers = db.relationship('Fundraiser', backref='users', lazy=True)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Fundraiser(db.Model):
    """
    Create a Fundraiser table
    """

    __tablename__ = 'fundraisers'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Fundraiser: {}>'.format(self.title)
