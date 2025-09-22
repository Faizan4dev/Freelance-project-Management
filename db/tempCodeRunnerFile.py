import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.config import connect_to_db

import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOurPAssword"
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_tables():
    conn = connect_to_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS fpms")
        cursor.execute("USE fpms")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                company VARCHAR(100),
                contact_number VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS freelancers (
                freelancer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                bio TEXT,
                rating FLOAT DEFAULT 0,
                contact_number VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                skill_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS freelancer_skills (
                freelancer_id INT,
                skill_id INT,
                PRIMARY KEY (freelancer_id, skill_id),
                FOREIGN KEY (freelancer_id) REFERENCES freelancers(freelancer_id) ON DELETE CASCADE,
                FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT,
                title VARCHAR(150) NOT NULL,
                description TEXT,
                budget DECIMAL(10,2),
                status ENUM('open', 'in progress', 'completed', 'cancelled') DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                application_id INT AUTO_INCREMENT PRIMARY KEY,
                project_id INT,
                freelancer_id INT,
                cover_letter TEXT,
                proposed_budget DECIMAL(10,2),
                status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
                FOREIGN KEY (freelancer_id) REFERENCES freelancers(freelancer_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                rating_id INT AUTO_INCREMENT PRIMARY KEY,
                client_id INT,
                freelancer_id INT,
                project_id INT,
                rating INT CHECK (rating BETWEEN 1 AND 5),
                review TEXT,
                rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(client_id),
                FOREIGN KEY (freelancer_id) REFERENCES freelancers(freelancer_id),
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        print("✅ All tables created successfully in database 'freelance_db'.")

    except Error as e:
        print(f"❌ Error while creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()

