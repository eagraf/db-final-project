DROP SCHEMA IF EXISTS db_project CASCADE;
CREATE SCHEMA db_project;

CREATE TABLE db_project.test(
    a VARCHAR(15),
    b INT
);

CREATE TABLE db_project.zip(
    zip VARCHAR(5) PRIMARY KEY,
    lat FLOAT,
    lng FLOAT,
    city VARCHAR(255),
    state_id VARCHAR(2),
    state_name VARCHAR(255),
    zcta BOOLEAN,
    parent_zcta VARCHAR(255),
    population INT,
    density FLOAT,
    county_fips VARCHAR(5),
    county_name VARCHAR(255),
    county_weights VARCHAR(255),
    county_names_all VARCHAR(255),
    county_fips_all VARCHAR(255),
    imprecise BOOLEAN,
    military BOOLEAN,
    timezone VARCHAR(255)
);

CREATE TABLE db_project.business(
    license_numer VARCHAR(255) PRIMARY KEY,
    license_type VARCHAR(255),
    license_expiration_date DATE,
    license_status VARCHAR(255),
    license_creation_date DATE,
    industry VARCHAR(255),
    business_name VARCHAR(255),
    business_name_2 VARCHAR(255),
    address_building VARCHAR(255),
    address_street_name VARCHAR(255),
    secondary_address_street_name VARCHAR(255),
    address_city VARCHAR(255),
    address_state VARCHAR(255),
    address_zip VARCHAR(255),
    contact_phone VARCHAR(255),
    address_borough VARCHAR(255),
    borough_code VARCHAR(255),
    community_board VARCHAR(255),
    council_district VARCHAR(255),
    bin VARCHAR(255),
    bbl VARCHAR(255),
    nta VARCHAR(255),
    census_tract VARCHAR(255),
    detail VARCHAR(255),
    longitude FLOAT,
    latitude FLOAT,
    location VARCHAR(255)
);

GRANT ALL PRIVILEGES ON all tables in SCHEMA db_project TO finalproject;
