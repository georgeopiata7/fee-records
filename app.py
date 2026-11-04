from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

import mysql.connector
from db import connect_db

app = Flask(__name__)
app.secret_key = "my_secret_key"


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

    return render_template("bursar_login.html")


#Display student registration form

@app.route("/bursar_login", methods = ["GET", "POST"])
def bursar_login():
    if request.method == "POST":

        #Get details entered by the bursar

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]


        # connect database

        connection = connect_db()

        cursor = connection.cursor()

        #Find bursar

        cursor.execute(
            "SELECT password , role FROM bursar_details WHERE username = %s", 
            (username,)

        )

        bursar = cursor.fetchone()

        #Check username, password and role

        if bursar and check_password_hash(bursar[0], password) and bursar[1].lower() == "bursar":
            session["bursar"] = username

            cursor.close()
            connection.close()

            return render_template("record_student.html")

        else:
            cursor.close()
            connection.close()

            return "Invalid username or password!"
    return render_template("bursar_login.html")



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


    connection = connect_db()
    cursor = connection.cursor()

    #check if student already exist



    cursor.execute(
        "SELECT * FROM  students_fee WHERE  admission_number = %s ",
        (admission,)

    )
    student = cursor.fetchone()

    if student:
        #add new payment to previous payment

        new_paid = float(student[4]) + paid
        balance  = float(student[3]) - new_paid

        cursor.execute(
            "UPDATE students_fee SET amount_paid = %s, balance = %s WHERE admission_number = %s",
            (new_paid, balance, admission)
        )

    else: 
        #Record a new student

        balance = total - paid

        cursor.execute(
            "INSERT INTO students_fee(student_name, admission_number, total_fees, amount_paid, balance) VALUES(%s, %s, %s, %s, %s)",
            (name, admission, total, paid, balance)
        )

    connection.commit()


    #Display students from A-Z
    cursor.execute(
        "SELECT * FROM students_fee ORDER BY student_name ASC"
    )

    

    students_fee = cursor.fetchall()


    cursor.close()
    connection.close()

    return render_template ("students_fees.html", students_fee = students_fee)

@app.route("/students")
def view_students():
    connection = connect_db()
    cursor = connection.cursor()

    #Retrieve all students from A-z
    cursor.execute(
        "SELECT * FROM students_fee ORDER BY student_name ASC"
         
     )
    students_fee = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("students_fees.html", students_fee = students_fee)


@app.route("/search", methods = ["POST"])
def search_student():
    search = request.form["search"]

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students_fee WHERE student_name LIKE %s",
        ("%" + search +  "%",)
    )
    students_fee = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("students_fees.html" ,students_fee = students_fee)

@app.route("/make_payment", methods=["GET", "POST"])
def make_payment():
    if request.method == "POST":
        admission = request.form["admission_number"]

        connection = connect_db()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students_fee WHERE admission_number = %s",
            (admission)
        )

        student = cursor.fetchone()
        cursor.close()
        connection.close()

        if student:

            return render_template(
                "make_payment.html",
                student = None,
                message = None
            )
        else:
            return render_template(
                "make_payment.html",
                message = "Student Not Found"
            )
    return render_template("make_payment.html")
    







if __name__ == "__main__":
    app.run(debug=True)


