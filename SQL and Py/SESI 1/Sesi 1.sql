use world; -- pilih database apa aja

SHOW tables; -- Memperlihatkan informasi tabel dari database
# ---------------------------------------------------------------------------------------------------------------------- #
-- Untuk menampilkan semua kolom pada tabel
SELECT * FROM city;
SELECT * FROM country;
SELECT * FROM countrylanguage;

-- Untuk menampilkan beberapa kolom dalam 1 tabel
SELECT Name AS `Country Name`, LocalName, Region -- AS ini digunakan untuk ganti nama tabel jika ini pake spasi pakai kutip 1 sebelah angka 1
FROM country;

# LIMIT, DISTINCT, COUNT, SUM, AVG #

#LIMIT → batasi jumlah baris.
SELECT * FROM city
LIMIT 10;

#DISTINCT → ambil nilai unik saja. --Biasanya digunakan quick review
SELECT distinct CountryCode
FROM city;

#COUNT() → hitung jumlah baris.
SELECT COUNT( DISTINCT CountryCode) AS `Total Country Code`
FROM city;

#SUM() → jumlahkan nilai angka.
SELECT SUM(Population) as AllPopulation
FROM city;

#AVG() → hitung rata-rata nilai angka.
SELECT AVG(Population) as Average
FROM city;

SELECT COUNT(Name) AS BanyakNegara , AVG(GNP) AS Rerata, SUM(Population) AS JmlPopulasi, MIN(GNP) GNPterkecil, MAX(GNP) GNPterbesar
FROM Country;