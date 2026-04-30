create database studentdb;
use studentdb;
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    branch VARCHAR(50),
    semester INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
CREATE TABLE marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no varchar(20) not null,
    subject VARCHAR(50) not null,
    marks INT,
    semester INT not null,
    UNIQUE (roll_no, subject, semester),
FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
) ENGINE=InnoDB;
ALTER TABLE marks 
ADD COLUMN internal INT,
ADD COLUMN external INT;
ALTER TABLE marks DROP COLUMN marks;
select * from marks;
select * from students;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);

select * from users;


ALTER TABLE students
ADD COLUMN status VARCHAR(20) DEFAULT 'Pending',
ADD COLUMN submitted_by VARCHAR(100);


ALTER TABLE students 
ADD COLUMN user_id INT;

ALTER TABLE students
ADD CONSTRAINT fk_user_student
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;




ALTER TABLE students
ADD COLUMN overall_marks INT DEFAULT 0,
ADD COLUMN overall_gpa FLOAT DEFAULT 0;



CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending',
    start_date DATE,
    end_date DATE,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

select * from tasks;