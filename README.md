# py-flask-sqli

A simple Flask application demonstrating SQL injection vulnerability.

## ⚠️ Warning
This application is intentionally vulnerable to SQL injection attacks for educational purposes only. **DO NOT** use this code in production environments.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python init_db.py
```

3. Run the application:
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### API Endpoint

**GET** `/api/v1.0/<service>`

Requires `X-API-Key` header with value: `secret_key_123`

Example legitimate request:
```bash
curl -H "X-API-Key: secret_key_123" http://localhost:5000/api/v1.0/api
```

### SQL Injection Example

The application is vulnerable to SQL injection through the `service` parameter. Example:

```bash
curl -H "X-API-Key: secret_key_123" "http://localhost:5000/api/v1.0/api\" OR \"1\"=\"1"
```

This will bypass the service filter and return all records from the database.

## Vulnerability Details

The vulnerability exists in the `poke_service` function where user input is directly concatenated into the SQL query:

```python
query = f"""select rd
from data as rd
where rd.service = "{service.lower()}" """
```

This allows attackers to inject malicious SQL code through the `service` parameter.