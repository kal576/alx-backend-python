from mysql.connector import Error
from seed import connect_to_prodev

def stream_user_ages():
    
    connection = None
    try:
        connection = connect_to_prodev()

        if connection.is_connected():
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_data")

                row = cursor.fetchone()
                while row:
                    yield row['age']
                    row = cursor.fetchone()
    
    except Error as err:
        print(f"Error: {err}")
    finally:
        if connection and connection.is_connected():
            connection.close()

def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        print("No users found")
        return
    
    average_age = total_age/count
    print(f"The average age is {average_age}")

if __name__ == "__main__":
    calculate_average_age()


