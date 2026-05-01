DROP DATABASE IF EXISTS payroll_management;
CREATE DATABASE payroll_management;
USE payroll_management;

-- =========================
-- ADMIN TABLE
-- =========================
CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- SALARY STRUCTURE TABLE
-- =========================
CREATE TABLE salary_structure (
    structure_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,

    base_salary_min DECIMAL(10,2) NOT NULL,
    base_salary_max DECIMAL(10,2) NOT NULL,

    housing_allowance_pct DECIMAL(5,4) DEFAULT 0.0000,
    da_pct DECIMAL(5,4) DEFAULT 0.0000,
    tax_rate_pct DECIMAL(5,4) DEFAULT 0.0000,
    pf_pct DECIMAL(5,4) DEFAULT 0.0000,

    transport_allowance DECIMAL(10,2) DEFAULT 0.00,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (base_salary_min >= 0),
    CHECK (base_salary_max >= 0),
    CHECK (base_salary_min <= base_salary_max),

    CHECK (housing_allowance_pct BETWEEN 0 AND 1),
    CHECK (da_pct BETWEEN 0 AND 1),
    CHECK (tax_rate_pct BETWEEN 0 AND 1),
    CHECK (pf_pct BETWEEN 0 AND 1)
);

-- =========================
-- EMPLOYEE TABLE
-- =========================
CREATE TABLE employee (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_code VARCHAR(20) NOT NULL UNIQUE,

    full_name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),

    contact_no VARCHAR(15),
    email VARCHAR(100) UNIQUE,

    date_of_joining DATE NOT NULL,

    basic_salary DECIMAL(10,2) NOT NULL,
    structure_id INT,

    status ENUM('ACTIVE', 'INACTIVE') DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (basic_salary >= 0),

    CONSTRAINT fk_employee_structure
        FOREIGN KEY (structure_id)
        REFERENCES salary_structure(structure_id)
        ON DELETE SET NULL
);

-- INDEX
CREATE INDEX idx_employee_structure ON employee(structure_id);

-- =========================
-- ATTENDANCE TABLE
-- =========================
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,

    emp_id INT NOT NULL,
    month TINYINT NOT NULL,
    year SMALLINT NOT NULL,

    days_worked INT NOT NULL,
    days_absent INT NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (month BETWEEN 1 AND 12),
    CHECK (year >= 2000),

    CHECK (days_worked >= 0),
    CHECK (days_absent >= 0),
    CHECK (days_worked + days_absent <= 31),

    CONSTRAINT fk_attendance_employee
        FOREIGN KEY (emp_id)
        REFERENCES employee(emp_id)
        ON DELETE CASCADE,

    UNIQUE (emp_id, month, year)
);

-- INDEX
CREATE INDEX idx_attendance_emp ON attendance(emp_id);

-- =========================
-- PAYROLL TABLE
-- =========================
CREATE TABLE payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,

    emp_id INT NOT NULL,
    month TINYINT NOT NULL,
    year SMALLINT NOT NULL,

    basic_salary DECIMAL(10,2) NOT NULL,
    hra DECIMAL(10,2) NOT NULL,
    da DECIMAL(10,2) NOT NULL,
    transport_allowance DECIMAL(10,2) NOT NULL,

    pf DECIMAL(10,2) NOT NULL,
    tax DECIMAL(10,2) NOT NULL,

    gross_salary DECIMAL(10,2) NOT NULL,
    net_salary DECIMAL(10,2) NOT NULL,

    pdf_path VARCHAR(255),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CHECK (month BETWEEN 1 AND 12),
    CHECK (year >= 2000),

    CHECK (basic_salary >= 0),
    CHECK (hra >= 0),
    CHECK (da >= 0),
    CHECK (transport_allowance >= 0),
    CHECK (pf >= 0),
    CHECK (tax >= 0),
    CHECK (gross_salary >= 0),
    CHECK (net_salary >= 0),

    CONSTRAINT fk_payroll_employee
        FOREIGN KEY (emp_id)
        REFERENCES employee(emp_id)
        ON DELETE CASCADE,

    UNIQUE (emp_id, month, year)
);

-- INDEX
CREATE INDEX idx_payroll_emp ON payroll(emp_id);

-- =========================
-- SAMPLE ADMIN USER
-- =========================
INSERT INTO admin (username, password_hash)
VALUES ('admin', SHA2('admin123', 256));