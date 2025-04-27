from flask import Flask, request, send_from_directory, render_template_string
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    conn.autocommit = True
    return conn

# Record a visit to the database
def record_visit(ip_address, notes=None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO visits (visitor_ip, notes) VALUES (%s, %s) RETURNING id;",
            (ip_address, notes)
        )
        visit_id = cur.fetchone()[0]
        cur.close()
        conn.close()
        return visit_id
    except Exception as e:
        print(f"Error recording visit: {e}")
        return None

# Retrieve all visits
def get_visits():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, visited_at, visitor_ip, notes FROM visits ORDER BY visited_at DESC;")
    visits = cur.fetchall()
    cur.close()
    conn.close()
    return visits

@app.route('/')
def index():
    # Record the visit
    ip = request.remote_addr
    record_visit(ip, "Visited memory game")
    
    # Serve the index.html file
    return send_from_directory('.', 'index.html')

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/admin', methods=['GET'])
def admin_panel():
    # You might want to add authentication here
    visits = get_visits()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Panel - Visit Tracker</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #d65d7a; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8e1e8; }
            tr:hover { background-color: #f5f5f5; }
        </style>
    </head>
    <body>
        <h1>Visit Tracker - Admin Panel</h1>
        <p>This page shows when your boyfriend (or anyone else) visited your memory game.</p>
        
        <h2>Recent Visits</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Date/Time</th>
                <th>IP Address</th>
                <th>Notes</th>
            </tr>
            {% for visit in visits %}
            <tr>
                <td>{{ visit[0] }}</td>
                <td>{{ visit[1] }}</td>
                <td>{{ visit[2] }}</td>
                <td>{{ visit[3] }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    
    return render_template_string(html, visits=visits)

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)