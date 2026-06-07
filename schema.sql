-- =========================================================================
-- PROJECT SETUP: Thinklar CRM PROJECT
-- =========================================================================

-- Step 1: Create the database only if it does not exist
CREATE DATABASE IF NOT EXISTS thinklar_crm;

-- Step 2: Set the database context to avoid any "No database selected" errors
USE thinklar_crm;

-- Step 3: Define the leads table with professional CRM attributes
CREATE TABLE IF NOT EXISTS leads (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Unique auto-generated ID for each lead
    name VARCHAR(255) NOT NULL,                 -- Lead's full name
    email VARCHAR(255) NOT NULL UNIQUE,         -- Unique email constraint to prevent duplicates
    mobile VARCHAR(15) NOT NULL,                -- Stored as VARCHAR to retain country codes and leading zeros
    company VARCHAR(255) NULL,                  -- Company name (Optional field)
    source VARCHAR(100) NULL,                   -- Lead source (e.g., LinkedIn, Website, Referral)
    status VARCHAR(50) DEFAULT 'New',           -- Default status for any incoming lead
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Auto-records the date and time of creation
);

-- Step 4: Insert sample records into the leads table for testing and development
INSERT INTO leads (name, email, mobile, company, source, status) VALUES  
('Amit Sharma', 'amit.sharma@gmail.com', '9876543210', 'Anand Motors', 'LinkedIn', 'New'),
('Rahul Verma', 'rahul.v@yahoo.com', '9123456789', 'Modern Travels', 'Website', 'Contacted'),
('Priya Singh', 'priya.singh@gmail.com', '8877665544', 'Tech Solutions', 'Referral', 'Qualified'),
('Vikram Malhotra', 'vikram.m@outlook.com', '7766554433', 'Global Traders', 'Cold Call', 'Lost'),
('Sneha Gupta', 'sneha.g@gmail.com', '9988776655', 'EduStart Coaching', 'Website', 'New');

-- Step 5: Verify and view the final populated table data
SELECT * FROM thinklar_crm.leads;