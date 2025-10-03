-- PostgreSQL initialization script for Great Expectations demo
-- This script creates the sample NYC taxi data table

-- Create the nyc_taxi_data table
CREATE TABLE IF NOT EXISTS nyc_taxi_data (
    vendor_id INTEGER,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    trip_distance DECIMAL(10,2),
    fare_amount DECIMAL(10,2),
    extra DECIMAL(10,2),
    mta_tax DECIMAL(10,2),
    tip_amount DECIMAL(10,2),
    tolls_amount DECIMAL(10,2),
    ehail_fee DECIMAL(10,2),
    improvement_surcharge DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);

-- Insert sample data
INSERT INTO nyc_taxi_data VALUES
(1, '2023-01-01 10:00:00', '2023-01-01 10:15:00', 1, 1.5, 8.50, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(2, '2023-01-01 11:00:00', '2023-01-01 11:20:00', 2, 2.3, 12.75, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(3, '2023-01-01 12:00:00', '2023-01-01 12:10:00', 1, 0.8, 6.25, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(4, '2023-01-01 13:00:00', '2023-01-01 13:25:00', 3, 3.1, 15.50, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(5, '2023-01-01 14:00:00', '2023-01-01 14:15:00', 2, 1.9, 9.75, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(6, '2023-01-01 15:00:00', '2023-01-01 15:30:00', 1, 4.2, 18.25, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(7, '2023-01-01 16:00:00', '2023-01-01 16:12:00', 2, 1.2, 7.50, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(8, '2023-01-01 17:00:00', '2023-01-01 17:35:00', 4, 5.8, 25.75, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(9, '2023-01-01 18:00:00', '2023-01-01 18:20:00', 1, 2.7, 13.25, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
(10, '2023-01-01 19:00:00', '2023-01-01 19:18:00', 2, 1.6, 8.75, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);

-- Create additional sample tables for comprehensive testing
CREATE TABLE IF NOT EXISTS housing_data (
    id SERIAL PRIMARY KEY,
    price DECIMAL(12,2),
    bedrooms INTEGER,
    bathrooms DECIMAL(3,1),
    sqft_living INTEGER,
    sqft_lot INTEGER,
    floors DECIMAL(3,1),
    waterfront INTEGER,
    view INTEGER,
    condition INTEGER,
    grade INTEGER,
    sqft_above INTEGER,
    sqft_basement INTEGER,
    yr_built INTEGER,
    yr_renovated INTEGER,
    zipcode INTEGER,
    lat DECIMAL(10,7),
    long DECIMAL(10,7),
    sqft_living15 INTEGER,
    sqft_lot15 INTEGER
);

CREATE TABLE IF NOT EXISTS supermarket_sales (
    invoice_id VARCHAR(20),
    branch VARCHAR(10),
    city VARCHAR(20),
    customer_type VARCHAR(20),
    gender VARCHAR(10),
    product_line VARCHAR(50),
    unit_price DECIMAL(10,2),
    quantity INTEGER,
    tax_5_percent DECIMAL(10,2),
    total DECIMAL(10,2),
    date DATE,
    time TIME,
    payment VARCHAR(20),
    cogs DECIMAL(10,2),
    gross_margin_percentage DECIMAL(5,2),
    gross_income DECIMAL(10,2),
    rating DECIMAL(3,1)
);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO try_gx;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO try_gx;
