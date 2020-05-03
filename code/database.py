import psycopg2
import psycopg2.extras
from load_data.py import connection_string


class database:
    conn = psycopg2.connect(connection_string)
    
    def query(self, query, parameters=()):
        cursor = self.conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    # Get % of essential businesses
    def getEssentialDensity(self, zipCode):
        return None
    
    # Show change in essential density after changing essential list
    def getEssentialDensityDelta(self, zipCode):
        return None

    def getIndustriesInZipCode(self, zipCode):
        q = "SELECT Industry FROM db_project.business WHERE address_zip = %s GROUP BY Industry"
        return self.query(q, zipCode)

