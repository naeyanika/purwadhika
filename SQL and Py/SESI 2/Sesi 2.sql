-- SELECT, FROM, JOIN, WHER, GROUP BY, HAVING, ORDER BY, LIMIT 
# ----------------------- WHERE ------------------- # Digunakan untuk filtering
USE world;

SELECT * FROM country;


SELECT 
Name as CountryName, Continent, Population, GNP
FROM Country
WHERE GNP > 1000;


-- Menampilkan nama negara, continet, population, dan GNP Nama Negaranya diawali dengan A dan berada di Eropa Serta GNP > 1000

SELECT 
Name as CountryName, Continent, Population, GNP
FROM country
WHERE 
	Name LIKE 'A%' AND -- Like digunakan untuk filtering
    Continent = 'Europe' AND
    GNP > 1000;


SELECT 
Name as CountryName, Continent, Population, GNP
FROM country
WHERE 
    GNP BETWEEN 1000 AND 3000; -- Diantara 1000 dan 3000
    
    
SELECT 
Name as CountryName, Continent, Population, GNP
FROM country
WHERE 
    GNP NOT BETWEEN 1000 AND 3000; -- Tidak diantara 1000 dan 3000
    
    
SELECT 
Name as CountryName, Continent, Population, GNP
FROM country
WHERE 
    Continent IN ("Europe","Asia"); -- Hanya eropa dan asia
    
SELECT 
Name as CountryName, Continent, Population, GNP
FROM country
WHERE 
    Continent NOT IN ("Europe","Asia"); -- Diluar eropa dan asia
    
-- Sorting cara 1
SELECT	
	Name as countryName, Continent, Population, GNP
FROM
	country
WHERE
	GNP BETWEEN 1000 AND 3000
ORDER BY Continent DESC;

-- Sorting cara 2
SELECT	
	Name as countryName, Continent, Population, GNP
FROM
	country
WHERE
	GNP BETWEEN 1000 AND 3000
    
ORDER BY 3 ASC; -- Bisa pakai angka sesuai Select yang kita pilih

-- Sorting 2 Kolom akan berguna ketika duplicate value
SELECT	
	Name as countryName, Continent, Population, GNP
FROM
	country
WHERE
	GNP BETWEEN 1000 AND 3000
ORDER BY Continent ASC, Population DESC; 

-- GROUPING RESULT *Dibagian select melibatkan aggregat func (COUNT, MAX, MIN, SUM, AVG)
USE world;

SELECT *
FROM country;
-- Menampilkan rata2 LifeExpectancy, Jumlah populasi setiap benua, dan max GNP dari setiap benua
SELECT Continent AS Benua, 
	AVG(LifeExpectancy) AS rerataLE,
    SUM(Population) AS JmlPopulasi,
    MAX(GNP) as GNPtertinggi
FROM country
# WHERE function filter yang merujuk ke data asli, sedangkan HAVING adalah fuction filter table setelah grouping
GROUP BY Continent
# Filter setelah grouping tidak bisa where, hanya bisa dilakukan dengan function dengan HAVING.
HAVING rerataLE > 70
ORDER BY 3 desc;

# SUB QUERY
-- # Menampilkan semua data kolom city tampilkan data populasi diatas-rata rata
USE WORLD;
SELECT *
FROM city
WHERE POPULATION >
	(SELECT AVG(POPULATION) FROM CITY)
ORDER BY NAME;


--
USE CLASSICMODELS;
SELECT * FROM PAYMENTS;
SELECT * FROM ORDERS;

-- Filtering Sub Queries
SELECT distinct(customerNumber) 
FROM payments
WHERE customerNumber NOT IN
	(SELECT distinct(customerNumber) 
    FROM orders);
    
############################################################################################################
SELECT *
FROM COUNTRY;

SELECT NAME, CONTINENT, REGION, SURFACEAREA, POPULATION, 
			ROUND(POPULATION/SURFACEAREA,0) AS PopulasiPerluas
FROM COUNTRY;

-- UCASE (UPPER)
-- LCASE (LOWER)
-- CONCAT
-- TRIM
-- REGEX
-- DAY, MONTH, MONTHNAME

# CASE WHEN
SELECT * FROM CITY;
-- Populasi diatas 10Juta > Padat Penduduk
-- Populasi diatas 5.000.000 - 10.000.000 > Normal
-- Populasi diatas 2.000.000 - 5.000.000 > Cukup Senggang
-- Populasi dibawah 2.000.000 > Sepi

SELECT name, district, population,
		CASE
        WHEN POPULATION > 10000000 THEN "PADAT PENDUDUK"
        WHEN POPULATION > 5000000 THEN "NORMAL"
        WHEN POPULATION > 2000000 THEN "CUKUP SENGGANG"
        ELSE "SEPI"
		END AS KategoriPenduduk
	FROM CITY;