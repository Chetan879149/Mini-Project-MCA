import sqlite3

def delete_user_by_aadhaar(aadhaar):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE aadhaar = ?", (aadhaar,))
    conn.commit()
    conn.close()
    print(f"User with Aadhaar {aadhaar} deleted.")

# Example usage: delete user with aadhaar '123456789012'
delete_user_by_aadhaar("")

def print_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, aadhaar, phone, role FROM users")
    all_rows = cursor.fetchall()
    conn.close()

    print("Users in the database:")
    for row in all_rows:
        print(row)

# Check users after deletion
print_all_users()
