from app.database import get_db_connection

def add_apartment(rent_price, utilities_price, status="available"):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO apartments (rent_price, utilities_price, status)
    VALUES (?, ?, ?)
    ''', (rent_price, utilities_price, status))

    conn.commit()
    apartment_id = cursor.lastrowid
    conn.close()
    return apartment_id
