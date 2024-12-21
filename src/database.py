import sqlite3

def connect_db():
    return sqlite3.connect('apartments.db')

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Create tenants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tenants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            apartment_number TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            notes TEXT
        )
    ''')

    # Create payments table for tracking payments made by tenants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER,
            payment_date TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_status TEXT NOT NULL,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    ''')

    conn.commit()
    conn.close()

def load_tenants():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tenants')
    rows = cursor.fetchall()

    tenants = []
    for row in rows:
        tenant = {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'apartment_number': row[3],
            'email': row[4],
            'phone': row[5],
            'notes': row[6].splitlines() if row[6] else []  # Ensure notes is a list
        }
        tenants.append(tenant)

    conn.close()
    return tenants

def save_tenants(tenants):
    conn = connect_db()
    cursor = conn.cursor()

    for tenant in tenants:
        notes_string = "\n".join(tenant['notes'])  # Convert notes list into a string with newlines
        cursor.execute('''
            INSERT OR REPLACE INTO tenants (id, first_name, last_name, apartment_number, email, phone, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tenant['id'], tenant['first_name'], tenant['last_name'], tenant['apartment_number'],
              tenant['email'], tenant['phone'], notes_string))

    conn.commit()
    conn.close()

def load_payments(tenant_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments WHERE tenant_id = ?', (tenant_id,))
    rows = cursor.fetchall()

    payments = []
    for row in rows:
        payment = {
            'id': row[0],
            'tenant_id': row[1],
            'payment_date': row[2],
            'amount': row[3],
            'payment_status': row[4]
        }
        payments.append(payment)

    conn.close()
    return payments

def save_payment(tenant_id, payment_date, amount, payment_status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO payments (tenant_id, payment_date, amount, payment_status)
        VALUES (?, ?, ?, ?)
    ''', (tenant_id, payment_date, amount, payment_status))
    conn.commit()
    conn.close()

def update_tenant_in_db(tenant):
    conn = connect_db()
    cursor = conn.cursor()

    notes_string = "\n".join(tenant['notes'])
    cursor.execute('''
        UPDATE tenants SET first_name = ?, last_name = ?, apartment_number = ?, email = ?, phone = ?, notes = ?
        WHERE id = ?
    ''', (tenant['first_name'], tenant['last_name'], tenant['apartment_number'], tenant['email'],
          tenant['phone'], notes_string, tenant['id']))

    conn.commit()
    conn.close()

def delete_tenant_from_db(tenant_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tenants WHERE id = ?', (tenant_id,))
    cursor.execute('DELETE FROM payments WHERE tenant_id = ?', (tenant_id,))
    conn.commit()
    conn.close()
