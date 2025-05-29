import time
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

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                    logging.info(f"Attempt {attempt+1}")
                    return result
                except Exception as err:
                    logging.error(f"Error in attempt {attempt+1}: {err}")
                    if attempt < retries - 1:
                        logging.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logging.error(f"Failed to resolve error: {err}")
                        logging.info(f"Total attempts: {attempt+1}")
                        raise
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)