import mysql.connector
from mysql.connector import Error

def stream_users():
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

                row = cursor.fetchone()
                while row:
                    yield row
                    row = cursor.fetchone()
    except Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            connection.close()
