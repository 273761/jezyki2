from flask import Flask, send_file, jsonify, send_from_directory
import pyodbc
import os

app = Flask(__name__, static_folder='static')

# Konfiguracja połączenia SQL
server = 'serwer-jezyki.database.windows.net,1433'
database = 'bazaJezyki'
username = 'adminlogin273761'
password = 'Password273761'
driver = '{ODBC Driver 18 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
conn = pyodbc.connect(conn_str)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route("/ile-niemiecki")
def ile_niemiecki():
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(CAST(REPLACE(liczbaUczniow, ' ', '') AS INT)) FROM [dbo].[tabelaJezyki] WHERE jezykObcy = 'niemiecki'")
    result = cursor.fetchone()
    return jsonify({"count": result[0] if result else 0})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
