CREATE DATABASE coin_data;
USE coin_data;

CREATE TABLE metals (
  metal_id varchar(5) PRIMARY KEY,
  name varchar(255) NOT NULL,
  price decimal(30,10) NOT NULL,
  price_date date NOT NULL
);
-- Metal types
insert into metals(metal_id,name,price,price_date) values("au","gold",-1,"1000-01-01"),("ag","silver",-1,"1000-01-01"),("pd","palladium",-1,"1000-01-01"),("pt","platinum",-1,"1000-01-01"),("rh","rhodium",-1,"1000-01-01"),("other","unknown",-1,"1000-01-01");

CREATE TABLE tags (
  tag_id varchar(255) PRIMARY KEY,
  bullion boolean DEFAULT FALSE
);
-- Tags
INSERT INTO tags(tag_id) VALUES("none");
INSERT INTO tags(tag_id,bullion) VALUES("bullion",TRUE);

CREATE TABLE countries (
  country_id varchar(255) PRIMARY KEY,
  display_name varchar(255) NOT NULL,
  tags varchar(255) default "none",
  FOREIGN KEY (tags) REFERENCES tags(tag_id) ON UPDATE CASCADE
);

CREATE TABLE country_names (
  name varchar(255) PRIMARY KEY,
  country_id varchar(255) NOT NULL,
  FOREIGN KEY (country_id) REFERENCES countries(country_id) ON UPDATE CASCADE
);

CREATE TABLE denominations (
  denomination_id varchar(255) PRIMARY KEY,
  country_id varchar(255) NOT NULL,
  FOREIGN KEY (country_id) REFERENCES countries(country_id) ON UPDATE CASCADE,
  name varchar(255) NOT NULL,
  tags varchar(255) DEFAULT "none",
  FOREIGN KEY (tags) REFERENCES tags(tag_id) ON UPDATE CASCADE,
  alternative_name_1 varchar(255),
  alternative_name_2 varchar(255),
  alternative_name_3 varchar(255),
  alternative_name_4 varchar(255),
  alternative_name_5 varchar(255)
);

CREATE TABLE face_values (
  value_id varchar(255) PRIMARY KEY,
  denomination_id varchar(255) NOT NULL,
  FOREIGN KEY (denomination_id) REFERENCES denominations(denomination_id) ON UPDATE CASCADE,
  value decimal(20,10) NOT NULL,
  name varchar(255),
  tags varchar(255) DEFAULT "none",
  FOREIGN KEY (tags) REFERENCES tags(tag_id) ON UPDATE CASCADE,
  alternative_name_1 varchar(255),
  alternative_name_2 varchar(255),
  alternative_name_3 varchar(255),
  alternative_name_4 varchar(255),
  alternative_name_5 varchar(255)
);

CREATE TABLE coins (
  coin_id varchar(255) PRIMARY KEY,
  face_value_id varchar(255) NOT NULL,
  FOREIGN KEY (face_value_id) REFERENCES face_values(value_id) ON UPDATE CASCADE,
  gross_weight decimal(20,10) NOT NULL,
  fineness decimal(11,10) NOT NULL,
  precious_metal_weight decimal(20,10),
  years varchar(1024) NOT NULL,
  tags varchar(255) DEFAULT "none",
  FOREIGN KEY (tags) REFERENCES tags(tag_id) ON UPDATE CASCADE,
  metal varchar(5) NOT NULL,
  FOREIGN KEY (metal) REFERENCES metals(metal_id) ON UPDATE CASCADE,
  name varchar(255)
);

CREATE TABLE specific_coins (
  id int PRIMARY KEY AUTO_INCREMENT,
  coin_id varchar(255) NOT NULL,
  FOREIGN KEY (coin_id) REFERENCES coins(coin_id) ON UPDATE CASCADE,
  year int,
  mintmark varchar(255)
);

CREATE TABLE purchases (
  purchase_id int PRIMARY KEY AUTO_INCREMENT,
  coin_id varchar(255) NOT NULL,
  FOREIGN KEY (coin_id) REFERENCES coins(coin_id) ON UPDATE CASCADE,
  purchase_date date NOT NULL,
  unit_price decimal(30,10) NOT NULL,
  purchase_quantity int DEFAULT 1,
  specific_coin int,
  FOREIGN KEY (specific_coin) REFERENCES specific_coins(id) ON UPDATE CASCADE
);

