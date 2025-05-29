import sqlite3 
import functools
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #define the connection
        conn = sqlite3.connect('user')
        logging.info("Connected to {database}")

        try:
            return func(conn, *args, **kwargs)
        except Exception as err:
            logging.info(f"Error: {err}")
            raise
        finally:
            #close the connection
            conn.close()
            logging.info("Connection to {database} closed")
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)