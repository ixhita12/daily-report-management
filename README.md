# Daily Report Management System

A web-based **Daily Report Management System** developed using **Python Flask** and **MySQL**.
The system allows students to submit their daily work reports and enables the admin to review, approve, or reject them with comments.

This project demonstrates role-based access, workflow management, and a structured reporting system suitable for academic and organizational use.

---

## 🚀 Features

### Student Panel

* Student login system
* Submit daily work reports
* Edit reports if rejected
* Delete reports before approval
* View report status (Pending / Approved / Rejected)
* View admin comments on rejected reports

### Admin Panel

* Admin dashboard with report statistics
* View all submitted reports
* Approve or reject reports
* Provide rejection comments
* Filter reports by status
* Filter reports by date

---

## 🛠️ Tech Stack

**Backend**

* Python
* Flask

**Database**

* MySQL

**Frontend**

* HTML
* CSS
* Bootstrap


**Version Control**

* Git
* GitHub

---

## 📂 Project Structure

```
daily-report-project/
│
├── app.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   ├── submit_report.html
│   ├── edit_report.html
│   ├── view_report.html
│   ├── report_success.html
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/ixhita12/daily-report-management.git

### 2. Navigate to project folder

```
cd daily-report-system
```

### 3. Install dependencies

```
pip install flask
pip install mysql-connector-python
```

### 4. Configure MySQL Database

Create database:

```
CREATE DATABASE daily_report_db;
```

Create reports table:

```
CREATE TABLE reports (
id INT AUTO_INCREMENT PRIMARY KEY,
report_date DATE,
email VARCHAR(100),
work_done TEXT,
hours INT,
status VARCHAR(20),
review_comment TEXT
);
```

### 5. Run the application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Default Admin Login

```
Email: admin@gmail.com
Password: admin123
```

Students can login using their email and password.

---

## 📊 Workflow

1. Student submits daily report
2. Report status becomes **Pending**
3. Admin reviews the report
4. Admin can **Approve** or **Reject**
5. If rejected, admin adds a **comment**
6. Student edits and resubmits the report

---

## 📌 Future Improvements

* Password encryption
* Email notifications
* Dashboard analytics
* Export reports to PDF/CSV
* Deployment on cloud server

---

## 👩‍💻 Author

**Ishita Gupta**

MCA Major Project
Daily Report Management System
