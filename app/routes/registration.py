import os
from flask import Flask,render_template,Blueprint,redirect,request,flash,current_app
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
registration_bp=Blueprint('registration',__name__)
@registration_bp.route('/registration',methods=["GET","POST"])
def register():
    config = current_app.config['DB_CONFIG']
    if request.method == "POST":
        full_name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('phone')
        password = request.form.get('password')
    
        # Basic validation
        if not all([full_name, email, phone_number, password]):
            flash("All fields are required!", "danger")
            return render_template('register.html')

        password_hash = generate_password_hash(password)

        db = None
        cursor = None

        try:
            db=mysql.connector.connect(**config)
            cursor = db.cursor(dictionary=True)
            #---check user is already exist---
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email address is already taken","warning")
                return render_template('register.html')

            sql="""
                INSERT INTO USERS(email,password_hash,name,mobile_no)
                VALUES(%s,%s,%s,%s)
            """
            cursor.execute(sql,(email,password_hash,full_name,phone_number))
            db.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect('/login') # Redirect to the login page
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            flash("An error occurred. Please try again.", "danger")
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    return render_template('register.html')