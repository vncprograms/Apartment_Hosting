from app.database import get_db_connection

def add_apartment(rent_price, utilities_price):
    """Add a new apartment to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO apartments (rent_price, utilities_price)
        VALUES (?, ?)
    ''', (rent_price, utilities_price))
    conn.commit()
    apartment_id = cursor.lastrowid  # Get the last inserted ID
    conn.close()
    return apartment_id
