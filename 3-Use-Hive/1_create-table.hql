CREATE TABLE Persons1000 (
   LastName varchar(255),
   FirstName varchar(255),
   Address varchar(255),
   City varchar(255)
);

INSERT INTO Persons1000
VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger');

INSERT INTO Persons1000
VALUES ('Cardinal', 'Sue Bee', 'Skagen 41', 'Oslo');

INSERT INTO Persons1000
VALUES ('Bluebird', 'Beatrice Erichsen', 'Skaagen 211', 'Bergen');

update persons1000 
set address = 'thisaddress';