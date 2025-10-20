## join table
# INNER JOIN
-- Mengembalikan hanya baris yang cocok (matching) di kedua tabel. Kalau tidak ada pasangan data, maka baris tersebut tidak muncul.
# LEFT JOIN (atau LEFT OUTER JOIN)
-- Mengembalikan semua baris dari tabel kiri + data yang cocok dari tabel kanan. Kalau tidak ada pasangan di kanan, hasilnya NULL.
# RIGHT JOIN (atau RIGHT OUTER JOIN)
-- Kebalikan dari LEFT JOIN: menampilkan semua baris dari tabel kanan, plus data yang cocok dari tabel kiri.
# 
-- 
USE world;
SELECT * FROM CITY;
SELECT * FROM COUNTRY;
SELECT * FROM COUNTRYLANGUAGE;

-- tampilkan nama kota, negara, benua, populasi
-- nama negara, asal benua, gnp, bahasa official, % penggunaan

SELECT
	c.name as NamaKota, 
    co.name as NamaNegara, 
    co.continent, 
    c.population
FROM 
	city as c -- deklarasi table sebelah kiri
JOIN 
	country as co -- tabel kanan
ON 
	c.CountryCode = co.code -- join primary dan foreign key
ORDER BY 1;

USE sakila;






















    
