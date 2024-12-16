from app.database import get_db_connection

def add_note(tenant_id, note_type, note_description, date_added):
    """Add a note for a tenant."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO notes (tenant_id, note_type, note_description, date_added)
    VALUES (?, ?, ?, ?)
    """, (tenant_id, note_type, note_description, date_added))
    conn.commit()
    conn.close()

def get_tenant_notes(tenant_id):
    """Get all notes for a tenant."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE tenant_id = ?", (tenant_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes
