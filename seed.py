import mysql.connector
from mysql.connector import errorcode
import os 
import csv
import uuid

def connect_db():
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="c@Zajoel5864"
    )
        print("Datababse connected successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS ALS_prodev"
        )
        print("Database ALX_prodev successfully created or already exists")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="c@Zajoel5864",
            database="ALX_prodev"
        )
        print("Connected to ALX_prodev successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None
    
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
             """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL
        )
        """
        )
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    try:
        if not os.path.exists(csv_file):
            print("File does not exist/ file path is incorrect")
            return
        
        cursor = connection.cursor()

        with open (csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = int(row['age'])

                insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
                cursor.execute(insert_query, (user_id, name, email, age))

        connection.commit()
        print("Data inserted successfully")
    except FileNotFoundError:
        print(f"Error: {csv_file} not found")
    except csv.Error as err:
        print(f"CSV Reading Error: {err}")
        if connection.is_connected():
            connection.rollback()
    except Exception as err:
        print(f"Unexpected error: {err}")
        if connection.is_connected():
            connection.rollback()
    finally:
        cursor.close()
