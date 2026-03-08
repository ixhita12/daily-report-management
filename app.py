from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sanish@123",
        database="daily_report_db"
    )

app = Flask(__name__)
app.secret_key = "supersecretkey"


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    # Admin security
    if role == "admin":
        if email != "admin@gmail.com" or password != "admin123":
            return redirect('/')

    # Student simple login
    if role == "student":
        if not email or not password:
            return redirect('/')

    session['email'] = email
    session['role'] = role

    if role == "admin":
        return redirect('/admin-dashboard')
    else:
        return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():

    if session.get('role') != 'student':
        return redirect('/')

    user_email = session.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()

    # 👇 Only this student's reports
    cursor.execute(
        "SELECT COUNT(*) FROM reports WHERE email = %s",
        (user_email,)
    )
    total_reports = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM reports WHERE email = %s AND report_date = CURDATE()",
        (user_email,)
    )
    today_reports = cursor.fetchone()[0]
    cursor.execute(
    "SELECT report_date, work_done, hours FROM reports WHERE email = %s ORDER BY id DESC LIMIT 1",
    (user_email,)
    )
    last_report = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "student_dashboard.html",
        total_reports=total_reports,
        today_reports=today_reports,
        last_report=last_report
    )


@app.route('/admin-dashboard')
def admin_dashboard():

    if session.get('role') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Total reports
    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]

    # Today's reports
    cursor.execute("SELECT COUNT(*) FROM reports WHERE report_date = CURDATE()")
    today_reports = cursor.fetchone()[0]

    # Total students (unique emails)
    cursor.execute("SELECT COUNT(DISTINCT email) FROM reports")
    total_students = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_reports=total_reports,
        today_reports=today_reports,
        total_students=total_students
    )


@app.route('/submit-report', methods=['GET'])
def submit_report():

    if session.get('role') != 'student':
        return redirect('/')

    return render_template("submit_report.html")

@app.route('/submit-report', methods=['POST'])
def save_report():
    date = request.form['date']
    email = session.get('email') 
    work = request.form['work']
    hours = request.form['hours']

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO reports (report_date, email, work_done, hours, status)
VALUES (%s, %s, %s, %s, %s)
"""
    cursor.execute(query, (date, email, work, hours, 'Pending'))

    conn.commit()
    cursor.close()
    conn.close()
    if not session.get('email'):
     return redirect('/')
 
    return render_template("report_success.html")


@app.route('/view-reports')
def view_reports():

    if not session.get('role'):
        return redirect('/')

    status_filter = request.args.get('status')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if session.get('role') == 'student':

        user_email = session.get('email')
        query = "SELECT * FROM reports WHERE email = %s"
        values = (user_email,)

    else:

        if status_filter and status_filter != "All":
            query = "SELECT * FROM reports WHERE status = %s"
            values = (status_filter,)
        else:
            query = "SELECT * FROM reports"
            values = ()

    cursor.execute(query, values)
    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view_report.html", reports=reports)


@app.route('/edit-report/<int:id>', methods=['GET', 'POST'])
def edit_report(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Pehle report fetch karo
    cursor.execute("SELECT * FROM reports WHERE id = %s", (id,))
    report = cursor.fetchone()
    if not report:
      return redirect('/view-reports')

    # 🔐 SECURITY CHECK
    if session.get('role') == 'student':
        if report['email'] != session.get('email'):
            return redirect('/dashboard')

        if report['status'] == 'Approved':
            return redirect('/dashboard')

    # Agar POST hai to update logic
    if request.method == 'POST':
        new_work = request.form['work']
        new_hours = request.form['hours']

        cursor.execute("""
           UPDATE reports 
           SET work_done = %s, hours = %s, status = 'Pending', review_comment = NULL
           WHERE id = %s
        """, (new_work, new_hours, id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/view-reports')

    return render_template("edit_report.html", report=report)

@app.route('/delete-report/<int:id>')
def delete_report(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Report check karo
    cursor.execute("SELECT * FROM reports WHERE id = %s", (id,))
    report = cursor.fetchone()

    # Agar student hai aur email match nahi karta → block
    if session.get('role') == 'student':

     if report['email'] != session.get('email'):
        return redirect('/dashboard')

     if report['status'] == 'Approved':
        return redirect('/dashboard')

    cursor.execute("DELETE FROM reports WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/view-reports')





@app.route('/approve/<int:id>')
def approve_report(id):

    if session.get('role') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE reports SET status = 'Approved' WHERE id = %s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/view-reports')

@app.route('/reject/<int:id>', methods=['POST'])
def reject_report(id):

    if session.get('role') != 'admin':
        return redirect('/')

    comment = request.form.get('comment')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE reports SET status = 'Rejected', review_comment = %s WHERE id = %s",
        (comment, id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/view-reports')


    return render_template("reject_report.html", report=report)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
