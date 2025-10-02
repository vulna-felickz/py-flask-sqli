import sqlite3

def init_database():
    """Initialize the database with sample data"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL,
            rd TEXT NOT NULL
        )
    ''')
    
    # Insert sample data
    sample_data = [
        ('api', 'API service is running'),
        ('database', 'Database service is healthy'),
        ('cache', 'Cache service is operational'),
        ('auth', 'Authentication service is active'),
        ('web', 'Web service is up')
    ]
    
    cursor.executemany('INSERT INTO data (service, rd) VALUES (?, ?)', sample_data)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
