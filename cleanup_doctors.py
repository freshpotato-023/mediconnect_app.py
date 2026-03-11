import sqlite3
import os

def cleanup_orphaned_doctors():
    """Remove doctors from doctors table that don't have corresponding user accounts"""

    db_path = 'mediconnect.db'
    if not os.path.exists(db_path):
        print('Database not found')
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all doctors
    cursor.execute('SELECT id, name FROM doctors')
    all_doctors = cursor.fetchall()

    # Get all doctor users
    cursor.execute('SELECT id, full_name FROM users WHERE role = "doctor"')
    doctor_users = cursor.fetchall()

    doctor_user_names = {user[1] for user in doctor_users}

    print(f'Total doctors in doctors table: {len(all_doctors)}')
    print(f'Total doctor users: {len(doctor_users)}')
    print()

    orphaned_doctors = []
    for doc_id, doc_name in all_doctors:
        if doc_name not in doctor_user_names:
            orphaned_doctors.append((doc_id, doc_name))

    print(f'Orphaned doctors (no user account): {len(orphaned_doctors)}')
    for doc_id, doc_name in orphaned_doctors:
        print(f'  - ID: {doc_id}, Name: {doc_name}')

    # Delete orphaned doctors
    if orphaned_doctors:
        print(f'\nDeleting {len(orphaned_doctors)} orphaned doctors...')
        for doc_id, doc_name in orphaned_doctors:
            cursor.execute('DELETE FROM doctors WHERE id = ?', (doc_id,))
            print(f'  Deleted: {doc_name}')

        conn.commit()
        print('Cleanup completed!')

    # Verify remaining doctors
    cursor.execute('SELECT COUNT(*) FROM doctors')
    remaining = cursor.fetchone()[0]
    print(f'\nRemaining doctors: {remaining}')

    conn.close()

if __name__ == "__main__":
    cleanup_orphaned_doctors()
