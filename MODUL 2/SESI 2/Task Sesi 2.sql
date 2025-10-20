-- task 1
USE sakila;
SELECT * FROM film;

SELECT distinct (rating) -- distict function harus diikuti nama kolom
FROM film;

SELECT
 title AS judulFilm, description AS deskripsiFilm, length AS durasiFilm
FROM film;

SELECT
 title AS judulFilm, description AS deskripsiFilm, length AS durasiFilm
FROM film
WHERE 
	DESCRIPTION LIKE '%documentary%' AND
    length > 60;

-- task 2
USE classicmodels;

SELECT *
FROM products;

SELECT distinct(productLine)
FROM products;

SELECT productName, productLine, productScale, buyPrice
FROM products;

SELECT productName, productLine, productScale, buyPrice
FROM products
WHERE productScale in ('1:10', '1:12') AND
	productLine = 'Classic Cars' AND
    buyPrice > 100;
    
-- TASK 3
USE classicmodels;

SELECT *
FROM products;

SELECT productName, productLine, buyPrice
FROM PRODUCTS
order by buyPrice DESC
LIMIT 1;

-- Soal 1
USE classicmodels;

SELECT *
FROM products;

SELECT productName, quantityInStock
FROM products
ORDER BY quantityInStock asc
LIMIT 10;

-- Soal 2
SELECT *
FROM payments;

SELECT distinct(customerNumber)
FROM payments
WHERE amount > 100000;

-- Soal 3
SELECT *
FROM products;

SELECT productName as namaProduk, quantityInStock as qty
FROM products
WHERE productName LIKE '%Ford%';

-- Cust Non eropa
SELECT * 
FROM customers;

SELECT customerName, country
FROM customers
WHERE country NOT IN ('France','Germany','Spain','UK');

-- validasi pembayaran range
SELECT *
FROM payments;

SELECT amount
FROM payments
WHERE amount BETWEEN 20000 AND 50000;

-- order dengan status
SELECT *
FROM orders;

SELECT customerNumber, orderNumber, status
FROM orders
WHERE status = 'Cancelled';

-- Produk dengan nama mirip
SELECT *
FROM products;

SELECT *
FROM products
WHERE productName LIKE '%Truck%'
ORDER BY buyPrice DESC
LIMIT 1;

-- Customer membayar banyak
SELECT * FROM payments;

SELECT customerNumber, COUNT(*) AS jmlPembayaran
FROM payments
GROUP BY customerNumber
ORDER BY jmlPembayaran DESC
LIMIT 5;

-- Pembayaran terbesar
SELECT customerNumber, MAX(amount) AS maxPayment
FROM payments
GROUP BY customerNumber;

-- 3 Negara Top Customer
SELECT * FROM customers;

SELECT country, COUNT(*) AS jmlCustomer -- Menghitung total cust dari group by, jika tidak pakai group by akan menghitung semua
FROM customers
GROUP BY country
ORDER BY jmlCustomer DESC
LIMIT 3;




