from mysql.connector import Error
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    try:
        connection = connect_to_prodev()

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

def batch_processing(batch_size):

    filtered_users = []

    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age']>25:
                filtered_users.append(user)
    
    for user in filtered_users:
        print(user)
    
    return filtered_users