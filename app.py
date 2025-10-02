from flask import Flask, request, jsonify
import sqlite3
from functools import wraps

app = Flask(__name__)

# Simple API key for demonstration
API_KEY = "secret_key_123"

def require_api_key():
    """Decorator to require API key in requests"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            if api_key != API_KEY:
                return jsonify({"error": "Invalid or missing API key"}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def execute_query(query):
    """Execute SQL query and return results"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results
    except Exception as e:
        conn.close()
        raise e

@app.route('/api/v1.0/<service>', methods=['GET'])
@require_api_key()
def poke_service(service):
    """
    Vulnerable endpoint that accepts service parameter
    and constructs SQL query using string concatenation
    """
    # VULNERABLE: SQL injection through string concatenation
    query = f"""select rd
from data as rd
where rd.service = "{service.lower()}" """
    
    try:
        results = execute_query(query)
        return jsonify({
            "service": service,
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return jsonify({
        "message": "Flask SQL Injection Demo API",
        "endpoints": {
            "/api/v1.0/<service>": "GET - Poke a service (requires X-API-Key header)"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
