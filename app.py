from flask import Flask, request
import psycopg2

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=5000)
