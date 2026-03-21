from flask import Flask, render_template, request, redirect
from models import db, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB
with app.app_context():
    db.create_all()

# 🏠 Home + Search + Stats
@app.route('/', methods=['GET'])
def index():
    query = request.args.get('search')

    if query:
        students = Student.query.filter(Student.name.contains(query)).all()
    else:
        students = Student.query.all()

    total_students = len(students)

    avg_age = 0
    if total_students > 0:
        avg_age = sum([s.age for s in students]) / total_students

    return render_template(
        'index.html',
        students=students,
        total_students=total_students,
        avg_age=avg_age
    )

# ➕ Add student
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = int(request.form['age'])
    email = request.form['email']
    department = request.form['department']

    new_student = Student(
        name=name,
        age=age,
        email=email,
        department=department
    )

    db.session.add(new_student)
    db.session.commit()

    return redirect('/')

# ✏️ Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.age = int(request.form['age'])
        student.email = request.form['email']
        student.department = request.form['department']

        db.session.commit()
        return redirect('/')

    return render_template('edit.html', student=student)

# ❌ Delete student
@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()
    