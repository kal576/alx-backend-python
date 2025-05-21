import time
import sqlite3 
import functools
import logging

query_cache = {}

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

def cache_query(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        if query in query_cache:
            logging.info(f"Cache hit for {query}")
            return query_cache[query]
        logging.info(f"No cache result. Executing {query}:")
        result = func(query, *args, **kwargs)
        logging.info(f"Caching {query}:")
        query_cache[query] = result
        return result
    return wrapper
        

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")