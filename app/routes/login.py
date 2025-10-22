import os
from flask import Flask,Blueprint,render_template,request,session,redirect,url_for,current_app
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
login_bp = Blueprint('login',__name__)
# --- Store DB config in a dictionary ---

@login_bp.route('/login',methods=["GET","POST"])
def login():
    db = None
    cursor = None
    config = current_app.config['DB_CONFIG']
    msg = []
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        password_hash=generate_password_hash(password)
        print(password_hash)

    #now we try to connect database
        try:
            db=mysql.connector.connect(**config)
            cursor=db.cursor(dictionary=True)
            #query to find user
            cursor.execute("SELECT* FROM users WHERE email= %s",(email,))
            user=cursor.fetchone()

            #check if user exist and match the password
            if user and check_password_hash(user['password_hash'],password):
                session['username'] = user['email']
                session['name'] = user['name']   
                return redirect(url_for('admin.admin_dashboard'))
            else:
                msg = "invalid password or email"
                print(msg)
        except mysql.connector.Error as err:
            print("database error",err)
            msg = "something went wrong! please try again later"
        except Exception as e:
            print("unexpected error",e)
            msg="unexpected error occured"
        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
    return render_template('login.html',message=msg)
