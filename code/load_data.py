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

            # Print a single row
            count = 0
            for row in csv_reader:
                count += 1
            print(count)




if __name__ == "__main__":
    main()
