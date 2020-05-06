import psycopg2
import psycopg2.extras
from load_data import connection_string


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
    def getEssentialDensityDelta(self, zipCode, newBiz):
        firstDensity = self.getEssentialDensity(zipCode)
        self.addEssentialBusiness(newBiz)
        secondDensity = self.getEssentialDensity(zipCode)
        self.removeEssentialBusiness(newBiz)
        return secondDensity - firstDensity

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

    essential_Businesses = ["Booting Company", "Process Server Individual", "Tow Truck Driver", 
        "Garage", "Laundry", "Employment Agency", "Tow Truck Company", "Tow Truck Exemption", "Laundries",
        "Stoop Line Stand", "Debt Collection Agency", "Newsstand", "Garage and Parking Lot", "Laundry Jobber",
        "Parking Lot", "Process Serving Agency", "Storage Warehouse"]

    def addEssentialBusiness(self, newBiz):
        industries = self.query("SELECT Industry FROM db_project.business GROUP BY Industry")
        if(newBiz not in industries): #Fail
            print("Business Type Not Found.")
            return False
        if(newBiz in self.essential_Businesses): #Do nothing because it's already there
            return True
        self.essential_Businesses.append(newBiz)
        return True

    def removeEssentialBusiness(self, remBiz):
        if(remBiz in self.essential_Businesses):
            self.essential_Businesses.remove(remBiz)  