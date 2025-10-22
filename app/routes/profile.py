import os
from flask import Flask,Blueprint,session,redirect,url_for,render_template,request,flash,current_app
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash
profile_bp=Blueprint('profile',__name__)
@profile_bp.route('/profile')
def profile_information():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    name = session.get('name')
    email = session.get('username')
    print(email)
    print(name)
    return render_template('profile.html',name = name,email=email)
@profile_bp.route('/profile/edit_profile',methods=["POST"])
def edit_profile():
    name = request.form.get('fullName')
    email = request.form.get('email_address')
    config = current_app.config['DB_CONFIG']
    try:
        db=mysql.connector.connect(**config)
        cursor = db.cursor()
        cursor.execute("""
                        UPDATE users
                        SET name = %s ,email =%s
                        WHERE email=%s; 
                """,(name,email,session.get('username')))
        db.commit()
        session['name']=name
        session['username']=email
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return redirect(url_for('profile.profile_information'))
@profile_bp.route('/profile/change_password',methods=["POST"])
def change_password():
    currentPassword=request.form.get('currentPassword')
    newPassword=request.form.get('newPassword')
    confirmNewPassword = request.form.get('confirmNewPassword')
    email = session.get('username')
    config = current_app.config['DB_CONFIG']
    if newPassword != confirmNewPassword:
        flash("New password and confirm password do not match.", "danger")
        return redirect(url_for('profile.profile_information'))
    try:
        db=mysql.connector.connect(**config)
        cursor=db.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE email=%s",(email,))
        row=cursor.fetchone()
        if not row:
            flash("User not found!", "danger")
            return redirect(url_for('profile.profile_information'))
        stored_hash = row[0]
        if not check_password_hash(stored_hash,currentPassword):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('profile.profile_information'))
        new_hash=generate_password_hash(newPassword)
        cursor.execute("UPDATE users SET password_hash =%s WHERE email=%s",(new_hash,email))
        db.commit()
        flash("Password updated successfully!", "success")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    return redirect(url_for('profile.profile_information'))