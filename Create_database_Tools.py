import sqlite3

conn = sqlite3.connect('tools_database.db')  # Replace with your filename
cursor = conn.cursor()

# Create the table (modify column names and data types if needed)
sql = '''CREATE TABLE IF NOT EXISTS borrow_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rfid TEXT NOT NULL,
            tool TEXT NOT NULL,
            borrow_date_and_time TEXT NOT NULL,
            return_date_and_time TEXT,
            session_id TEXT
           )'''
cursor.execute(sql)
conn.commit()
conn.close()

print("Table 'borrow_records' created successfully!")

# # Connect to the database
# def connect_db():
#     return sqlite3.connect('tools_database.db')
#
# # Create the borrow_records table if it doesn't exist
# def create_table():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS borrow_records (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             rfid TEXT NOT NULL,
#             tool TEXT NOT NULL,
#             borrow_date TEXT NOT NULL,
#             return_date TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
# if __name__ == '__main__':
#     create_table()  # Make sure the table exists
#
