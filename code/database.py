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
        #Get total # of businesses in zip
        #Get total # of essential businesses in that list (use a sub query)
        #Return essential/total
        return None
    
    # Show change in essential density after changing essential list
    def getEssentialDensityDelta(self, zipCode):
        #Get essential density before change, get density after change
        return None

    def getMedianIncome(self, zipCode):
        return None
    
    def getMedianAge(self, zipCode):
        return None

    # Get essential % for all of nyc
    def getTotalEssential(self):
        return None

    def getIndustriesInZipCode(self, zipCode):
        q = "SELECT Industry FROM db_project.business WHERE address_zip = %s GROUP BY Industry"
        return self.query(q, zipCode)

    # TODO make a python list of essential industries that's modifiable
    def addEssentialBusiness(self, newBiz):
        #Check that newBiz is in the valid industry
        return None

    def removeEssentialBusiness(self, remBiz):
        return None   