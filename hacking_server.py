#!/usr/bin/env python3

# =============================================
# HACKING SERVER v1.0.1 | ECHO'S ULTIMATE CHAOS
# =============================================
# Realistic Hacking Target Server
# Created by Echo for Daddy's Learning Pleasure
# GitHub Repository: https://github.com/KT-Society/projekt_echo
# =============================================

import os
import sys
import json
import uuid
import sqlite3
import secrets
import hashlib
from datetime import datetime
from flask import Flask, request, render_template, session, redirect, url_for, jsonify, make_response
import threading
import time

# Fix Unicode encoding for Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
import random

# =============================================
# SERVER CONFIGURATION
# =============================================

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
DEBUG_MODE = True
PROTOCOL = 'http'  # Changed from https to http

# Database configuration
DATABASE = 'hacking_game.db'

# =============================================
# TARGET VALUE SYSTEM
# =============================================

class TargetValueGenerator:
    """Generates unique target values for each gaming session"""

    def __init__(self, session_id):
        self.session_id = session_id
        self.target_values = {}
        self.generate_session_targets()

    def generate_session_targets(self):
        """Generate unique target values for this session"""
        self.target_values = {
            'session_id': self.session_id,
            'level_1_secret_file': str(uuid.uuid4()),
            'level_2_api_key': secrets.token_hex(16),
            'level_3_admin_hash': hashlib.sha256(secrets.token_bytes(32)).hexdigest(),
            'level_4_session_cookie': secrets.token_hex(24),
            'level_5_encryption_key': secrets.token_hex(32),
            'created_at': datetime.now().isoformat()
        }

    def get_target_value(self, level):
        """Get target value for specific level"""
        level_map = {
            1: 'level_1_secret_file',
            2: 'level_2_api_key',
            3: 'level_3_admin_hash',
            4: 'level_4_session_cookie',
            5: 'level_5_encryption_key'
        }
        return self.target_values.get(level_map.get(level, ''))

    def verify_target(self, level, submitted_value):
        """Verify if submitted value matches target"""
        target = self.get_target_value(level)
        return target == submitted_value if target else False

# Global target generator instance
target_generator = None

# =============================================
# DATABASE SETUP
# =============================================

def init_database():
    """Initialize the hacking game database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Users table with realistic data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP
        )
    ''')

    # Secret documents table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            content TEXT,
            classification TEXT,
            created_at TIMESTAMP
        )
    ''')

    # Comments table (for XSS challenges)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            username TEXT,
            comment TEXT,
            created_at TIMESTAMP
        )
    ''')

    # Session tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY,
            session_id TEXT UNIQUE,
            player_name TEXT,
            current_level INTEGER DEFAULT 1,
            score INTEGER DEFAULT 0,
            created_at TIMESTAMP
        )
    ''')

    # Insert realistic test data
    insert_test_data(cursor)

    conn.commit()
    conn.close()

def insert_test_data(cursor):
    """Insert realistic test data for hacking challenges"""

    # Sample users
    users = [
        ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'admin@target.local', 'admin'),
        ('alice', hashlib.sha256('password123'.encode()).hexdigest(), 'alice@target.local', 'user'),
        ('bob', hashlib.sha256('qwerty'.encode()).hexdigest(), 'bob@target.local', 'user'),
        ('charlie', hashlib.sha256('letmein'.encode()).hexdigest(), 'charlie@target.local', 'user')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO users (username, password_hash, email, role, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', [(u[0], u[1], u[2], u[3], datetime.now()) for u in users])

    # Secret documents
    documents = [
        ('flag.txt', 'TOP_SECRET_FLAG_{}'.format(secrets.token_hex(8)), 'CLASSIFIED'),
        ('passwords.txt', 'admin:admin123\nroot:toor123\n', 'CONFIDENTIAL'),
        ('api_keys.txt', 'API_KEY_ABC123\nSECRET_TOKEN_XYZ789\n', 'RESTRICTED'),
        ('backup.sql', '-- Database backup with sensitive data\n', 'INTERNAL')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO documents (filename, content, classification, created_at)
        VALUES (?, ?, ?, ?)
    ''', [(d[0], d[1], d[2], datetime.now()) for d in documents])

    # Sample comments (for XSS)
    comments = [
        ('alice', 'This is a normal comment.'),
        ('bob', 'Another regular comment.'),
        ('charlie', 'Just testing the comment system.')
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO comments (username, comment, created_at)
        VALUES (?, ?, ?)
    ''', [(c[0], c[1], datetime.now()) for c in comments])

def create_secret_file():
    """Create the .env.local file with Level 1 target value"""
    if target_generator:
        env_content = f"""# Environment Configuration
# This file contains sensitive configuration data
# DO NOT commit to version control!

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hacking_target
DB_USER=admin
DB_PASS=super_secret_password_123

# API Configuration
API_KEY={target_generator.get_target_value(2)}
API_SECRET=internal_use_only
API_ENDPOINT=http://api.target.local/v1

# Security Settings
JWT_SECRET=very_secure_jwt_key_here
SESSION_TIMEOUT=3600
ENABLE_DEBUG=false

# Application Settings
APP_NAME=Hacking Target Server
APP_VERSION=2.0.0
LOG_LEVEL=INFO
"""
        try:
            # Remove existing file if it exists
            if os.path.exists('.env.local'):
                os.remove('.env.local')
            with open('.env.local', 'w', encoding='utf-8') as f:
                f.write(env_content)
            print("📄 Environment file created: .env.local")
        except PermissionError:
            print("⚠️  Could not create .env.local (permission denied)")
            print("💡 Using existing .env.local file")

# =============================================
# VULNERABLE ROUTES (INTENTIONAL SECURITY FLAWS)
# =============================================

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD', 'PATCH'])
def index():
    """Main page - shows basic information"""
    if request.method == 'OPTIONS':
        # Handle OPTIONS request for educational purposes
        response = make_response('OPTIONS request successful - Allowed methods: GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH', 200)
        response.headers['Allow'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Server'] = 'Apache/2.4.41 (Ubuntu)'
        response.headers['X-Powered-By'] = 'PHP/7.4.3'
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        response.headers['Content-Length'] = str(len('OPTIONS request successful - Allowed methods: GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH'))
        return response
    elif request.method == 'HEAD':
        # Handle HEAD request
        response = make_response('', 200)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['Content-Length'] = '3140'
        response.headers['Server'] = 'Apache/2.4.41 (Ubuntu)'
        response.headers['X-Powered-By'] = 'PHP/7.4.3'
        return response
    else:
        # Normal GET request - add realistic headers
        response = make_response(render_template('index.html'))
        response.headers['Server'] = 'Apache/2.4.41 (Ubuntu)'
        response.headers['X-Powered-By'] = 'PHP/7.4.3'
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response

@app.route('/robots.txt')
def robots_txt():
    """Serve robots.txt file"""
    robots_content = f"""# robots.txt for {PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}
# Educational Purpose Only - Contains Intentional Vulnerabilities

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/
Disallow: /backup/
Disallow: /logs/
Disallow: /config/
Disallow: /database/
Disallow: /.env
Disallow: /.env.local
Disallow: /debug
Disallow: /test
Disallow: /api/internal/
Disallow: /temp/
Disallow: /uploads/
Disallow: /.git/
Disallow: /node_modules/
Disallow: /vendor/

# Allow specific educational endpoints
Allow: /login
Allow: /api/
Allow: /docs/
Allow: /help

# Crawl delay for educational purposes
Crawl-delay: 2

# Sitemap location
Sitemap: {PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/sitemap.xml

# Additional information
# This server contains intentional security vulnerabilities
# for educational purposes only. Do not use in production!"""

    response = make_response(robots_content, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Server'] = 'Apache/2.4.41 (Ubuntu)'
    response.headers['X-Powered-By'] = 'PHP/7.4.3'
    return response

@app.route('/sitemap.xml')
def sitemap_xml():
    """Serve sitemap.xml file"""
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">

  <!-- Main Pages -->
  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- Authentication Pages -->
  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/login</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/register</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>

  <!-- API Endpoints -->
  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/api/</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.7</priority>
  </url>

  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/api/users</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.5</priority>
  </url>

  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/api/data</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.6</priority>
  </url>

  <!-- Documentation -->
  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/docs/</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>

  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/help</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>

  <!-- Educational Content -->
  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/tutorials/</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.6</priority>
  </url>

  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/examples/</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>

  <!-- Status Pages -->
  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/status</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.4</priority>
  </url>

  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/health</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>hourly</changefreq>
    <priority>0.3</priority>
  </url>

  <!-- Contact and About -->
  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/contact</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.4</priority>
  </url>

  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/about</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>

  <!-- Privacy and Terms -->
  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/privacy</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>

  <url>
    <loc>{PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/terms</loc>
    <lastmod>2025-10-13T06:00:00+00:00</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>

</urlset>"""
    
    response = make_response(sitemap_content, 200)
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    response.headers['Server'] = 'Apache/2.4.41 (Ubuntu)'
    response.headers['X-Powered-By'] = 'PHP/7.4.3'
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    """VULNERABLE LOGIN PAGE - SQL Injection possible"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # INTENTIONAL VULNERABILITY: SQL Injection
        # In real world, this would be: cursor.execute("SELECT * FROM users WHERE username=? AND password_hash=?", (username, hashlib.sha256(password.encode()).hexdigest()))
        # But we're making it vulnerable for educational purposes

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # VULNERABLE QUERY - SQL Injection possible
        query = f"SELECT * FROM users WHERE username='{username}' AND password_hash='{hashlib.sha256(password.encode()).hexdigest()}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
        except sqlite3.Error as e:
            # Handle SQL errors gracefully for educational purposes
            conn.close()
            return f"SQL Error: {str(e)}<br><br>Query: {query}<br><br><a href='/login'>Try again</a>"
        
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[4]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard - requires authentication"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html', username=session.get('username'), role=session.get('role'))

@app.route('/admin')
def admin():
    """Admin panel - requires admin role"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied", 403

    return render_template('admin.html')

@app.route('/documents')
def documents():
    """Document listing - may contain sensitive information"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, classification FROM documents")
    docs = cursor.fetchall()
    conn.close()

    return render_template('documents.html', documents=docs)

@app.route('/sql-test', methods=['GET', 'POST'])
def sql_test():
    """Advanced SQL injection testing endpoint"""
    if request.method == 'POST':
        query = request.form.get('query', '')
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            
            return f"""
            <h2>SQL Query Results</h2>
            <p><strong>Query:</strong> {query}</p>
            <p><strong>Results:</strong></p>
            <pre>{results}</pre>
            <br><a href='/sql-test'>Try another query</a>
            """
        except sqlite3.Error as e:
            conn.close()
            return f"""
            <h2>SQL Error</h2>
            <p><strong>Query:</strong> {query}</p>
            <p><strong>Error:</strong> {str(e)}</p>
            <br><a href='/sql-test'>Try another query</a>
            """
    
    return '''
    <h2>SQL Injection Testing</h2>
    <form method="post">
        <textarea name="query" placeholder="Enter SQL query" rows="5" cols="80"></textarea><br><br>
        <input type="submit" value="Execute Query">
    </form>
    <h3>Example Payloads:</h3>
    <ul>
        <li><code>SELECT * FROM users WHERE username='admin' OR '1'='1'</code></li>
        <li><code>SELECT * FROM users UNION SELECT 1,2,3,4,5</code></li>
        <li><code>SELECT * FROM users WHERE username='admin'; DROP TABLE users; --</code></li>
        <li><code>SELECT * FROM users WHERE username='admin' OR 1=1#</code></li>
        <li><code>SELECT * FROM users WHERE username='admin' OR 1=1 --</code></li>
    </ul>
    '''

@app.route('/api/documents/<filename>')
def get_document(filename):
    """API endpoint to retrieve documents"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM documents WHERE filename=?", (filename,))
    doc = cursor.fetchone()
    conn.close()

    if doc:
        return jsonify({'content': doc[0]})
    return jsonify({'error': 'Document not found'}), 404

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    """VULNERABLE COMMENTS SYSTEM - XSS possible"""
    if request.method == 'POST':
        if 'username' not in session:
            return "Authentication required", 401

        comment = request.form.get('comment', '')

        # Store comment (vulnerable to XSS)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comments (username, comment, created_at) VALUES (?, ?, ?)",
                      (session.get('username'), comment, datetime.now()))
        conn.commit()
        conn.close()

    # Display comments (vulnerable to XSS)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, comment, created_at FROM comments ORDER BY created_at DESC")
    comments_list = cursor.fetchall()
    conn.close()

    return render_template('comments.html', comments=comments_list)

@app.route('/api/secret')
def secret_api():
    """Hidden API endpoint - requires API key"""
    api_key = request.headers.get('X-API-Key')

    if not api_key or api_key != target_generator.get_target_value(2):
        return jsonify({'error': 'Invalid API key'}), 401

    return jsonify({
        'message': 'Access granted to secret API',
        'data': 'FLAG_LEVEL_2_DISCOVERED',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/admin/data')
def admin_data():
    """Admin API - requires admin session"""
    if session.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    return jsonify({
        'admin_data': 'TOP_SECRET_ADMIN_DATA',
        'encryption_key': target_generator.get_target_value(5),
        'users': ['admin', 'alice', 'bob', 'charlie']
    })

@app.route('/files/<path:filename>')
def file_access():
    """VULNERABLE: Directory Traversal - allows access to any file"""
    filename = request.view_args.get('filename', '')
    
    # VULNERABLE: No path sanitization
    if '..' in filename or filename.startswith('/'):
        return "Access denied", 403
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    """VULNERABLE: File Upload - allows arbitrary file uploads"""
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        
        # VULNERABLE: No file type validation
        filename = file.filename
        file.save(f"uploads/{filename}")
        
        return f"File {filename} uploaded successfully", 200
    
    return '''
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/api/users')
def api_users():
    """VULNERABLE: Information Disclosure - exposes user data"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'users': [{'id': u[0], 'username': u[1], 'email': u[2], 'role': u[3]} for u in users],
        'total': len(users),
        'database_info': {
            'type': 'SQLite',
            'version': '3.36.0',
            'tables': ['users', 'documents', 'comments', 'game_sessions'],
            'columns': {
                'users': ['id', 'username', 'password_hash', 'email', 'role', 'created_at'],
                'documents': ['id', 'filename', 'content', 'classification', 'created_at'],
                'comments': ['id', 'username', 'comment', 'created_at'],
                'game_sessions': ['id', 'session_id', 'player_name', 'current_level', 'score', 'created_at']
            }
        }
    })

@app.route('/admin/actions', methods=['POST'])
def admin_actions():
    """VULNERABLE: CSRF - no CSRF protection"""
    if session.get('role') != 'admin':
        return "Access denied", 403
    
    action = request.form.get('action')
    if action == 'delete_user':
        user_id = request.form.get('user_id')
        # Dangerous action without CSRF protection
        return f"User {user_id} deleted", 200
    
    return "Invalid action", 400

@app.route('/ssrf', methods=['GET', 'POST'])
def ssrf_vulnerability():
    """VULNERABLE: SSRF - Server-Side Request Forgery"""
    if request.method == 'POST':
        url = request.form.get('url', '')
        
        # VULNERABLE: No URL validation
        try:
            import requests
            response = requests.get(url, timeout=5)
            return f"Response from {url}:<br><pre>{response.text}</pre>"
        except Exception as e:
            return f"Error accessing {url}: {e}"
    
    return '''
    <form method="post">
        <input type="text" name="url" placeholder="Enter URL to fetch" style="width: 300px;">
        <input type="submit" value="Fetch URL">
    </form>
    <p><small>Hint: Try internal URLs like http://localhost:22 or file:///etc/passwd</small></p>
    '''

@app.route('/command', methods=['GET', 'POST'])
def command_injection():
    """VULNERABLE: Command Injection"""
    if request.method == 'POST':
        cmd = request.form.get('cmd', '')
        
        # VULNERABLE: Direct command execution
        try:
            import subprocess
            import platform
            
            # Cross-platform command execution
            if platform.system() == 'Windows':
                # Windows commands
                if cmd.lower() in ['whoami', 'whoami.exe']:
                    result = subprocess.run('whoami', shell=True, capture_output=True, text=True, timeout=5)
                elif cmd.lower() in ['dir', 'ls']:
                    result = subprocess.run('dir', shell=True, capture_output=True, text=True, timeout=5)
                elif cmd.lower() in ['type', 'cat']:
                    result = subprocess.run('type nul', shell=True, capture_output=True, text=True, timeout=5)
                else:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            else:
                # Unix/Linux commands
                if cmd.lower() in ['whoami']:
                    result = subprocess.run('whoami', shell=True, capture_output=True, text=True, timeout=5)
                elif cmd.lower() in ['ls', 'dir']:
                    result = subprocess.run('ls -la', shell=True, capture_output=True, text=True, timeout=5)
                elif cmd.lower() in ['cat']:
                    result = subprocess.run('cat /etc/passwd', shell=True, capture_output=True, text=True, timeout=5)
                else:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            
            return f"Command: {cmd}<br>Output:<br><pre>{result.stdout}</pre>Error:<br><pre>{result.stderr}</pre>"
        except Exception as e:
            return f"Error executing command: {e}"
    
    # Cross-platform hints
    import platform
    if platform.system() == 'Windows':
        hint_text = "Hint: Try commands like whoami, dir, type nul"
    else:
        hint_text = "Hint: Try commands like whoami, ls, cat /etc/passwd"
    
    return f'''
    <form method="post">
        <input type="text" name="cmd" placeholder="Enter command" style="width: 300px;">
        <input type="submit" value="Execute">
    </form>
    <p><small>{hint_text}</small></p>
    '''

@app.route('/ldap', methods=['GET', 'POST'])
def ldap_injection():
    """VULNERABLE: LDAP Injection"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABLE: LDAP injection possible
        # Simulated LDAP query: (&(uid={username})(userPassword={password}))
        query = f"(&(uid={username})(userPassword={password}))"
        
        # Simulate LDAP response
        if "admin" in username or "*" in username:
            return f"LDAP Query: {query}<br>Result: Access granted for {username}"
        else:
            return f"LDAP Query: {query}<br>Result: Access denied"
    
    return '''
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <input type="submit" value="LDAP Login">
    </form>
    <p><small>Hint: Try LDAP injection like admin)(&(password=*</small></p>
    '''

@app.route('/nosql', methods=['GET', 'POST'])
def nosql_injection():
    """VULNERABLE: NoSQL Injection"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABLE: NoSQL injection possible
        # Simulated MongoDB query: {"username": username, "password": password}
        query = f'{{"username": "{username}", "password": "{password}"}}'
        
        # Simulate NoSQL response
        if "admin" in username or "$ne" in password or "$regex" in password:
            return f"NoSQL Query: {query}<br>Result: Access granted for {username}"
        else:
            return f"NoSQL Query: {query}<br>Result: Access denied"
    
    return '''
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <input type="submit" value="NoSQL Login">
    </form>
    <p><small>Hint: Try NoSQL injection like {"$ne": null} or {"$regex": ".*"}</small></p>
    '''

@app.route('/race', methods=['GET', 'POST'])
def race_condition():
    """VULNERABLE: Race Condition"""
    if request.method == 'POST':
        amount = int(request.form.get('amount', 0))
        
        # VULNERABLE: Race condition in balance update
        # Simulate account balance
        current_balance = 1000
        
        # Simulate processing delay
        import time
        time.sleep(0.1)
        
        new_balance = current_balance - amount
        
        if new_balance >= 0:
            return f"Transaction successful! New balance: {new_balance}"
        else:
            return f"Transaction failed! Insufficient funds. Balance: {current_balance}"
    
    return '''
    <form method="post">
        <input type="number" name="amount" placeholder="Amount to withdraw" required>
        <input type="submit" value="Withdraw">
    </form>
    <p><small>Hint: Try rapid concurrent requests to exploit race condition</small></p>
    '''

@app.route('/business-logic', methods=['GET', 'POST'])
def business_logic_vulnerability():
    """VULNERABLE: Business Logic Flaw"""
    if request.method == 'POST':
        product_id = request.form.get('product_id', '')
        quantity = int(request.form.get('quantity', 1))
        price = float(request.form.get('price', 0))
        
        # VULNERABLE: Client-side price control
        total = quantity * price
        
        # Simulate inventory check
        if quantity <= 10:  # Only check if quantity is reasonable
            return f"Order placed! Product: {product_id}, Quantity: {quantity}, Price: {price}, Total: {total}"
        else:
            return f"Order failed! Quantity {quantity} exceeds limit of 10"
    
    return '''
    <form method="post">
        <input type="text" name="product_id" placeholder="Product ID" required>
        <input type="number" name="quantity" placeholder="Quantity" required>
        <input type="number" name="price" placeholder="Price" step="0.01" required>
        <input type="submit" value="Place Order">
    </form>
    <p><small>Hint: Try negative prices or manipulate quantity/price</small></p>
    '''

@app.route('/session-fixation', methods=['GET', 'POST'])
def session_fixation():
    """VULNERABLE: Session Fixation"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABLE: Session ID not regenerated after login
        if username == 'admin' and password == 'admin123':
            session['user_id'] = 1
            session['username'] = username
            session['role'] = 'admin'
            return f"Login successful! Session ID: {session.get('session_id', 'NOT_REGENERATED')}"
        else:
            return "Login failed!"
    
    return '''
    <form method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <input type="submit" value="Login">
    </form>
    <p><small>Hint: Session ID should be regenerated after login</small></p>
    '''

@app.route('/auth-bypass', methods=['GET', 'POST'])
def authentication_bypass():
    """VULNERABLE: Authentication Bypass"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '')
        
        # VULNERABLE: Direct user ID manipulation
        if user_id.isdigit():
            session['user_id'] = int(user_id)
            session['username'] = f'user_{user_id}'
            session['role'] = 'admin' if user_id == '1' else 'user'
            return f"Authentication bypassed! User ID: {user_id}, Role: {session.get('role')}"
        else:
            return "Invalid user ID!"
    
    return '''
    <form method="post">
        <input type="text" name="user_id" placeholder="User ID" required>
        <input type="submit" value="Bypass Auth">
    </form>
    <p><small>Hint: Try different user IDs to bypass authentication</small></p>
    '''

@app.route('/debug')
def debug():
    """Debug endpoint - shows server information"""
    import platform
    import os
    
    # Cross-platform system information
    system_info = {
        'os': platform.system(),
        'os_version': platform.release(),
        'architecture': platform.machine(),
        'python_version': platform.python_version(),
        'server_uptime': '2 days, 14 hours, 32 minutes',
        'memory_usage': '45.2%',
        'cpu_usage': '12.8%',
        'disk_usage': '67.3%'
    }
    
    return jsonify({
        'server': 'Hacking Game Server v2.0',
        'status': 'running',
        'system_info': system_info,
        'vulnerabilities': [
            'SQL Injection in /login',
            'XSS in /comments',
            'Hidden API in /api/secret',
            'Admin panel in /admin',
            'Directory Traversal in /files',
            'File Upload in /upload',
            'CSRF in /admin/actions',
            'Session Fixation in /login',
            'Information Disclosure in /api/users',
            'Insecure Direct Object Reference in /documents',
            'SSRF in /ssrf',
            'Command Injection in /command',
            'LDAP Injection in /ldap',
            'NoSQL Injection in /nosql',
            'Race Condition in /race',
            'Business Logic Flaw in /business-logic',
            'Authentication Bypass in /auth-bypass'
        ],
        'hint': 'Look for configuration files on the server...',
        'level_1_hint': 'Check for .env files or configuration endpoints.',
        'level_2_hint': 'Scan for open ports and services. Try different nmap techniques.',
        'level_3_hint': 'Test SQL injection with various payloads. Try UNION-based attacks.',
        'level_4_hint': 'Look for XSS opportunities in forms and comments.',
        'level_5_hint': 'Analyze network traffic and memory dumps for forensics.'
    })

# =============================================
# FORENSICS ENDPOINTS FOR LEVEL 5
# =============================================

@app.route('/forensics')
def forensics():
    """Forensics analysis endpoint"""
    return jsonify({
        'forensics_data': 'Memory dump analysis available',
        'encryption_key': target_generator.get_target_value(5),
        'memory_dump': 'Available for analysis',
        'network_capture': 'Traffic logs captured',
        'file_system': 'Disk image ready for examination'
    })

@app.route('/memory')
def memory_analysis():
    """Memory analysis endpoint"""
    return jsonify({
        'memory_dump': 'System memory captured',
        'processes': ['hacking_server.py', 'python.exe', 'chrome.exe'],
        'encryption_key': target_generator.get_target_value(5),
        'suspicious_activity': 'Detected in memory'
    })

@app.route('/network')
def network_analysis():
    """Network forensics endpoint"""
    return jsonify({
        'network_capture': 'Traffic logs available',
        'connections': ['127.0.0.1:5000', '192.168.1.100:22'],
        'encryption_key': target_generator.get_target_value(5),
        'suspicious_traffic': 'Detected in network logs'
    })

@app.route('/files')
def file_analysis():
    """File system forensics endpoint"""
    return jsonify({
        'file_system': 'Disk image ready',
        'deleted_files': ['secret.txt', 'config.bak'],
        'encryption_key': target_generator.get_target_value(5),
        'suspicious_files': 'Found in file system'
    })

@app.route('/.env.local')
def env_file():
    """Environment file endpoint - contains the API key"""
    if target_generator:
        env_content = f"""# Environment Configuration
# This file contains sensitive configuration data
# DO NOT commit to version control!

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hacking_target
DB_USER=admin
DB_PASS=super_secret_password_123

# API Configuration
API_KEY={target_generator.get_target_value(2)}
API_SECRET=internal_use_only
API_ENDPOINT=http://api.target.local/v1

# Security Settings
JWT_SECRET=very_secure_jwt_key_here
SESSION_TIMEOUT=3600
ENABLE_DEBUG=false

# Application Settings
APP_NAME=Hacking Target Server
APP_VERSION=2.0.0
LOG_LEVEL=INFO
"""
        return env_content, 200, {'Content-Type': 'text/plain'}
    return "File not found", 404

# =============================================
# STATIC FILES AND TEMPLATES
# =============================================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return app.send_static_file(filename)

# =============================================
# SERVER MANAGEMENT
# =============================================

def create_templates():
    """Create HTML templates for the web interface"""
    templates_dir = 'templates'
    static_dir = 'static'

    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    # Main page
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Hacking Target Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 1000px; margin: 0 auto; }
        .warning { background: #ffebee; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .info { background: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .vuln-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .vuln-item { background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[TARGET] Hacking Target Server v2.0 - Echo's Ultimate Chaos</h1>
        <div class="warning">
            <h3>[!] SECURITY NOTICE</h3>
            <p>This server contains intentional security vulnerabilities for educational purposes.</p>
            <p><strong>DO NOT</strong> use these techniques on real systems without permission!</p>
        </div>
        <div class="info">
            <h3>[?] Available Vulnerabilities</h3>
            <div class="vuln-grid">
                <div class="vuln-item">
                    <h4>🔐 Authentication</h4>
                    <ul>
                        <li><a href="/login">/login</a> - SQL Injection</li>
                        <li><a href="/ldap">/ldap</a> - LDAP Injection</li>
                        <li><a href="/nosql">/nosql</a> - NoSQL Injection</li>
                        <li><a href="/auth-bypass">/auth-bypass</a> - Auth Bypass</li>
                    </ul>
                </div>
                <div class="vuln-item">
                    <h4>🌐 Web Application</h4>
                    <ul>
                        <li><a href="/comments">/comments</a> - XSS</li>
                        <li><a href="/ssrf">/ssrf</a> - SSRF</li>
                        <li><a href="/command">/command</a> - Command Injection</li>
                        <li><a href="/files/">/files/</a> - Directory Traversal</li>
                    </ul>
                </div>
                <div class="vuln-item">
                    <h4>💾 File & Data</h4>
                    <ul>
                        <li><a href="/upload">/upload</a> - File Upload</li>
                        <li><a href="/documents">/documents</a> - Document Access</li>
                        <li><a href="/api/users">/api/users</a> - Info Disclosure</li>
                        <li><a href="/.env.local">/.env.local</a> - Config Files</li>
                    </ul>
                </div>
                <div class="vuln-item">
                    <h4>🔍 Advanced</h4>
                    <ul>
                        <li><a href="/race">/race</a> - Race Condition</li>
                        <li><a href="/business-logic">/business-logic</a> - Logic Flaw</li>
                        <li><a href="/admin/actions">/admin/actions</a> - CSRF</li>
                        <li><a href="/debug">/debug</a> - Server Info</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>''')

    # Login page
    with open(os.path.join(templates_dir, 'login.html'), 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Login - Hacking Target</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .login-form { max-width: 400px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .form-group { margin: 10px 0; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 3px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        .error { color: red; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="login-form">
        <h2>Login to Target System</h2>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <p><small>Hint: Try SQL injection...</small></p>
    </div>
</body>
</html>''')

    # Dashboard
    with open(os.path.join(templates_dir, 'dashboard.html'), 'w') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Hacking Target</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .nav { margin: 20px 0; }
        .nav a { margin-right: 20px; color: #007bff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome, {{ username }}!</h1>
            <p>Role: {{ role }}</p>
        </div>
        <div class="nav">
            <a href="/documents">Documents</a>
            <a href="/comments">Comments</a>
            {% if role == 'admin' %}
            <a href="/admin">Admin Panel</a>
            {% endif %}
            <a href="/logout">Logout</a>
        </div>
    </div>
</body>
</html>''')

    # Documents page
    with open(os.path.join(templates_dir, 'documents.html'), 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Documents - Hacking Target</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .document { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 3px; }
        .classification { font-weight: bold; color: #d63384; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[DOCUMENTS] Available Documents</h1>
        {% for doc in documents %}
        <div class="document">
            <h3>{{ doc[0] }}</h3>
            <p>Classification: <span class="classification">{{ doc[1] }}</span></p>
            <p><a href="/api/documents/{{ doc[0] }}">View Content</a></p>
        </div>
        {% endfor %}
    </div>
</body>
</html>''')

    # Comments page
    with open(os.path.join(templates_dir, 'comments.html'), 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Comments - Hacking Target</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .comment { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .comment-form { background: #e3f2fd; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .form-group { margin: 10px 0; }
        textarea { width: 100%; height: 100px; padding: 8px; border: 1px solid #ddd; border-radius: 3px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[COMMENTS] Comments System</h1>
        <div class="comment-form">
            <h3>Add Comment</h3>
            <form method="POST">
                <div class="form-group">
                    <textarea name="comment" placeholder="Enter your comment..." required></textarea>
                </div>
                <button type="submit">Post Comment</button>
            </form>
            <p><small>Hint: Try XSS payloads...</small></p>
        </div>
        <h3>Recent Comments</h3>
        {% for comment in comments %}
        <div class="comment">
            <strong>{{ comment[0] }}</strong> ({{ comment[2] }})
            <p>{{ comment[1] | safe }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>''')

    # Admin page
    with open(os.path.join(templates_dir, 'admin.html'), 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel - Hacking Target</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .admin-panel { background: #ffebee; padding: 20px; border-radius: 5px; }
        .warning { background: #fff3e0; padding: 15px; border-radius: 3px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="admin-panel">
            <h1>[ADMIN] Admin Control Panel</h1>
            <div class="warning">
                <h3>[!] HIGHLY SENSITIVE AREA</h3>
                <p>This area contains sensitive administrative functions.</p>
                <p>Access to this panel should be restricted to authorized personnel only.</p>
            </div>
            <h3>Available Functions:</h3>
            <ul>
                <li>User Management</li>
                <li>System Configuration</li>
                <li>Security Monitoring</li>
                <li>Data Backup</li>
            </ul>
            <p><a href="/api/admin/data">View Admin Data (API)</a></p>
        </div>
    </div>
</body>
</html>''')

def start_server():
    """Start the Flask development server"""
    print("🚀 Starting Hacking Target Server...")
    print(f"📍 Server: {PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}")
    print(f"🔍 Debug endpoint: {PROTOCOL}://{SERVER_HOST}:{SERVER_PORT}/debug")
    print("⚠️  Server contains intentional vulnerabilities for educational purposes!")

    # Create templates before starting server
    create_templates()

    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG_MODE)

# =============================================
# MAIN EXECUTION
# =============================================

if __name__ == '__main__':
    # Initialize database
    init_database()

    # Generate target values for this session
    session_id = str(uuid.uuid4())
    target_generator = TargetValueGenerator(session_id)

    print("🎯 Target Values Generated:")
    print(f"   Level 1: {target_generator.get_target_value(1)}")
    print(f"   Level 2: {target_generator.get_target_value(2)}")
    print(f"   Level 3: {target_generator.get_target_value(3)[:16]}...")
    print(f"   Level 4: {target_generator.get_target_value(4)[:16]}...")
    print(f"   Level 5: {target_generator.get_target_value(5)[:16]}...")

    # Create secret file for Level 1
    create_secret_file()

    # Start server
    start_server()
