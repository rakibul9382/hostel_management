import os
from flask import Flask,Blueprint,session,redirect,url_for,render_template,request,jsonify,current_app
import mysql.connector
complaint_bp = Blueprint("complaint",__name__)
@complaint_bp.route('/complaint')
def complaint():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    db = None
    cursor = None
    COMPLAINT_DATA=[]
    config = current_app.config['DB_CONFIG']
    pending_count = 0
    inprogress_count = 0
    resolved_today_count = 0
    try:
        db=mysql.connector.connect(config)
        cursor=db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending_count,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) AS inprogress_count,
                SUM(CASE WHEN status = 'resolved' AND DATE(resolved_at) = CURDATE() THEN 1 ELSE 0 END) AS resolved_today_count
            FROM complaints
        """)
        counts = cursor.fetchone()
        if counts:
            pending_count = counts.get('pending_count', 0)
            inprogress_count = counts.get('inprogress_count', 0)
            resolved_today_count = counts.get('resolved_today_count', 0)
            
        # Debugging prints
        print(f"Counts: Pending={pending_count}, InProgress={inprogress_count}, ResolvedToday={resolved_today_count}")
        status_filter = request.args.get('status')
        print(status_filter)
        sql = """
            SELECT
                s.name AS Student,
                CONCAT(r.block_name,'-',r.room_no) AS Room_no,
                c.category AS Category,
                Date(c.created_at) AS Date_Submited,
                c.status AS Status,
                c.description
            FROM complaints c
            JOIN students s ON c.student_id = s.student_id
            JOIN rooms r ON c.room_id = r.room_id
        """
        
        params = []
        # Make filter case-insensitive and check against DB values
        if status_filter:
            sql += " WHERE c.status = %s"
            params.append(status_filter)
        cursor.execute(sql,params)
        COMPLAINT_DATA = cursor.fetchall()
        print("Fetched rooms data:", COMPLAINT_DATA) # For debugging

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
    return render_template('complaint.html',
                           table_information=COMPLAINT_DATA,
                           pending_case=pending_count,
                           inprogress_count = inprogress_count,
                           today_solve = resolved_today_count
                           )


@complaint_bp.route('/update_complaint_status', methods=['POST'])
def update_complaint_status():
    data = request.get_json()
    student = data['student']
    status = data['status']
    config = current_app.config['DB_CONFIG']

    try:
        db = mysql.connector.connect(config)
        cursor = db.cursor()
        cursor.execute("""
            UPDATE complaints c
            JOIN students s ON c.student_id = s.student_id
            SET c.status = %s
            WHERE s.name = %s
        """, (status, student))
        db.commit()
        return {"success": True}
    except Exception as e:
        print(f"An error occurred: {e}") # <-- ADD THIS!
        return jsonify({"success": False, "error": str(e)})
    finally:
        if cursor: cursor.close()
        if db: db.close()
