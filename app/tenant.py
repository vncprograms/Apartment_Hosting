from app.database import get_db_connection

def add_tenant(name, lease_start_date, lease_end_date, deposit, apartment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO tenants (name, lease_start_date, lease_end_date, deposit, apartment_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, lease_start_date, lease_end_date, deposit, apartment_id))
    
    conn.commit()
    
    tenant_id = cursor.lastrowid
    conn.close()
    return tenant_id

def get_tenant_payments(tenant_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT month, year, amount FROM payments
    WHERE tenant_id = ?
    ORDER BY year, month
    ''', (tenant_id,))

    payments = cursor.fetchall()
    conn.close()
    return payments
