from db import connect_db
from werkzeug.security import generate_password_hash
from getpass import getpass

#Get bursar details
username = input("Enter username: ")
email = input("Enter email: ")

password = getpass("Enter password: ")
confirm_password = getpass("Confirm password: ")

role = input("Enter your role: ")

#check password

if password != confirm_password:
    print("password do not match!")
    raise SystemExit

#Hash the password 
hashed_password = generate_password_hash(password)

#Connect to database
connection = connect_db()
cursor = connection.cursor()

#save bursor details

cursor.execute(
    "INSERT INTO bursar_details(username, email, password, role) VALUES (%s, %s, %s, %s)",
    (username, email, hashed_password, role)

)

connection.commit()

