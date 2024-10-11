# import sqlite3
# from datetime import datetime, timedelta
# import random
# from flask import Flask, render_template, jsonify
#
# app = Flask(__name__)
#
# # Connect to the database
# def connect_db():
#     return sqlite3.connect('tools_database.db')
#
# # Generate mock data
# def generate_mock_data():
#     name_list = ['aku', 'aki', 'aka', 'ake', 'ako']
#     rfid_list = ['123456', '654321', '789012', '345678', '901234']
#     tool_list = ['Hammer123', 'Wrench456', 'Screwdriver789', 'Drill012', 'Pliers345']
#
#     # Simulate borrowing and returning data
#     conn = connect_db()
#     cursor = conn.cursor()
#
#     for i in range(5):
#         name = random.choice(name_list)
#         rfid = random.choice(rfid_list)
#         tool = random.choice(tool_list)
#         borrow_date = datetime.now() - timedelta(days=random.randint(1, 10))
#         return_date = None if random.random() > 0.5 else borrow_date + timedelta(hours=random.randint(1, 24))
#
#         cursor.execute("INSERT INTO borrow_records (id, name, rfid, tool, borrow_date_and_time, return_date_and_time) VALUES (?, ?, ?, ?, ?, ?)",
#                        (name, rfid, tool, borrow_date.strftime("%Y-%m-%d %H:%M:%S"),
#                         return_date.strftime("%Y-%m-%d %H:%M:%S") if return_date else None))
#
#     conn.commit()
#     conn.close()
#
# # Fetch all records from the database
# def fetch_records():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, name, rfid, tool, borrow_date_and_time, return_date_and_time FROM borrow_records ORDER BY borrow_date_and_time DESC')
#     records = cursor.fetchall()
#     conn.close()
#     return records
#
# # Route to display the data on the web page
# @app.route('/')
# def index():
#     transactions = fetch_records()  # Fetch data from the database
#     return render_template('index.html', transactions=transactions)
#
# # Route to insert mock data
# @app.route('/generate')
# def generate():
#     generate_mock_data()
#     return "Mock data generated successfully!"
#
# # API endpoint to get data in JSON format
# @app.route('/api/data')
# def get_data():
#     transactions = fetch_records()
#     data = [{"id": r[0], "name": r[1], "rfid": r[2], "tool": r[3], "borrow_date_and_time": r[4], "return_date_and_time": r[5]} for r in transactions]
#     return jsonify(data)
#
# if __name__ == '__main__':
#     app.run(debug=True)

import sqlite3
from datetime import datetime, timedelta
import random
import uuid
from flask import Flask, render_template, jsonify

app = Flask(__name__)


# Connect to the database
def connect_db():
    return sqlite3.connect('tools_database.db')


# Generate mock data with multiple tool borrowing per session
def generate_mock_data():
    name_list = ['aku', 'aki', 'aka', 'ake', 'ako']
    rfid_list = ['123456', '654321', '789012', '345678', '901234']
    tool_list = ['Hammer123', 'Wrench456', 'Screwdriver789', 'Drill012', 'Pliers345']

    conn = connect_db()
    cursor = conn.cursor()

    for i in range(5):
        name = random.choice(name_list)
        rfid = random.choice(rfid_list)
        session_id = str(uuid.uuid4())  # Generate unique session ID for multiple borrowings
        borrow_date = datetime.now() - timedelta(days=random.randint(1, 10))
        return_date = None if random.random() > 0.5 else borrow_date + timedelta(hours=random.randint(1, 24))

        # Simulate borrowing multiple tools in one session
        tools_borrowed = random.sample(tool_list, random.randint(1, 3))  # Borrow 1 to 3 tools
        for tool in tools_borrowed:
            cursor.execute(
                "INSERT INTO borrow_records (rfid, tool, borrow_date_and_time, return_date_and_time, session_id, name) VALUES (?, ?, ?, ?, ?, ?)",
                (rfid, tool, borrow_date.strftime("%Y-%m-%d %H:%M:%S"),
                 return_date.strftime("%Y-%m-%d %H:%M:%S") if return_date else None,
                 session_id, name))

    conn.commit()
    conn.close()


# Function to start borrowing session (borrow multiple tools)
def start_borrowing_session(rfid, name):
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    print(f"Borrowing session started for RFID {rfid} with session ID: {session_id}")
    return session_id


# Function to borrow multiple tools
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
def end_borrowing_session(session_id):
    conn = connect_db()
    cursor = conn.cursor()

    return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update all records for the session, setting the return date
    cursor.execute(
        "UPDATE borrow_records SET return_date_and_time = ? WHERE session_id = ? AND return_date_and_time IS NULL",
        (return_date, session_id))

    conn.commit()
    conn.close()


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


# Route to simulate data generation
@app.route('/generate')
def generate():
    generate_mock_data()
    return "Mock data generated successfully!"


# Route to borrow multiple tools via API for testing purposes
@app.route('/borrow/<rfid>/<name>/<tools>')
def borrow(rfid, name, tools):
    tools_list = tools.split(',')  # Parse tools from URL (comma-separated)
    borrow_multiple_tools(rfid, name, tools_list)
    return f"Borrowed tools {tools} for {name} successfully!"


# Route to simulate returning tools and ending a borrowing session
@app.route('/return/<session_id>')
def return_tools(session_id):
    end_borrowing_session(session_id)
    return f"Tools for session {session_id} have been returned!"


# API endpoint to get data in JSON format
@app.route('/api/data')
def get_data():
    transactions = fetch_records()
    data = [{"id": r[0], "name": r[1], "rfid": r[2], "tool": r[3], "borrow_date_and_time": r[4],
             "return_date_and_time": r[5], "session_id": r[6]} for r in transactions]
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
