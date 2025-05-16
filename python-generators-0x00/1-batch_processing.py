import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "c@Zajoel5864",
            database = "ALX_prodev"
        )
    try:
        if connection.is_connected():
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_data")

                batch = []
                row = cursor.fetchone()

                while row:
                    batch.append(row)
                    if len(batch) == batch_size:
                        yield batch
                        batch = []
                    row = cursor.fetchone()

                if batch:
                    yield batch

    except Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            connection.close()
