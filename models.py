from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    apartment_number = db.Column(db.String(10))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<Tenant {self.first_name} {self.last_name}>"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    tenant = db.relationship('Tenant', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f"<Payment for {self.amount}>"


# New User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.username}>"
