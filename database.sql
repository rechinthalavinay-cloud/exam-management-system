-- Examination Module Database Schema
-- Run: mysql -u root -p < database.sql

CREATE DATABASE IF NOT EXISTS exam_db;
USE exam_db;

-- Users table (admin login)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    course VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exams table
CREATE TABLE IF NOT EXISTS exams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exam_name VARCHAR(100) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    total_marks INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Results table (grade auto-calculated on insert/update)
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    exam_id INT NOT NULL,
    marks INT NOT NULL,
    grade VARCHAR(5) DEFAULT NULL,
    percentage DECIMAL(5,2) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_exam (student_id, exam_id)
);

-- Admin user is auto-created on first run (username: admin, password: admin123)

-- Sample data
INSERT INTO students (student_name, email, phone, course) VALUES
('Rahul Sharma', 'rahul@example.com', '9876543210', 'Computer Science'),
('Priya Patel', 'priya@example.com', '9876543211', 'Information Technology'),
('Amit Kumar', 'amit@example.com', '9876543212', 'Electronics');

INSERT INTO exams (exam_name, subject, total_marks) VALUES
('Mid Term Exam', 'Data Structures', 100),
('Final Exam', 'Database Management', 100),
('Unit Test', 'Web Development', 50);
