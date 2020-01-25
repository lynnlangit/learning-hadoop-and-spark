CREATE TABLE Persons1000 (
   LastName varchar(255),
   FirstName varchar(255),
   Address varchar(255),
   City varchar(255)
);

INSERT INTO Persons1000
VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger');

update persons1000 
set address = 'thisaddress';