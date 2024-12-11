#CREATE TABLE my_tb (
 	id INT PRIMARY KEY AUTO_INCREMENT,
    firstname varchar(30) not null,
    middlename varchar(30),
    lastname varchar(30) not null,
    birthday date not null,
    age int(2) not null,
    contact varchar(11) UNIQUE,
    email varchar(320) UNIQUE,
    username varchar(100) UNIQUE not null,
    password varchar(300) not null
);


CREATE TABLE crud_tb (
 	id INT PRIMARY KEY AUTO_INCREMENT,
    firstname varchar(30) not null,
    middlename varchar(30),
    lastname varchar(30) not null,
    birthday date not null,
    age int(2) not null,
    contact varchar(11) UNIQUE,
    email varchar(320) UNIQUE
);