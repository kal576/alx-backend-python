from seed import connect_to_prodev
from mysql.connector import Error

def stream_users():
    connection = None

    try:
        connection = connect_to_prodev()
        if connection.is_connected():
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_data")

                row = cursor.fetchone()
                while row:
                    yield row
                    row = cursor.fetchone()
    except Error as err:
        print(f"Error: {err}")
    finally:
        if connection and connection.is_connected():
            connection.close()
