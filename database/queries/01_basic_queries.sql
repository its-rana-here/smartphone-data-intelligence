
-- =====================================================
-- SMARTPHONE DATA INTELLIGENCE SYSTEM
-- File: 01_basic_queries.sql
-- Objective: Explore smartphone data using basic SQL
-- =====================================================

USE smartphone_data_intelligence;


-- 1. SELECT: Display all smartphone records
SELECT *
FROM smartphones;


-- 2. SELECT: Display specific columns
SELECT brand_name, model, price
FROM smartphones;


-- 3. WHERE: Find smartphones from Apple
SELECT brand_name, model, price
FROM smartphones
WHERE brand_name = 'Apple';


-- 4. WHERE: Find smartphones costing more than 50000
SELECT brand_name, model, price
FROM smartphones
WHERE price > 50000;


-- 5. WHERE: Combine conditions
-- Smartphones costing more than 30000 with at least 8 GB RAM
SELECT brand_name, model, price, ram_capacity
FROM smartphones
WHERE price > 30000
  AND ram_capacity >= 8;


-- 6. ORDER BY: Cheapest smartphones first
SELECT brand_name, model, price
FROM smartphones
ORDER BY price ASC;


-- 7. ORDER BY: Most expensive smartphones first
SELECT brand_name, model, price
FROM smartphones
ORDER BY price DESC;


-- 8. LIMIT: Display only 10 smartphones
SELECT brand_name, model, price
FROM smartphones
LIMIT 10;


-- 9. Combine WHERE, ORDER BY, and LIMIT
-- Find the 10 most expensive smartphones
SELECT brand_name, model, price
FROM smartphones
WHERE price > 0
ORDER BY price DESC
LIMIT 10;


-- 10. Find smartphones with missing ratings
SELECT brand_name, model, price, avg_rating
FROM smartphones
WHERE avg_rating IS NULL
LIMIT 20;


select *  from smartphones;
