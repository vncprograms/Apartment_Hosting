from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tenant model
class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    apartment_number = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    notes = db.Column(db.Text)

    # Relationship to complaints (one-to-many)
    complaints = db.relationship('Complaint', backref='tenant', lazy=True)

# Complaint model
class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)

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
        notes = request.form['notes']

        new_tenant = Tenant(first_name=first_name, last_name=last_name, 
                            apartment_number=apartment_number, email=email, 
                            phone=phone, notes=notes)

        db.session.add(new_tenant)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_tenant.html')

# Edit tenant route
@app.route('/edit_tenant/<int:id>', methods=['GET', 'POST'])
def edit_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    if request.method == 'POST':
        tenant.first_name = request.form['first_name']
        tenant.last_name = request.form['last_name']
        tenant.apartment_number = request.form['apartment_number']
        tenant.email = request.form['email']
        tenant.phone = request.form['phone']
        tenant.notes = request.form['notes']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_tenant.html', tenant=tenant)

# View tenant details route
@app.route('/view_tenant/<int:id>')
def view_tenant(id):
    tenant = Tenant.query.get_or_404(id)
    return render_template('view_tenant.html', tenant=tenant)

# Update tenant notes route (NEW)
@app.route('/update_notes/<int:id>', methods=['POST'])
def update_notes(id):
    tenant = Tenant.query.get_or_404(id)
    tenant.notes = request.form['notes']  # Get the updated notes from the form
    db.session.commit()  # Save the changes to the database
    return redirect(url_for('view_tenant', id=tenant.id))  # Redirect back to the tenant's view page

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query')  # Get the search query from the form input
    if query:
        # Query the database for tenants with matching first or last name
        tenants = Tenant.query.filter(
            Tenant.first_name.contains(query) | Tenant.last_name.contains(query)
        ).all()
    else:
        tenants = Tenant.query.all()  # If no query, return all tenants
    
    return render_template('index.html', tenants=tenants)

if __name__ == "__main__":
    app.run(debug=True)
