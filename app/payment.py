from app.database import get_db_connection

def add_payment(tenant_id, amount, month, year, payment_date):
    """Add a payment record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO payments (tenant_id, amount, month, year, payment_date)
    VALUES (?, ?, ?, ?, ?)
    """, (tenant_id, amount, month, year, payment_date))
    conn.commit()
    conn.close()

def get_tenant_payments(tenant_id):
    """Get all payments for a tenant."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE tenant_id = ?", (tenant_id,))
    payments = cursor.fetchall()
    conn.close()
    return payments
