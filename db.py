import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "login_db"

    )

    return connection


