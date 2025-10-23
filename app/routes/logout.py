from flask import Flask,redirect,render_template,Blueprint,session,url_for,flash
logout_bp = Blueprint('logout',__name__)

@logout_bp.route('/logout')
def logout():
    session.clear() # Clear the session manually
    flash('You have been logged out.', 'info')
    return redirect(url_for('home.index')) # Redirect to the login page route