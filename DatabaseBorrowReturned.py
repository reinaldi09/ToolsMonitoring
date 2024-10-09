from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Connect to the database
def connect_db():
    return sqlite3.connect('tools.db')

# Combined handling of borrowing and returning tools
@app.route('/transaction', methods=['POST'])
def handle_transaction():
    rfid = request.json.get('rfid')
    tool = request.json.get('tool')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = connect_db()
    cursor = conn.cursor()

    # Check if the tool is already borrowed (return_date is NULL)
    cursor.execute("SELECT * FROM borrow_records WHERE tool = ? AND return_date IS NULL", (tool,))
    record = cursor.fetchone()

    if record:
        # The tool is borrowed, so we return it
        cursor.execute("UPDATE borrow_records SET return_date = ? WHERE tool = ? AND return_date IS NULL", (current_time, tool))
        conn.commit()
        response = f"Tool {tool} returned successfully by user {rfid}."
    else:
        # The tool is not borrowed, so we borrow it
        cursor.execute("INSERT INTO borrow_records (rfid, tool, borrow_date) VALUES (?, ?, ?)", (rfid, tool, current_time))
        conn.commit()
        response = f"Tool {tool} borrowed successfully by user {rfid}."

    conn.close()
    return jsonify(message=response)

if __name__ == '__main__':
    app.run(debug=True)

