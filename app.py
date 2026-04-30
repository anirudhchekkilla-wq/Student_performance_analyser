from flask import Flask, render_template, request, redirect, session, flash, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

'''app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False'''
# ================= DATABASE =================
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pandu%402006@localhost/studentdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= MODELS =================

class Students(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    branch = db.Column(db.String(50))
    semester = db.Column(db.Integer)
    status = db.Column(db.String(20), default='Pending')
    submitted_by = db.Column(db.String(100))
    overall_marks = db.Column(db.Integer, default=0)
    overall_gpa = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    marks = db.relationship(
        'Marks',
        backref='student',
        lazy=True,
        cascade="all, delete-orphan",
        primaryjoin="Students.roll_no==Marks.roll_no"
    )


class Marks(db.Model):
    __tablename__ = 'marks'

    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(20), db.ForeignKey('students.roll_no'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    internal = db.Column(db.Integer, nullable=False, default=0)
    external = db.Column(db.Integer, nullable=False, default=0)
    semester = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('roll_no', 'subject', 'semester', name='unique_student_subject_sem'),
    )


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    status = db.Column(db.String(50), default='Pending')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# ================= SUBJECT CONFIG =================
SEM_SUBJECTS = {
    "CSE": {
        1: ["Maths", "C", "English", "Chemistry"],
        2: ["DS", "Python", "Physics", "Maths2"],
        3: ["OOP", "Java", "DBMS", "OS"],
        4: ["CN", "CPP", "SE", "DM"],
        5: ["AI", "ML", "DL", "CV"],
        6: ["NLP", "Big Data", "Cloud", "Cyber Security"],
        7: ["IoT", "Blockchain", "Data Science", "Ethical Hacking"],
        8: ["Mobile App Dev", "Web Dev", "Software Testing", "Project Management"]
    },
    "IT": {
        1: ["Maths", "C", "English", "Chemistry"],
        2: ["DS", "Python", "Physics", "Maths2"],
        3: ["OOP", "QALR", "UHV", "DE"],
        4: ["CO", "ITWS", "DBMS", "PP"],
        5: ["DAA", "CN", "IDS", "DWDM", "IPR", "SE"],
        6: ["OS", "Big Data", "AIDL", "CSCL", "ML", "WT"],
        7: ["IoT", "Blockchain", "Data Science", "Ethical Hacking"],
        8: ["Mobile App Dev", "Web Dev", "Software Testing", "Project Management"]
    }
}

# ================= HELPERS =================

def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def subject_key(subject):
    return subject.replace(" ", "_").replace("-", "_").lower()


def get_grade_and_gpa(total):
    if total >= 90:
        return "A+", 10
    elif total >= 80:
        return "A", 9
    elif total >= 70:
        return "B", 8
    elif total >= 60:
        return "C", 7
    elif total >= 40:
        return "D", 6
    else:
        return "F", 0


def is_logged_in():
    return 'user_id' in session


def is_admin():
    return session.get('role') == 'admin'


# ================= AUTH =================
# ================= TASKS =================


from datetime import datetime

@app.route('/add_task', methods=['POST'])
def add_task():
    if not is_logged_in():
        return redirect('/login')

    title = request.form.get('title')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Basic check
    if not title or not start_date or not end_date:
        flash("All fields required")
        return redirect('/')

    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    today = datetime.today().date()

    if start < today:
        flash("Start date cannot be before today")
        return redirect('/')

    if end <= start:
        flash("End date must be after start date")
        return redirect('/')

    task = Task(
        title=title,
        status="Pending",
        start_date=start,
        end_date=end,
        user_id=session['user_id']
    )

    db.session.add(task)
    db.session.commit()

    return redirect('/')

@app.route('/complete_task/<int:id>')
def complete_task(id):
    if not is_logged_in():
        return redirect('/login')

    task = Task.query.get(id)

    if task and task.user_id == session['user_id']:
        task.status = 'Completed'
        db.session.commit()

    return redirect('/')
@app.route('/delete_task/<int:id>')
def delete_task(id):
    task = Task.query.get(id)

    if task and task.user_id == session['user_id']:
        db.session.delete(task)
        db.session.commit()

    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        role = request.form.get('role').strip()

        if not username or not password or not role:
            flash("All fields required")
            return redirect('/register')

        if User.query.filter_by(username=username).first():
            flash("Username exists")
            return redirect('/register')

        user = User(
            username=username,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(user)
        db.session.commit()

        flash("Registered successfully")
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()

        if user and check_password_hash(user.password, request.form.get('password')):
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            return redirect('/')
        
    
        flash("Invalid credentials")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/download/<int:id>')
def download_student_pdf(id):
    if not is_logged_in():
        return redirect('/login')

    student = Students.query.get_or_404(id)

    # 🔐 Access control
    if not is_admin() and student.submitted_by != session['username']:
        flash("Not allowed")
        return redirect('/')

    marks = Marks.query.filter_by(
        roll_no=student.roll_no,
        semester=student.semester
    ).all()

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Student Performance Report", styles['Title']))
    elements.append(Spacer(1, 10))

    # Student info
    elements.append(Paragraph(f"Name: {student.name}", styles['Normal']))
    elements.append(Paragraph(f"Roll No: {student.roll_no}", styles['Normal']))
    elements.append(Paragraph(f"Branch: {student.branch}", styles['Normal']))
    elements.append(Paragraph(f"Semester: {student.semester}", styles['Normal']))
    elements.append(Spacer(1, 15))

    # Table data
    data = [["Subject", "Internal", "External", "Total", "GPA", "Grade"]]

    for m in marks:
        total = m.internal + m.external
        grade, gpa = get_grade_and_gpa(total)

        data.append([
            m.subject,
            m.internal,
            m.external,
            total,
            gpa,
            grade
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))

    elements.append(table)
    elements.append(Spacer(1, 15))

    # Overall
    elements.append(Paragraph(f"Total Marks: {student.overall_marks}", styles['Normal']))
    elements.append(Paragraph(f"GPA: {student.overall_gpa}", styles['Normal']))

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{student.roll_no}.pdf",
        mimetype='application/pdf'
    )
# ================= MAIN =================

@app.route('/')
def index():
    if not is_logged_in():
        return redirect('/login')

    if is_admin():
        students = Students.query.all()
    else:
        students = Students.query.filter_by(
            submitted_by=session['username'],
            status='Approved'
        ).all()

    tasks = Task.query.filter_by(user_id=session['user_id']).all()

    # 🔔 NOTIFICATIONS LOGIC
    today = datetime.today().date()
    notifications = []

    for t in tasks:
        if t.status == "Pending":
            days_left = (t.end_date - today).days

            if days_left == 0:
                notifications.append(f"⚠️ Task '{t.title}' is due TODAY!")
            elif days_left == 1:
                notifications.append(f"⏰ Task '{t.title}' is due TOMORROW!")
            elif days_left < 0:
                notifications.append(f"❌ Task '{t.title}' is OVERDUE!")

    return render_template(
        'index.html',
        students=students,
        tasks=tasks,
        notifications=notifications
    )
# ================= ADD STUDENT + MARKS =================

@app.route('/add', methods=['POST'])
def add():
    if not is_logged_in():
        return redirect('/login')

    name = request.form.get('name')
    roll_no = request.form.get('roll_no')
    email = request.form.get('email')
    phone = request.form.get('phone')
    branch = request.form.get('branch')
    semester = safe_int(request.form.get('semester'))

    if not name or not roll_no or not branch or not semester:
        flash("Required fields missing")
        return redirect('/')

    if Students.query.filter_by(roll_no=roll_no).first():
        flash("Student already exists")
        return redirect('/')

    student = Students(
        name=name,
        roll_no=roll_no,
        email=email,
        phone=phone,
        branch=branch,
        semester=semester,
        status='Approved' if is_admin() else 'Pending',
        user_id=session['user_id'],
        submitted_by=session['username']
    )

    db.session.add(student)

    # ADD MARKS
    subjects = SEM_SUBJECTS.get(branch, {}).get(semester, [])

    for subject in subjects:
        key = subject_key(subject)

        internal = safe_int(request.form.get(f"{key}_internal"), 0)
        external = safe_int(request.form.get(f"{key}_external"), 0)

        mark = Marks(
            roll_no=roll_no,
            subject=subject,
            internal=internal,
            external=external,
            semester=semester
        )

        db.session.add(mark)
        total_marks = 0
        total_gpa = 0

        marks_list = Marks.query.filter_by(
        roll_no=roll_no,
        semester=semester).all()

        for m in marks_list:
            total = m.internal + m.external
            _, gpa = get_grade_and_gpa(total)

            total_marks += total
            total_gpa += gpa

        if marks_list:
            avg_gpa = total_gpa / len(marks_list)
        else:
            avg_gpa = 0

        # 🔥 STORE IN STUDENT
        student.overall_marks = total_marks
        student.overall_gpa = round(avg_gpa, 2)
    db.session.commit()

    flash("Student added successfully")
    return redirect('/')


# ================= VIEW =================

@app.route('/student/<int:id>')
def view_student(id):
    if not is_logged_in():
        return redirect('/login')

    student = Students.query.get_or_404(id)

    if not is_admin() and student.status != 'Approved':
        flash("Not approved yet")
        return redirect('/')

    # 🔥 NEW: Fetch tasks of this student
    tasks = Task.query.filter_by(user_id=student.user_id).all()

    marks = Marks.query.filter_by(
        roll_no=student.roll_no,
        semester=student.semester
    ).all()

    subject_data = []
    total_marks = 0
    total_gpa = 0

    chart_labels = []
    chart_values = []

    for m in marks:
        total = m.internal + m.external
        grade, gpa = get_grade_and_gpa(total)

        total_marks += total
        total_gpa += gpa

        subject_data.append({
            "subject": m.subject,
            "internal": m.internal,
            "external": m.external,
            "total": total,
            "grade": grade,
            "gpa": gpa
        })

        chart_labels.append(m.subject)
        chart_values.append(total)

    avg = round(total_marks / len(subject_data), 2) if subject_data else 0
    avg_gpa = round(total_gpa / len(subject_data), 2) if subject_data else 0
    overall_grade, _ = get_grade_and_gpa(avg)

    return render_template(
        'student.html',
        student=student,
        subject_data=subject_data,
        avg=avg,
        avg_gpa=avg_gpa,
        overall_grade=overall_grade,
        chart_labels=chart_labels,
        chart_values=chart_values,
        tasks=tasks   # 🔥 PASS TASKS
    )

# ================= EDIT (ONLY STUDENT) =================

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if not is_logged_in():
        return redirect('/login')

    student = Students.query.get_or_404(id)

   
    if is_admin():
        flash("Admin cannot edit")
        return redirect('/')

    if student.submitted_by != session['username']:
        flash("Not allowed")
        return redirect('/')

    # Get marks
    marks = Marks.query.filter_by(
        roll_no=student.roll_no,
        semester=student.semester
    ).all()

    if request.method == 'POST':
        # Update student details
        student.name = request.form.get('name')
        student.email = request.form.get('email')
        student.phone = request.form.get('phone')
        student.branch = request.form.get('branch')
        student.semester = safe_int(request.form.get('semester'))

        for i, m in enumerate(marks):
            m.internal = safe_int(request.form.get(f'internal_{i}'))
            m.external = safe_int(request.form.get(f'external_{i}'))

        total_marks = 0
        total_gpa = 0

        for m in marks:
            total = m.internal + m.external
            _, gpa = get_grade_and_gpa(total)

            total_marks += total
            total_gpa += gpa

        if marks:
            avg_gpa = total_gpa / len(marks)
        else:
            avg_gpa = 0

        student.overall_marks = total_marks
        student.overall_gpa = round(avg_gpa, 2)

        db.session.commit()

        flash("Updated successfully")
        return redirect('/')

    return render_template('edit.html', student=student, marks=marks)

@app.route('/insights')
def insights():
    if not is_logged_in():
        return redirect('/login')

    students = Students.query.filter_by(status='Approved').all()

    branch_data = {}

    for s in students:
        marks = Marks.query.filter_by(
            roll_no=s.roll_no,
            semester=s.semester
        ).all()

        if not marks:
            continue

        total_gpa = 0

        for m in marks:
            total = m.internal + m.external
            _, gpa = get_grade_and_gpa(total)
            total_gpa += gpa

        avg_gpa = total_gpa / len(marks)

        if s.branch not in branch_data:
            branch_data[s.branch] = []

        branch_data[s.branch].append(avg_gpa)

    branch_labels = []
    branch_avg_gpa = []

    for branch, gpas in branch_data.items():
        branch_labels.append(branch)
        branch_avg_gpa.append(round(sum(gpas) / len(gpas), 2))

    if not branch_labels:
        branch_labels = ["No Data"]
        branch_avg_gpa = [0]

    top_branch = "No Data"
    top_branch_gpa = 0

    if branch_data:
        best_avg = 0

        for branch, gpas in branch_data.items():
            avg = sum(gpas) / len(gpas)

            if avg > best_avg:
                best_avg = avg
                top_branch = branch
                top_branch_gpa = round(avg, 2)

    branch_counts = {}

    for s in students:
        branch_counts[s.branch] = branch_counts.get(s.branch, 0) + 1

    pie_labels = list(branch_counts.keys())
    pie_values = list(branch_counts.values())

    if not pie_labels:
        pie_labels = ["No Data"]
        pie_values = [0]

    return render_template(
        'insights.html',
        branch_labels=branch_labels,
        branch_avg_gpa=branch_avg_gpa,
        pie_labels=pie_labels,
        pie_values=pie_values,
        top_branch=top_branch,
        top_branch_gpa=top_branch_gpa
    )
# ================= APPROVAL =================

@app.route('/approve/<int:id>')
def approve_student(id):
    if not is_logged_in() or not is_admin():
        return redirect('/')

    student = Students.query.get_or_404(id)
    student.status = 'Approved'
    db.session.commit()

    flash("Approved")
    return redirect('/')


@app.route('/reject/<int:id>')
def reject_student(id):
    if not is_logged_in() or not is_admin():
        return redirect('/')

    student = Students.query.get_or_404(id)

    # 🔥 ALWAYS DELETE
    Marks.query.filter_by(roll_no=student.roll_no).delete()
    db.session.delete(student)

    db.session.commit()

    flash("Student rejected and deleted successfully")
    return redirect('/')


# ================= RUN =================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)