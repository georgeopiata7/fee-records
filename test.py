from db import connect_db

try:
    connection = connect_db()
    print("Database connected successfully")


    connection.close()
except Exception as error:
    print("connection failed:", error)

    