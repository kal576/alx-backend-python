import sqlite3

class DatabaseConnection:
    #replace db_name with the actual database name
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name) #replace db_name with the actual database name
        self.cursor = self.conn.cursor()
        print("Successfully connected to database")
        return self.cursor()    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"Error: {exc_val}")
        return False

with DatabaseConnection("users.db") as cursor:
    query = """ 
            SELECT * FROM users"""
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
