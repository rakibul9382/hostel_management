import os
import mysql.connector
from flask import Flask,Blueprint,render_template,session,redirect,url_for,request,current_app
mess_bp = Blueprint('mess',__name__)
@mess_bp.route("/mess")
def mess():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    db = None
    Cursor = None
    data = []
    config = current_app.config['DB_CONFIG']
    try:
        db = mysql.connector.connect(**config)
        Cursor=db.cursor(dictionary=True)
        Cursor.execute("""SELECT* FROM mess_menu""")
        data = Cursor.fetchall()
        print(data)

    finally:
        if Cursor:
            Cursor.close()
        if db:
            db.close()
    return render_template('mess.html',
                    menu = data)

@mess_bp.route('/mess/update',methods=["POST"])
def update_menu():
    day=request.form.get('day')
    breakfast = request.form.get('breakfast')
    launch = request.form.get('lunch')
    dinner = request.form.get('dinner')
    config = current_app.config['DB_CONFIG']
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    cursor.execute("""
                    UPDATE mess_menu
                    SET breakfast=%s, launch=%s, dinner=%s
                    WHERE day_name = %s
                """,(breakfast,launch,dinner,day))
    db.commit()
    db.close()
    return redirect(url_for('mess.mess'))