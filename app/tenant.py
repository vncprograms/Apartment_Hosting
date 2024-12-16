import sqlite3

DATABASE_PATH = 'apartment_management.db'

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def create_tenants_table():
    """Create the tenants table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        deposit REAL,
        apartment_number TEXT,
        notes TEXT  -- Added notes column for storing tenant notes
    );
    ''')
    conn.commit()
    conn.close()

def add_notes_column():
    """Add the 'notes' column to the tenants table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        # Try to add the 'notes' column
        cursor.execute("ALTER TABLE tenants ADD COLUMN notes TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # If the 'notes' column already exists, it will raise an OperationalError, which we catch
        pass
    conn.close()

def add_tenant(first_name, last_name, phone, email, deposit, apartment_number, notes):
    """Add a new tenant to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tenants (first_name, last_name, phone, email, deposit, apartment_number, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, phone, email, deposit, apartment_number, notes))
    conn.commit()
    conn.close()

def get_all_tenants():
    """Get all tenants from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name, last_name, apartment_number, notes FROM tenants")
    tenants = cursor.fetchall()
    conn.close()

    return [{
        'id': tenant[0],
        'first_name': tenant[1],
        'last_name': tenant[2],
        'apartment_number': tenant[3],
        'notes': tenant[4]
    } for tenant in tenants]

def get_tenant_by_id(tenant_id):
    """Get tenant details by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, first_name, last_name, phone, email, deposit, apartment_number, notes
        FROM tenants WHERE id = ?
    ''', (tenant_id,))
    tenant = cursor.fetchone()
    conn.close()

    if tenant:
        return {
            'id': tenant[0],
            'first_name': tenant[1],
            'last_name': tenant[2],
            'phone': tenant[3],
            'email': tenant[4],
            'deposit': tenant[5],
            'apartment_number': tenant[6],
            'notes': tenant[7]
        }
    return None

def update_tenant_notes(tenant_id, notes):
    """Update tenant notes in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE tenants SET notes = ? WHERE id = ?''', (notes, tenant_id))
    conn.commit()
    conn.close()

# Ensure table and 'notes' column are created/added when the app starts
create_tenants_table()
add_notes_column()
