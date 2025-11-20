USE employees;


SELECT e.first_name, e.last_name
FROM employees e
JOIN dept_emp de ON e.emp_no = de.emp_no
WHERE de.dept_no IN (
    SELECT dept_no
    FROM employees e2
    JOIN dept_emp de2 ON e2.emp_no = de2.emp_no
    WHERE e2.first_name = 'Heng' AND e2.last_name = 'Giveon'
);

SELECT e.first_name, e.last_name, s.salary
FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no
WHERE YEAR(s.from_date) BETWEEN 2001 AND 2002
ORDER BY s.salary DESC
LIMIT 3;


SELECT gender, AVG(Total_Salary)
FROM (
    SELECT e.gender, s.emp_no, SUM(s.salary) AS Total_Salary
    FROM employees e
    JOIN salaries s ON e.emp_no = s.emp_no
    GROUP BY e.gender, s.emp_no
) AS mySubquery
GROUP BY gender;
