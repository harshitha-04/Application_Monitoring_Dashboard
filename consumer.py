from kafka import KafkaConsumer
import json
import mysql.connector
from mysql.connector import Error

# Kafka consumer
consumer = KafkaConsumer(
    'api-logs',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='harshi1412',
        database='logdb'
    )
    # After the connection is established
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    method VARCHAR(10),
    url TEXT,
    status INT,
    duration FLOAT,
    error BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
    print("Table 'logs' created or already exists.")

# Check the current database
    cursor.execute("SELECT DATABASE();")
    print("Connected to database:", cursor.fetchone())

# Check the tables in the database
    cursor.execute("SHOW TABLES;")
    print("Tables in logdb:", cursor.fetchall())

    print("MySQL connection successful.")
except Error as e:
    print("Error while connecting to MySQL:", e)
    exit(1)

cursor.execute("SELECT DATABASE();")
db = cursor.fetchone()
print(f"Connected to database: {db[0]}")

# Insert statement
insert_stmt = """
INSERT INTO logs (method, url, status, duration, error)
VALUES (%s, %s, %s, %s, %s)
"""

print("Starting consumer...")

for message in consumer:
    try:
        log = message.value
        data = (
            log.get("method"),
            log.get("url"),
            log.get("status"),
            log.get("duration"),
            log.get("error")
        )
        cursor.execute(insert_stmt, data)
        conn.commit()
        print("Inserted log:", data)
    except Exception as e:
        print("Error inserting log:", e)
        conn.rollback()  # In case of error, rollback the transaction
