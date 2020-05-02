import psycopg2
import psycopg2.extras
import csv

connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"

# TODO add your code here (or in other files, at your discretion) to load the data


def main():
    # TODO invoke your code to load the data into the database
    print("Loading data")

    # Get db connection
    conn = psycopg2.connect(connection_string)

    # Read in input data
    with conn.cursor() as cursor:
        # Load schema
        with open('schema.sql', 'r') as schema:
            setup_queries = schema.read()
            cursor.execute(setup_queries)
        conn.commit()

        # Load zip data
        with open('datasets/uszips.csv', 'r') as zip_data:
            csv_reader = csv.reader(zip_data, delimiter=',')

            first = True
            for row in csv_reader:
                if not first:
                    query = "INSERT INTO db_project.zip (zip, lat, lng, city, state_id, state_name, zcta, \
                        parent_zcta, population, density, county_fips, county_name, county_weights, \
                        county_names_all, county_fips_all, imprecise, military, timezone) \
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    cursor.execute(query, row)
                    conn.commit()
                else:
                    first = False

        # Load business data
        with open('datasets/Legally_Operating_Businesses.csv') as business_data:
            csv_reader = csv.reader(business_data, delimiter=',')

            first = True
            for row in csv_reader:

                clean_row = [ None if a=='' else a for a in row ]
                if not first:
                    query = "INSERT INTO db_project.business (license_numer, license_type, \
                        license_expiration_date, license_status, license_creation_date, industry, \
                        business_name, business_name_2, address_building, address_street_name, \
                        secondary_address_street_name, address_city, address_state, address_zip, \
                        contact_phone, address_borough, borough_code, community_board, council_district, \
                        bin, bbl, nta, census_tract, detail, longitude, latitude, location) \
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    try:
                        cursor.execute(query, clean_row)
                    except Exception:
                        conn.rollback()
                    conn.commit()
                else:
                    first = False


if __name__ == "__main__":
    main()
