import pymysql
import bcrypt
from pymysql import MySQLError
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "rootpass"),
    "charset": "utf8mb4",
}

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

USERS = [
    ("user1", "user1pw"),
    ("user2", "user2pw"),
    ("user3", "user3pw"),
]

CONTAINERS = [
    ("CXXU7788345", 15000.00),
    ("VTYU8765678", 18500.50),
    ("ABCU1234567", 12000.75),
    ("DEEU9876543", 21000.00),
    ("FGHU5556667", 16750.25),
    ("HIJU4443332", 14200.80),
    ("KLMU1112223", 19999.99),
    ("NOPU7778889", 13400.00),
    ("QRSTU654321", 22500.45),
    ("UVWXU112233", 17800.33),
]

def main():
    connection = None
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS atk CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    cursor.execute(f"USE atk;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash CHAR(60) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;""")

    for username, password in USERS:
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed)
        )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS containers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            container_number CHAR(11) UNIQUE NOT NULL,
            cost DECIMAL(10,2) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_container_number (container_number),
            INDEX idx_cost (cost)
        ) ENGINE=InnoDB;""")

    for number, cost in CONTAINERS:
        cursor.execute(
            "INSERT INTO containers (container_number, cost) VALUES (%s, %s)",
            (number, round(cost, 2))
        )

    connection.commit()

    if connection:
        connection.close()

if __name__ == "__main__":
    main()