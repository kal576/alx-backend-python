import sqlite3
import functools
import time
import logging

#### decorator to lof SQL queries

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_queries(func):
    ##the logging info shou contain: 1. query name 2. time taken 3. any error
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            query = args[0]
        else:
            query = kwargs.get('query', 'Unknown query')

        logging.info(f"Executing {query}")
        start_time = time.time()
        
        try:
            #Log the query
            #assign a variable name to the function to call later
            result = func(*args, **kwargs)
            time_elapsed = time.time() - start_time
            logging.info(f"Query {query} Executed Successfully")
            logging.info(f"Time Taken: {time_elapsed:.4f} seconds")
            return result
        except Exception as e:
            logging.error(f"Error executing query: {query}")
            logging.error(f"Exception: {e}")
            raise     
    return wrapper

        

      


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
