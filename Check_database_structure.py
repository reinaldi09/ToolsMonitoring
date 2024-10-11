import sqlite3

conn = sqlite3.connect('tools_database.db')
cursor = conn.cursor()

# Get table structure (or use a tool like sqlitebrowser)
cursor.execute('PRAGMA table_info(borrow_records)')

table_info = cursor.fetchall()

print("Table Structure:")
for column in table_info:
  print(column[1])  # Print column names (index 1)

conn.close()
