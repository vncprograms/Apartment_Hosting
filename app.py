from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # To use Flask's session for flashing messages
db = SQLAlchemy(app)

# Tenant model
class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    apartment_number = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20))

    # Relationship to complaints (one-to-many)
    complaints = db.relationship('Complaint', backref='tenant', lazy=True)
    
    # Relationship to notes (one-to-many)
    notes = db.relationship('Note', backref='tenant', lazy=True, cascade='all, delete-orphan')

# Complaint model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)

# Note model (New model to store individual notes for each tenant)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    note_type = db.Column(db.String(50))  # New field to store the note type (complaint, payment, late fee)

# Home page (List tenants)
@app.route('/')
def index():
    tenants = Tenant.query.all()
    return render_template('index.html', tenants=tenants)

# Delete tenant route
@app.route('/delete_tenant/<int:id>', methods=['POST'])
def delete_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    db.session.delete(tenant)
    db.session.commit()
    flash('Tenant deleted successfully!', 'success')
    return redirect(url_for('index'))

# Add tenant route
@app.route('/add_tenant', methods=['GET', 'POST'])
def add_tenant():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        apartment_number = request.form['apartment_number']
        email = request.form['email']
        phone = request.form['phone']

        new_tenant = Tenant(first_name=first_name, last_name=last_name, 
                            apartment_number=apartment_number, email=email, 
                            phone=phone)

        db.session.add(new_tenant)
        db.session.commit()
        flash('Tenant added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_tenant.html')

# View tenant details route (with notes)
@app.route('/view_tenant/<int:id>', methods=['GET'])
def view_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    return render_template('view_tenant.html', tenant=tenant)

# Add a new note for a tenant
@app.route('/add_note/<int:tenant_id>', methods=['POST'])
def add_note(tenant_id):
    tenant = Tenant.query.get_or_404(tenant_id)
    note_content = request.form['content']
    note_type = request.form['note_type']

    if note_type == 'other':
        note_type = request.form.get('custom_note_type', 'Other')

    if note_content:
        new_note = Note(content=note_content, tenant_id=tenant.id, note_type=note_type)
        db.session.add(new_note)
        db.session.commit()

    flash('Note added successfully!', 'success')
    return redirect(url_for('view_tenant', id=tenant.id))

# Delete a note route
@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    tenant_id = note.tenant_id

    db.session.delete(note)
    db.session.commit()

    flash('Note deleted successfully!', 'success')
    return redirect(url_for('view_tenant', id=tenant_id))

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
