# TASK SESI 3(6,7,9 EXCEPT)
USE SAKILA;

# SOAL 1
SELECT customer_id AS CustomerID, rental_id AS RentalID, amount AS Amount, payment_date AS PaymentDate
FROM PAYMENT
LIMIT 10;

# SOAL 2
SELECT title, release_year, rental_duration
FROM FILM
WHERE title LIKE "A%A" AND
	length(TITLE) > 10;

# SOAL 3
SELECT 
    rental_duration AS DurasiRental,
    COUNT(TITLE) AS BanyakFilm,
    ROUND(AVG(length), 2) AS RataRataDurasiFilm
FROM film
GROUP BY rental_duration
ORDER BY rental_duration;

# SOAL 4 
SELECT title, length, rating
FROM FILM
WHERE length > (SELECT AVG(length) FROM film)
ORDER BY length DESC
LIMIT 25;

# SOAL 5
SELECT 
	rating as Rating,
    MAX(replacement_cost) AS ReplacementCostTertinggi,
    MIN(rental_duration) AS RentalDurasiTerendah,
    ROUND(AVG(length), 4) AS RataRataDurasi
FROM FILM
GROUP BY RATING
ORDER BY RATING;

# SOAL 8
SELECT city, country_id
FROM CITY
WHERE CITY LIKE '%d%a'
ORDER BY city ASC
LIMIT 15;

# SOAL 10
SELECT 
	title, 
    description, 
    length, 
    rating 
FROM film
WHERE title LIKE '%h'
	AND length > (SELECT AVG(length) FROM film)
ORDER BY title ASC
LIMIT 10;


# SOAL 6, 7 DAN 9.
# SOAL 6
SELECT 
    f.title AS Judul,
    f.length AS Durasi,
    l.name AS Bahasa_Film
FROM film f
JOIN language l ON f.language_id = l.language_id
WHERE f.title LIKE '%K'
LIMIT 15;

# SOAL 7
SELECT 
    f.title AS Judul_Film,
    a.first_name AS First_Name,
    a.last_name AS Last_Name
FROM film f
JOIN film_actor fa ON f.film_id = fa.film_id
JOIN actor a ON fa.actor_id = a.actor_id
WHERE a.actor_id = 14;

# SOAL 9
SELECT 
    c.name AS Genre,
    COUNT(f.film_id) AS Banyak_Film
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY Banyak_Film ASC;