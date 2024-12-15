from app.database import get_db_connection

def add_payment(tenant_id, amount, month, year, payment_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO payments (tenant_id, amount, month, year, payment_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (tenant_id, amount, month, year, payment_date))

    conn.commit()
    conn.close()
