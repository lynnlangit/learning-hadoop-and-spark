SELECT Persons.LastName, Persons.FirstName
FROM
  Persons
WHERE
( Persons.City = 'Bergen')
ORDER BY Persons.LastName DESC;

