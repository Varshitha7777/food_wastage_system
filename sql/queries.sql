-- Providers per city
SELECT city, COUNT(*) AS total_providers FROM providers GROUP BY city;

-- Receivers per city
SELECT city, COUNT(*) AS total_receivers FROM receivers GROUP BY city;
