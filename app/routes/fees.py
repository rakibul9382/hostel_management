import os
from flask import Blueprint, render_template,request,session,redirect,url_for,current_app
import mysql.connector
import datetime
fees_bp=Blueprint('fees',__name__)
@fees_bp.route('/fees')
def fees():
    if 'username' not in session:
        return redirect(url_for('login.login'))  # your login route name
    db = None
    cursor = None
    collected_money_current_month = 0
    total_due = 0
    data = []
    config = current_app.config['DB_CONFIG']
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor(dictionary=True)

        # --- collected money for current month ---
        cursor.execute("""
            SELECT SUM(amount) AS collected_this_month
            FROM fees 
            WHERE status = 'Paid'
            AND DATE_FORMAT(paid_date, '%Y-%m') = DATE_FORMAT(CURDATE(), '%Y-%m')
        """)
        result = cursor.fetchone()
        if result and result['collected_this_month'] is not None:
            collected_money_current_month = result['collected_this_month']

        # --- total due amount ---
        cursor.execute("""
            SELECT SUM(amount) AS due_amount
            FROM fees
            WHERE status IN ('unpaid', 'overdue')
        """)
        result = cursor.fetchone()
        if result and result['due_amount'] is not None:
            total_due = result['due_amount']

        # --- table data ---
        status_filter = request.args.get('status')  # e.g., 'Paid', 'Due', 'Overdue'
        search_query = request.args.get('search')  # Get the search term
        month_filter = request.args.get('month')

        sql= """
                SELECT
                s.name AS student_name,
                r.room_no AS room_number,
                f.billing_month,
                f.amount,
                f.status,
                f.paid_date AS payment_date
        FROM students s
        JOIN rooms r ON s.room_id = r.room_id
        JOIN fees f ON s.student_id = f.student_id
    """
        conditions = []
        params = []
         # Add search condition if a search query exists
        if search_query:
            conditions.append("s.name LIKE %s")
            params.append(f"%{search_query}%")

        # Add status filter condition if a status is selected
        if status_filter and status_filter.lower() in ['paid', 'unpaid', 'overdue']:
            conditions.append("f.status = %s")
            params.append(status_filter)

        if month_filter:
             # Convert '2025-10' -> 'October 2025'
            dt = datetime.datetime.strptime(month_filter, "%Y-%m")
            month_str = dt.strftime("%B %Y")  # "October 2025"
            conditions.append("f.billing_month = %s")
            params.append(month_str)


        # Append all conditions to the main query
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(sql, params)
        data = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()
    print("Collected this month:", collected_money_current_month)
    print("Total due:", total_due)
    print("Table data:", data)
    # --- Pass to Jinja template ---
    return render_template(
        'fees.html',
        collected_this_month=collected_money_current_month,
        total_due=total_due,
        table_information=data
    )
