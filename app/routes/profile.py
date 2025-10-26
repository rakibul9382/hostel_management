import os
from flask import Flask, Blueprint, session, redirect, url_for, render_template, request, flash, current_app
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid

# Add helper to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_profile_picture(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        file.save(filepath)
        return unique_name
    return None

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile_information():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    
    name = session.get('name')
    email = session.get('username')
    
    # Handle POST request (file upload)
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file'] 
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        config = current_app.config['DB_CONFIG']
        db = mysql.connector.connect(**config)
        cursor = db.cursor(dictionary=True)
        
        filename = save_profile_picture(file)
        if filename:
            cursor.execute("UPDATE users SET profile_pic = %s WHERE email=%s", (filename, email))
            db.commit()
            flash('Profile picture uploaded successfully!', 'success')
        else:
            flash('Invalid file format!', 'danger')
        
        cursor.close()
        db.close()
        return redirect(url_for('profile.profile_information'))
    
    # Handle GET request (display profile)
    config = current_app.config['DB_CONFIG']
    db = mysql.connector.connect(**config)
    cursor = db.cursor(dictionary=True)
    
    try:
        # Fetch current user info - using only available columns
        cursor.execute("SELECT name, profile_pic FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

    except Exception as e:
        flash(f"Database error: {str(e)}", "danger")
        user = None
    finally:
        cursor.close()
        db.close()

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for('login.login'))

    profile_pic = user.get('profile_pic', 'default.png')
    
    # Get display name - use name from database or session
    display_name = user.get('name') or name or email.split('@')[0]  # Use email username part as fallback

    return render_template('profile.html', 
                         username=display_name, 
                         name=display_name, 
                         email=email, 
                         profile_pic=profile_pic)

# Edit profile route
@profile_bp.route('/profile/edit_profile', methods=["POST"])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login.login'))
        
    name = request.form.get('fullName')
    email = request.form.get('email_address')
    config = current_app.config['DB_CONFIG']
    
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        
        # Update name and email
        cursor.execute("""
            UPDATE users 
            SET name = %s, email = %s 
            WHERE email = %s
        """, (name, email, session.get('username')))
            
        db.commit()
        session['name'] = name
        session['username'] = email
        flash("Profile updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating profile: {str(e)}", "danger")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return redirect(url_for('profile.profile_information'))

# Change password route (unchanged)
@profile_bp.route('/profile/change_password', methods=["POST"])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login.login'))
        
    currentPassword = request.form.get('currentPassword')
    newPassword = request.form.get('newPassword')
    confirmNewPassword = request.form.get('confirmNewPassword')
    email = session.get('username')
    config = current_app.config['DB_CONFIG']
    
    if newPassword != confirmNewPassword:
        flash("New password and confirm password do not match.", "danger")
        return redirect(url_for('profile.profile_information'))
    
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE email=%s", (email,))
        row = cursor.fetchone()
        
        if not row:
            flash("User not found!", "danger")
            return redirect(url_for('profile.profile_information'))
            
        stored_hash = row[0]
        if not check_password_hash(stored_hash, currentPassword):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('profile.profile_information'))
            
        new_hash = generate_password_hash(newPassword)
        cursor.execute("UPDATE users SET password_hash = %s WHERE email=%s", (new_hash, email))
        db.commit()
        flash("Password updated successfully!", "success")
    except Exception as e:
        flash(f"Error changing password: {str(e)}", "danger")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
            
    return redirect(url_for('profile.profile_information'))