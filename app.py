from flask import Flask, request
import psycopg2
import time

app = Flask(__name__)

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                host="db",
                database="mydatabase",
                user="myuser",
                password="mypassword"
            )
            conn.close()
            print("Connected to the database.")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Waiting for database...")
            time.sleep(2)

def create_table_if_not_exists():
    conn = psycopg2.connect(
        host="db",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reversed_ips (
            id SERIAL PRIMARY KEY,
            ip VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def store_ip(ip):
    conn = psycopg2.connect(
        host="db",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reversed_ips (ip) VALUES (%s)", (ip,))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def reverse_ip():
    client_ip = request.remote_addr
    reversed_ip = ".".join(client_ip.split(".")[::-1])
    store_ip(reversed_ip)
    return reversed_ip

if __name__ == '__main__':
    wait_for_db()
    create_table_if_not_exists()
    app.run(host='0.0.0.0', port=5000)
