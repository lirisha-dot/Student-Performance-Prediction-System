CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    study_hours FLOAT NOT NULL,        -- hours studied per day
    attendance INT NOT NULL,           -- percentage
    previous_marks INT NOT NULL,       -- percentage of last exam
    assignment_score INT NOT NULL,     -- percentage
    final_marks FLOAT NOT NULL         -- target value (0-100)
);

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    study_hours FLOAT,
    attendance INT,
    previous_marks INT,
    assignment_score INT,
    predicted_marks FLOAT,             -- Linear Regression output
    predicted_level VARCHAR(30),       -- Decision Tree output
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
