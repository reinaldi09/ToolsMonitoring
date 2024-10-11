# from flask import Flask, request, jsonify
# import sqlite3
# from datetime import datetime
#
# app = Flask(__name__)
#
# # Connect to the database
# def connect_db():
#     return sqlite3.connect('tools.db')
#
# # Combined handling of borrowing and returning tools
# @app.route('/transaction', methods=['POST'])
# def handle_transaction():
#     rfid = request.json.get('rfid')
#     tool = request.json.get('tool')
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     conn = connect_db()
#     cursor = conn.cursor()
#
#     # Check if the tool is already borrowed (return_date is NULL)
#     cursor.execute("SELECT * FROM borrow_records WHERE tool = ? AND return_date IS NULL", (tool,))
#     record = cursor.fetchone()
#
#     if record:
#         # The tool is borrowed, so we return it
#         cursor.execute("UPDATE borrow_records SET return_date = ? WHERE tool = ? AND return_date IS NULL", (current_time, tool))
#         conn.commit()
#         response = f"Tool {tool} returned successfully by user {rfid}."
#     else:
#         # The tool is not borrowed, so we borrow it
#         cursor.execute("INSERT INTO borrow_records (rfid, tool, borrow_date) VALUES (?, ?, ?)", (rfid, tool, current_time))
#         conn.commit()
#         response = f"Tool {tool} borrowed successfully by user {rfid}."
#
#     conn.close()
#     return jsonify(message=response)
#
# # API to retrieve all transactions
# @app.route('/transactions', methods=['GET'])
# def get_transactions():
#     conn = connect_db()
#     cursor = conn.cursor()
#
#     # Get all transaction records
#     cursor.execute("SELECT rfid, tool, borrow_date, return_date FROM borrow_records")
#     records = cursor.fetchall()
#
#     # Format records for JSON response
#     result = []
#     for rfid, tool, borrow_date, return_date in records:
#         result.append({
#             'rfid': rfid,
#             'tool': tool,
#             'borrow_date': borrow_date,
#             'return_date': return_date
#         })
#
#     conn.close()
#     return jsonify(result)
#
# if __name__ == '__main__':
#     app.run(debug=True)


# import sqlite3
# from datetime import datetime, timedelta
# import random
# import uuid
# from flask import Flask, render_template, jsonify
#
# app = Flask(__name__)
#
#
# # Connect to the database
# def connect_db():
#     return sqlite3.connect('tools_database.db')
#
# # Function to start borrowing session (borrow multiple tools)
# def start_borrowing_session(rfid, name):
#     session_id = str(uuid.uuid4())  # Generate a unique session ID
#     print(f"Borrowing session started for RFID {rfid} with session ID: {session_id}")
#     return session_id
#
#
# # Function to borrow multiple tools
# def borrow_multiple_tools(rfid, name, tools):
#     session_id = start_borrowing_session(rfid, name)
#     conn = connect_db()
#     cursor = conn.cursor()
#
#     borrow_date = datetime.now()
#     for tool in tools:
#         cursor.execute(
#             "INSERT INTO borrow_records (rfid, tool, borrow_date_and_time, session_id, name) VALUES (?, ?, ?, ?, ?)",
#             (rfid, tool, borrow_date.strftime("%Y-%m-%d %H:%M:%S"), session_id, name))
#
#     conn.commit()
#     conn.close()
#     print(f"Tools {tools} borrowed by {rfid} under session {session_id}")
#
#
# # Function to mark tools as returned for a given session
# def end_borrowing_session(session_id):
#     conn = connect_db()
#     cursor = conn.cursor()
#
#     return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#     # Update all records for the session, setting the return date
#     cursor.execute(
#         "UPDATE borrow_records SET return_date_and_time = ? WHERE session_id = ? AND return_date_and_time IS NULL",
#         (return_date, session_id))
#
#     conn.commit()
#     conn.close()
#
#
# # Fetch all records from the database
# def fetch_records():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute(
#         'SELECT id, name, rfid, tool, borrow_date_and_time, return_date_and_time, session_id FROM borrow_records ORDER BY borrow_date_and_time DESC')
#     records = cursor.fetchall()
#     conn.close()
#     return records
#
#
# # Route to display the data on the web page
# @app.route('/')
# def index():
#     transactions = fetch_records()  # Fetch data from the database
#     return render_template('index.html', transactions=transactions)
#
# # Route to borrow multiple tools via API for testing purposes
# @app.route('/borrow/<rfid>/<name>/<tools>')
# def borrow(rfid, name, tools):
#     tools_list = tools.split(',')  # Parse tools from URL (comma-separated)
#     borrow_multiple_tools(rfid, name, tools_list)
#     return f"Borrowed tools {tools} for {name} successfully!"
#
#
# # Route to simulate returning tools and ending a borrowing session
# @app.route('/return/<session_id>')
# def return_tools(session_id):
#     end_borrowing_session(session_id)
#     return f"Tools for session {session_id} have been returned!"
#
#
# # API endpoint to get data in JSON format
# @app.route('/api/data')
# def get_data():
#     transactions = fetch_records()
#     data = [{"id": r[0], "name": r[1], "rfid": r[2], "tool": r[3], "borrow_date_and_time": r[4],
#              "return_date_and_time": r[5], "session_id": r[6]} for r in transactions]
#     return jsonify(data)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

import sqlite3
from datetime import datetime
import uuid
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Simulated variables for cabinet state
cabinet_locked = True

# Connect to the database
def connect_db():
    return sqlite3.connect('tools_database.db')

# Function to simulate RFID scan for unlocking the cabinet
def unlock_cabinet(rfid):
    global cabinet_locked
    if cabinet_locked:
        cabinet_locked = False
        print(f"Cabinet unlocked for RFID {rfid}.")
    else:
        print("Cabinet is already unlocked!")

# Function to simulate RFID scan for locking the cabinet
def lock_cabinet(rfid):
    global cabinet_locked
    if not cabinet_locked:
        cabinet_locked = True
        print(f"Cabinet locked for RFID {rfid}.")
    else:
        print("Cabinet is already locked!")

# Function to start borrowing session (borrow multiple tools)
def start_borrowing_session(rfid, name):
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    print(f"Borrowing session started for RFID {rfid} with session ID: {session_id}")
    unlock_cabinet(rfid)  # Unlock the cabinet when session starts
    return session_id

# Function to borrow multiple tools (after scanning barcodes)
def borrow_multiple_tools(rfid, name, tools):
    session_id = start_borrowing_session(rfid, name)
    conn = connect_db()
    cursor = conn.cursor()

    borrow_date = datetime.now()
    for tool in tools:
        cursor.execute(
            "INSERT INTO borrow_records (rfid, tool, borrow_date_and_time, session_id, name) VALUES (?, ?, ?, ?, ?)",
            (rfid, tool, borrow_date.strftime("%Y-%m-%d %H:%M:%S"), session_id, name))

    conn.commit()
    conn.close()
    print(f"Tools {tools} borrowed by {rfid} under session {session_id}")

# Function to mark tools as returned for a given session
def end_borrowing_session(session_id, rfid):
    conn = connect_db()
    cursor = conn.cursor()

    return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update all records for the session, setting the return date
    cursor.execute(
        "UPDATE borrow_records SET return_date_and_time = ? WHERE session_id = ? AND return_date_and_time IS NULL",
        (return_date, session_id))

    conn.commit()
    conn.close()
    print(f"Tools for session {session_id} have been returned.")
    lock_cabinet(rfid)  # Lock the cabinet after returning tools

# Fetch all records from the database
def fetch_records():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, name, rfid, tool, borrow_date_and_time, return_date_and_time, session_id FROM borrow_records ORDER BY borrow_date_and_time DESC')
    records = cursor.fetchall()
    conn.close()
    return records

# Route to display the data on the web page
@app.route('/')
def index():
    transactions = fetch_records()  # Fetch data from the database
    return render_template('index.html', transactions=transactions)

# Route to simulate borrowing tools via API (this simulates RFID scan and barcode scan)
@app.route('/borrow/<rfid>/<name>/<tools>')
def borrow(rfid, name, tools):
    tools_list = tools.split(',')  # Parse tools from URL (comma-separated)
    if cabinet_locked:
        return "Cabinet is locked. Please scan your RFID to unlock."
    borrow_multiple_tools(rfid, name, tools_list)
    return f"Borrowed tools {tools} for {name} successfully!"

# Route to simulate scanning RFID and unlocking the cabinet
@app.route('/rfid/scan/<rfid>')
def rfid_scan(rfid):
    unlock_cabinet(rfid)
    return f"RFID {rfid} scanned. Cabinet unlocked."

# Route to simulate scanning RFID and locking the cabinet
@app.route('/rfid/lock/<rfid>')
def rfid_lock(rfid):
    lock_cabinet(rfid)
    return f"RFID {rfid} scanned. Cabinet locked."

# Route to simulate returning tools and ending a borrowing session
@app.route('/return/<rfid>/<session_id>/<tools>')
def return_tools(rfid, session_id, tools):
    tools_list = tools.split(',')  # Parse tools from URL (comma-separated)
    if cabinet_locked:
        return "Cabinet is locked. Please scan your RFID to unlock."
    end_borrowing_session(session_id, rfid)
    return f"Returned tools {tools} for session {session_id}."

# API endpoint to get data in JSON format
@app.route('/api/data')
def get_data():
    transactions = fetch_records()
    data = [{"id": r[0], "name": r[1], "rfid": r[2], "tool": r[3], "borrow_date_and_time": r[4],
             "return_date_and_time": r[5], "session_id": r[6]} for r in transactions]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
