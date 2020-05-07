import psycopg2
import psycopg2.extras
from load_data import connection_string


class database:
    essential_Businesses = ["Booting Company", "Process Server Individual", "Tow Truck Driver", 
        "Garage", "Laundry", "Employment Agency", "Tow Truck Company", "Tow Truck Exemption", "Laundries",
        "Stoop Line Stand", "Debt Collection Agency", "Newsstand", "Garage and Parking Lot", "Laundry Jobber",
        "Parking Lot", "Process Serving Agency", "Storage Warehouse"]
    conn = psycopg2.connect(connection_string)

    #Initializes set essential businesses in database
    def __init__(self):
        q = "ALTER TABLE db_project.business ADD COLUMN ess int default 0" # Add ess col and default to NOT essential
        self.query(q, zipCode)[0]
        for biz in essential_Businesses: 
            q = "update db_project.business set ess = 1 where industry = '%s'"
            self.query(q, [zipCode,biz])[0]

    def query(self, query, parameters=()):
        cursor = self.conn.cursor()
        cursor.execute(query, parameters)
        return cursor.fetchall()

    # Get % of essential businesses
    def getEssentialDensity(self, zipCode):
        #Get total # of businesses in zip
        q = "SELECT COUNT(*) FROM db_project.business WHERE address_zip = '%s'"
        bus_total = self.query(q, zipCode)[0]

        #Get total # of essential businesses in that list (use a sub query)
        q = "SELECT COUNT(*) FROM db_project.business WHERE address_zip = '%s' AND Industry = '%s' AND ess = 1"
        ess_total = self.query(q, [zipCode,biz])[0]
        return ess_total/bus_total
    
    # Show change in essential density after changing essential list
    def getEssentialDensityDelta(self, zipCode, newBiz):
        firstDensity = self.getEssentialDensity(zipCode)
        self.addEssentialBusiness(newBiz)
        secondDensity = self.getEssentialDensity(zipCode)
        self.removeEssentialBusiness(newBiz)
        return secondDensity - firstDensity

    # Get essential % for all of nyc
    def getTotalEssential(self):
        q = "SELECT COUNT(*) FROM db_project.business where ess = 1"
        return self.query(q, [zipCode,biz])[0]

    def getIndustriesInZipCode(self, zipCode):
        q = "SELECT Industry FROM db_project.business WHERE address_zip = '%s' GROUP BY Industry"
        return self.query(q, zipCode)[0]

    def getEssentialIndustriesInZipCode(self, zipCode):
        q = "SELECT Industry FROM db_project.business WHERE address_zip = '%s' and ess = 1 GROUP BY Industry"
        return self.query(q, zipCode)[0]

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

    # Takes in Zipcode and then queries population from zip
    # and queries # of essential from business
    # Returns population / # of essential businesses in a zipcode
    def getPoptoEssential(self, zipCode):
        q = "SELECT population/count(*) FROM db_project.business JOIN db_project.zip ON db_project.business.address_zip = db_project.zip.zip WHERE address_zip = '%s' and ess = 1 group by population"
        return self.query(q, zipCode)[0]


    def getPoptoIndustry(self, industry ,zipCode):
        q = "SELECT population/count(*) FROM db_project.business JOIN db_project.zip ON db_project.business.address_zip = db_project.zip.zip WHERE address_zip = '%s' and industry = '%s' = 1 group by population"
        return self.query(q, [zipCode,industry])[0]