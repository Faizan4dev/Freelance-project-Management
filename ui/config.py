import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Faizan123@",
            database="fpms"
        )
        print("✅ Connected to the database successfully!")
        return connection
    except mysql.connector.Error as err:
        print("❌ Failed to connect:", err)
        return None

print("✅ config.py loaded")