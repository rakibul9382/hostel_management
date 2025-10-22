import os
from flask import Flask,request,render_template,Blueprint,url_for,session,redirect,current_app
import mysql.connector
student_bp=Blueprint('student',__name__)
@student_bp.route('/student',methods=["POST","GET"])
def student_information():
    if 'username' not in session:
        return redirect(url_for('login.login'))
    db=None
    cursor=None
    data=[]
    config = current_app.config['DB_CONFIG']
    try:
        db=mysql.connector.connect(**config)
        cursor=db.cursor(dictionary=True)
        sql="""
                SELECT s.student_id AS student_id,
                s.name AS student_name,
                s.email AS email_address,
                s.phone AS mobile_number,
                CONCAT(r.block_name,'-',r.room_no) AS room_no,
                f.status AS fees_status
                FROM students s
                JOIN rooms r ON s.room_id=r.room_id
                JOIN fees f ON s.student_id=f.student_id
            """
        conditions=[]
        params=[]
        status_filter=request.args.get('status')
        search_query=request.args.get('search')
        print(search_query)
        if search_query:
            conditions.append("""
                        (s.name LIKE %s 
                            OR s.email LIKE %s 
                            OR UPPER(TRIM(CONCAT(r.block_name, '-', r.room_no))) LIKE UPPER(TRIM(%s)))
            """)
            params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])


        if status_filter and status_filter.lower() in ['paid', 'unpaid', 'overdue']:
            conditions.append("f.status = %s")
            params.append(status_filter)
            
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        cursor.execute(sql,params)
        data=cursor.fetchall()
        print(data)
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    return render_template('students.html',data=data)