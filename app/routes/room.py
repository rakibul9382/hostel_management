import os
from flask import Flask, request, render_template, Blueprint,session,redirect,url_for,current_app
import mysql.connector

room_bp = Blueprint('room', __name__)

@room_bp.route('/rooms')
def rooms_details():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    db = None
    cursor = None
    rooms_data = []
    config = current_app.config['DB_CONFIG']
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(dictionary=True)

        block_filter = request.args.get('block')
        status_filter = request.args.get('status')

        # This query is still needed to get occupant names for display
        sql = """
            SELECT 
                r.room_id,
                CONCAT(r.block_name, '-', r.room_no) AS room_number,
                r.type,
                r.capacity,
                r.status,  -- It's good practice to select the column you filter on
                COUNT(s.student_id) AS current_occupants,
                GROUP_CONCAT(s.name SEPARATOR ', ') AS occupant_names
            FROM rooms r
            LEFT JOIN students s ON r.room_id = s.room_id
        """
        
        where_conditions = []
        params = []

        # Add block filter if selected
        if block_filter:
            where_conditions.append("r.block_name = %s")
            params.append(block_filter)
        
        # --- NEW SIMPLIFIED FILTER LOGIC ---
        # Filter directly on the `rooms.status` column. This is the fix.
        if status_filter == 'empty':
            where_conditions.append("r.status = %s")
            params.append('empty')
        elif status_filter == 'Occupied':
            # The value from your HTML is 'Occupied', but the DB stores 'occupied'
            where_conditions.append("r.status = %s")
            params.append('occupied') 

        if where_conditions:
            sql += " WHERE " + " AND ".join(where_conditions)

        # We still need GROUP BY for the COUNT and GROUP_CONCAT aggregations
        sql += " GROUP BY r.room_id, r.room_no, r.block_name, r.type, r.capacity, r.status"
        
        sql += " ORDER BY r.block_name, r.room_no"

        cursor.execute(sql, params)
        rooms_data = cursor.fetchall()
        print("Fetched rooms data:", rooms_data) # For debugging

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

    return render_template('rooms.html', rooms=rooms_data)