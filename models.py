from app import db

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
