from flask import Flask, render_template, request
import mysql.connector
from db import connect_db

app = Flask(__name__)


#Display login page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods = ["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    connection = connect_db()
    cursor = connection.cursor()

    #Save user input into database

    cursor.execute(
        "INSERT INTO cridentials (email, password) VALUES (%s, %s)", (email, password)
    )

    connection.commit()

    #Retrieve saved data from database


    cursor.close()
    connection.close()

    return render_template("record_student.html")


#Display student registration form

@app.route("/record")
def record():
    return render_template("record_student.html")

#Save student's information

@app.route("/record", methods = ["POST"])
def save_students():
    name = request.form["student_name"]
    admission = request.form["admission_number"]
    total = float(request.form["total_fees"])
    paid = float(request.form["amount_paid"])

    balance = total - paid

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO students_fee(student_name, admission_number, total_fees, amount_paid, balance) VALUES (%s, %s, %s, %s, %s)",
        (name, admission, total, paid, balance)
    )

    connection.commit()

    cursor.execute("SELECT * FROM students_fee")

    students_fee = cursor.fetchall()


    cursor.close()
    connection.close()

    return render_template ("students_fees.html", students_fee = students_fee)







if __name__ == "__main__":
    app.run(debug=True)


