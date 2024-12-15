import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database/apartment_management.db')
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create apartments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS apartments (
        apartment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rent_price REAL,
        utilities_price REAL,
        status TEXT
    )
    ''')

    # Create tenants table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenants (
        tenant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        lease_start_date TEXT,
        lease_end_date TEXT,
        deposit REAL,
        apartment_id INTEGER,
        FOREIGN KEY (apartment_id) REFERENCES apartments (apartment_id)
    )
    ''')

    # Create payments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER,
        amount REAL,
        month TEXT,
        year INTEGER,
        payment_date TEXT,
        FOREIGN KEY (tenant_id) REFERENCES tenants (tenant_id)
    )
    ''')

    # Create notes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER,
        note_type TEXT,
        note_description TEXT,
        date_added TEXT,
        FOREIGN KEY (tenant_id) REFERENCES tenants (tenant_id)
    )
    ''')

    conn.commit()
    conn.close()
