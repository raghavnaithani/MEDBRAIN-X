CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Patients Table
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    dob DATE,
    gender TEXT
);

-- Prescriptions Table
CREATE TABLE prescriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id),
    drug_name TEXT NOT NULL,
    dose TEXT,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- GIN index on drug_name
CREATE INDEX drug_name_gin ON prescriptions USING gin (to_tsvector('english', drug_name));

-- Interactions Table
CREATE TABLE interactions (
    drug_a TEXT NOT NULL,
    drug_b TEXT NOT NULL,
    risk_level TEXT CHECK (risk_level IN ('low', 'moderate', 'high')),
    description TEXT,
    PRIMARY KEY (drug_a, drug_b)
);
