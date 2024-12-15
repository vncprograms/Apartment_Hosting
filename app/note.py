from app.database import get_db_connection

def add_note(tenant_id, note_type, note_description, date_added):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO notes (tenant_id, note_type, note_description, date_added)
    VALUES (?, ?, ?, ?)
    ''', (tenant_id, note_type, note_description, date_added))

    conn.commit()
    conn.close()
