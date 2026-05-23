A modern web-based student performance management system built using Flask and MySQL.
This application helps admins and students manage academic records, analyze performance, visualize insights, and generate downloadable PDF reports.

🚀 Features
🔐 User Authentication (Admin & Student Roles)
🧑‍🎓 Student Record Management
📊 Subject-wise Marks Entry
📈 GPA & Grade Calculation
📉 Performance Analytics using Charts
📝 Student Task Planner
✅ Approval/Rejection System for Student Submissions
📄 Download Student Reports as PDF
📱 Responsive Modern UI
🛠️ Tech Stack
Backend
Python
Flask
Flask-SQLAlchemy
Werkzeug Security
ReportLab
Frontend
HTML5
CSS3
JavaScript
Chart.js
Database
MySQL
📂 Project Structure
student-performance-analyzer/
│
├── app.py
├── models.sql
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student.html
│   ├── insights.html
│   └── edit.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
└── README.md
⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/student-performance-analyzer.git
cd student-performance-analyzer
2️⃣ Create Virtual Environment
python -m venv venv

Activate environment:

Windows
venv\Scripts\activate
Mac/Linux
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt

Dependencies are listed in requirements.txt.

4️⃣ Setup MySQL Database

Open MySQL and run:

source models.sql;

Database schema includes:

students
marks
users
tasks

Defined in models.sql.

5️⃣ Configure Database Connection

Update MySQL credentials inside app.py:

app.config['SQLALCHEMY_DATABASE_URI'] = 
'mysql+pymysql://username:password@localhost/studentdb'

Current configuration exists in app.py.

6️⃣ Run the Application
python app.py

Application will start at:

http://127.0.0.1:5000
📊 Key Modules
🔐 Authentication
User Registration
Login/Logout
Password Hashing
Role-based Access

Implemented in:

login.html
register.html
app.py
🧑‍🎓 Student Management
Add Student
Edit Student
View Student Reports
Approval Workflow

Implemented in:

index.html
edit.html
student.html
📈 Analytics Dashboard
Branch-wise GPA
Pie Chart Distribution
Highest Performing Branch

Implemented in:

insights.html
📄 PDF Report Generation
Download student reports
Subject-wise performance table
GPA and grade summary

Implemented using ReportLab in app.py.

🎯 GPA & Grade System
Marks Range	Grade	GPA
90+	A+	10
80-89	A	9
70-79	B	8
60-69	C	7
40-59	D	6
Below 40	F	0

Logic implemented in:

📱 UI Highlights
Modern responsive dashboard
Gradient themed interface
Interactive charts
Mobile responsive layout
Task planner integration

Styles implemented in:

📌 Future Improvements
Email Notifications
Attendance Tracking
Student Profile Pictures
Export to Excel
Search & Filtering
Multi-Department Support
AI-based Performance Prediction
👨‍💻 Author

Developed by Pandu & Team 🚀

📄 License

This project is developed for educational purposes and learning demonstrations.
