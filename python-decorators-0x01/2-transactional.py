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

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('database')

        try:
            #commit if there is no error
            conn.commit()
            logging.info("Transaction Committed Successfully")
            return func(conn, *args, **kwargs)
        except Exception as err:
            #rollback if an error occurs
            conn.rollback()
            logging.info("Error: {err}")
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')