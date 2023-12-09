import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("DB_URL")
port = 3306
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database = os.getenv("DB_NAME")


connection = mysql.connector.connect(
host=host,
port=port,
user=username,
password=password,
database=database
)

if connection.is_connected():
    print("Conexão bem-sucedida!")
else:
    print("Não foi possível conectar ao banco de dados.")

