import os
from flask import Blueprint, render_template,session,redirect,url_for,current_app
import mysql.connector

admin_bp = Blueprint('admin',__name__)
@admin_bp.route('/admin')
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login.login'))  # your login route name
    name = session.get('name')
    config = current_app.config['DB_CONFIG']
    db = None
    cursor = None
    try:
        # --- Connect to the database for this specific request ---
        db = mysql.connector.connect(**config)
        cursor = db.cursor(dictionary=True)

        # --- Query total students ---
        cursor.execute("SELECT COUNT(*) AS total_students FROM students")
        total_students = cursor.fetchone()['total_students']

        # --- More efficient query for room occupancy ---
        cursor.execute("""
            SELECT 
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'occupied' THEN 1 ELSE 0 END) AS occupied
            FROM rooms
        """)
        room_data = cursor.fetchone()
        if room_data and room_data['total'] > 0:
            occupancy = round((room_data['occupied'] / room_data['total']) * 100, 2)
        else:
            occupancy = 0

        # --- Query pending complaints (with better error handling) ---
        cursor.execute("SELECT COUNT(*) AS pending FROM complaints WHERE status='Pending'")
        pending_row = cursor.fetchone()
        pending_complaints = pending_row['pending'] if pending_row else 0
        
        # --- Query total fees collected (with better error handling) ---
        cursor.execute("SELECT SUM(amount) AS total_fees FROM fees")
        fees_result = cursor.fetchone()
        total_fees = fees_result['total_fees'] if fees_result and fees_result['total_fees'] is not None else 0

        # --- Query recent complaints ---
        cursor.execute("""
            SELECT CONCAT(r.block_name,'-',r.room_no) AS room_no, c.category, c.status
            FROM complaints c
            JOIN rooms r ON c.room_id = r.room_id
            ORDER BY c.created_at DESC
            LIMIT 5
        """)
        complaints = cursor.fetchall()
        print(complaints)
        cursor.execute("""SELECT 
                    SUM(CASE WHEN r.block_name = 'A' THEN 1 ELSE 0 END) AS block_a_student_count,
                    SUM(CASE WHEN r.block_name = 'B' THEN 1 ELSE 0 END) AS block_b_student_count,
                    SUM(CASE WHEN r.block_name = 'C' THEN 1 ELSE 0 END) AS block_c_student_count,
                    SUM(CASE WHEN r.block_name = 'D' THEN 1 ELSE 0 END) AS block_d_student_count
                    FROM students s
                    JOIN rooms r ON s.room_id = r.room_id;
                """)
        counts = cursor.fetchone()
        block_A = counts.get('block_a_student_count', 0) if counts else 0
        block_B = counts.get('block_b_student_count', 0) if counts else 0
        block_C = counts.get('block_c_student_count', 0) if counts else 0
        block_D = counts.get('block_d_student_count', 0) if counts else 0
        
        block_counts=[int(block_A),int(block_B),int(block_C),int(block_D)]
        print("Block counts:", block_counts)
    finally:
        # --- Always close the cursor and connection to release resources ---
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

    # Send data to HTML
    return render_template(
        'admin_panel.html',
        total_students=total_students,
        occupancy=occupancy,
        pending_complaints=pending_complaints,
        total_fees=total_fees,
        complaints=complaints,
        data = name,
        block_counts = block_counts

    )
