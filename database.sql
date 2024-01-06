--Сначала создать вручную базу
--CREATE DATABASE parse;
--Затем выполнить команду
--C:\"Program Files"\PostgreSQL\16\bin\psql.exe -f database.sql -U postgres -d parse
CREATE TABLE IF NOT EXISTS users (
id serial PRIMARY KEY,
tg_chat integer
);

CREATE TABLE IF NOT EXISTS products (
article integer,
name varchar(80),
price integer,
url varchar(150),
last_update timestamp,
user_id integer REFERENCES users(id)
);

