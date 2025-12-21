-- ==========================================
-- Payroll Management System Database Schema
-- ==========================================

CREATE DATABASE IF NOT EXISTS payroll_management;
USE payroll_management;

-- ==========================================
-- 1. ADMIN TABLE (Authentication)
-- ==========================================
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- 2. SALARY STRUCTURE TABLE (Pay Grades)
-- ==========================================
CREATE TABLE salary_structure (
    structure_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    base_salary_min DECIMAL(10,2) NOT NULL,
    base_salary_max DECIMAL(10,2) NOT NULL,
    housing_allowance_pct DECIMAL(5,2) DEFAULT 0.00,
    transport_allowance DECIMAL(10,2) DEFAULT 0.00,
    tax_rate_pct DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (base_salary_min <= base_salary_max)
);

-- ==========================================
-- 3. EMPLOYEE TABLE
-- ==========================================
CREATE TABLE employee (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_code VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    contact_no VARCHAR(15),
    email VARCHAR(100),
    date_of_joining DATE NOT NULL,
    basic_salary DECIMAL(10,2) NOT NULL,

    structure_id INT,
    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_employee_structure
        FOREIGN KEY (structure_id)
        REFERENCES salary_structure(structure_id)
        ON DELETE SET NULL
);

-- ==========================================
-- 4. ATTENDANCE TABLE
-- ==========================================
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT NOT NULL,
    month_year VARCHAR(20) NOT NULL,   -- e.g. March-2025
    days_worked INT NOT NULL,
    days_absent INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_attendance_employee
        FOREIGN KEY (emp_id)
        REFERENCES employee(emp_id)
        ON DELETE CASCADE,

    UNIQUE (emp_id, month_year)
);

-- ==========================================
-- 5. PAYROLL / PAYSLIP TABLE
-- ==========================================
CREATE TABLE payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT NOT NULL,
    month_year VARCHAR(20) NOT NULL,

    basic_salary DECIMAL(10,2),
    hra DECIMAL(10,2),
    da DECIMAL(10,2),
    transport_allowance DECIMAL(10,2),

    pf DECIMAL(10,2),
    tax DECIMAL(10,2),

    gross_salary DECIMAL(10,2),
    net_salary DECIMAL(10,2),

    pdf_path VARCHAR(255),

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payroll_employee
        FOREIGN KEY (emp_id)
        REFERENCES employee(emp_id)
        ON DELETE CASCADE,

    UNIQUE (emp_id, month_year)
);

-- ==========================================
-- 6. SAMPLE ADMIN USER (OPTIONAL)
-- ==========================================
-- Password should be hashed in Python before insert
INSERT INTO admin (username, password_hash)
VALUES ('admin', 'admin123_hashed');
