from flask import Flask, send_file, jsonify
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv('hasla.env')

app = Flask(__name__)

# Konfiguracja połączenia SQL z pliku .env
server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')
driver = 'ODBC Driver 18 for SQL Server'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
conn = pyodbc.connect(conn_str)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/ile-niemiecki")
def ile_niemiecki():
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(CAST(REPLACE(liczbaUczniow, ' ', '') AS INT)) FROM [dbo].[tabelaJezyki] WHERE jezykObcy = 'niemiecki'")
    result = cursor.fetchone()
    return jsonify({"count": result[0] if result else 0})

if __name__ == "__main__":
    app.run(debug=True)
