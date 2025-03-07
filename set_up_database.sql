ALTER USER postgres PASSWORD 'Ahmede2*';

-- Create the database
CREATE DATABASE clinc_system;

-- Switch to the new database
\c clinc_system;

-- Create doctor_admin table
CREATE TABLE doctor_admin (
    doctor_admin_id VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL
);

-- Create patient table
CREATE TABLE patient (
    patient_id VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL
);

-- Create file table
CREATE TABLE file (
    file_id VARCHAR(255) PRIMARY KEY,
    phone_number VARCHAR(255),
    country_code VARCHAR(255),
    result_date DATE,
    selected_lab_test VARCHAR(255),
    result_type VARCHAR(255),
    file_path VARCHAR(255),
    status VARCHAR(255),
    doctor_admin_id VARCHAR(255),
    patient_id VARCHAR(255),
    FOREIGN KEY (doctor_admin_id) REFERENCES doctor_admin(doctor_admin_id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE
);

