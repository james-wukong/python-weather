## create database and tables

```sh
# , in the csv file needs to be transformed into \, before this could work
sed -i 's/,/\\,/g' input.csv
awk 'NR%2==1{gsub(",","~")}1' RS='"' ORS='"' infile
```

```sql
CREATE DATABASE IF NOT EXISTS `weather`;
SHOW DATABASES;
USE `weather`;
CREATE TABLE IF NOT EXISTS hourly_data (
    name STRING, datetime DATE, temp INT, feelslike DECIMAL(10, 4), dew DECIMAL(10, 4), humidity DECIMAL(10, 4), precip DECIMAL(10, 4), precipprob INT, preciptype STRING, snow DECIMAL(10, 4), snowdepth DECIMAL(10, 4), windgust DECIMAL(10, 4), windspeed DECIMAL(10, 4), winddir DECIMAL(10, 4), sealevelpressure DECIMAL(10, 4), cloudcover DECIMAL(10, 4), visibility DECIMAL(10, 4), solarradiation DECIMAL(10, 4), solarenergy DECIMAL(10, 4), uvindex INT, severerisk INT, conditions STRING, icon STRING, stations STRING) 
    ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n';
DESCRIBE `hourly_data`;
```

