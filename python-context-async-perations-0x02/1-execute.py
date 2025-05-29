import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params):
        self.query = query
        self.params = params
        self.db_name = db_name
        self.cursor = None
        self.conn = None
        self.result = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"Error: {exc_val}")
        return False
    
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as result:
    for row in result:
        print(row)