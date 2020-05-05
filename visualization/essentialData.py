import psycopg2
import psycopg2.extras
from folium import plugins
import pandas as pd
import numpy as np
import webbrowser
import folium

class essentialData:
    def __init__(self):
        self.conn = psycopg2.connect(host='localhost', dbname='dbms_final_project', user='farukhsaidmuratov', password='')

    def check_connectivity(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM db_project.business LIMIT 1")
        records = cursor.fetchall()
        return len(records) == 1

    def create_essential_Map(self):
        cursor = self.conn.cursor()
        cursor.execute("ALTER TABLE db_project.business  \
            DROP COLUMN IF EXISTS essential;")
        cursor.execute("ALTER TABLE db_project.business \
            ADD COLUMN essential boolean NOT NULL DEFAULT FALSE;")

        print("Getting essential businesses and creating column...")

        essential_Businesses = ["Booting Company", "Process Server Individual", "Tow Truck Driver", 
        "Garage", "Laundry", "Employment Agency", "Tow Truck Company", "Tow Truck Exemption", "Laundries",
        "Stoop Line Stand", "Debt Collection Agency", "Newsstand", "Garage and Parking Lot", "Laundry Jobber",
        "Parking Lot", "Process Serving Agency", "Storage Warehouse"]

        for business in essential_Businesses:
            query = "UPDATE db_project.business \
                SET essential=TRUE  \
                WHERE industry=%s"
            cursor.execute(query, (business,))
        self.conn.commit() 

        query = "SELECT address_zip FROM db_project.business WHERE essential=TRUE"
        cursor.execute(query)
        essential = cursor.fetchall()

        print("Loading essential zips into db...")

        df = pd.DataFrame(essential, columns=['zip']).dropna() 
        dupes = df.pivot_table(index=['zip'], aggfunc='size')

        df.sort_values('zip', inplace=True)
        df.drop_duplicates(subset=None, keep='first', inplace=True)

        df['essential'] = np.asarray(dupes)
        df['zip'] = df['zip'].astype(str)

        print("Creating ny choro map...")

        nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)   
        folium.Choropleth(geo_data='nyczip.geojson', data=df, columns=['zip', 'essential'], \
                        key_on='feature.properties.postalCode', fill_color='OrRd', fill_opacity=.7, \
                        legend_name='Essentials Per Zip').add_to(nyMap)
        nyMap.save('nycEssentialMap.html')
        webbrowser.open('nycEssentialMap.html')
        cursor.close()  

    def create_essentialDensity_Map(self):
        cursor = self.conn.cursor()
        cursor.execute("ALTER TABLE db_project.business  \
            DROP COLUMN IF EXISTS essential;")
        cursor.execute("ALTER TABLE db_project.business \
            ADD COLUMN essential boolean NOT NULL DEFAULT FALSE;")

        print("Getting essential businesses and creating column...")

        essential_Businesses = ["Booting Company", "Process Server Individual", "Tow Truck Driver", 
        "Garage", "Laundry", "Employment Agency", "Tow Truck Company", "Tow Truck Exemption", "Laundries",
        "Stoop Line Stand", "Debt Collection Agency", "Newsstand", "Garage and Parking Lot", "Laundry Jobber",
        "Parking Lot", "Process Serving Agency", "Storage Warehouse"]

        for business in essential_Businesses:
            query = "UPDATE db_project.business \
                SET essential=TRUE  \
                WHERE industry=%s"
            cursor.execute(query, (business,))
        self.conn.commit() 

        query = "SELECT address_zip, essential FROM db_project.business"
        cursor.execute(query)
        essential = cursor.fetchall()

        print("Loading essential zips into db...")

        df = pd.DataFrame(essential, columns=['zip', 'essential']).dropna() 
        df = df.groupby(['zip', 'essential']).size().reset_index(name='Count')

        print(df.head())
        
        # Create placeholder column for df density
        df['essentialDensity'] = np.nan

        print(df.head())

        for index, row in df.iterrows():
            zip_code = row["zip"]
            trueCount = (df[(df['essential'] == True) & (df['zip'] == zip_code)])["Count"]
            falseCount = (df[(df['essential'] == False) & (df['zip'] == zip_code)])["Count"]

            if(len(trueCount) == 0):
                trueCount = 0
            else:
                trueCount = trueCount.item()

            if(len(falseCount) == 0):
                falseCount = 0
            else:
                falseCount = falseCount.item()

            density = float(trueCount)/(float(trueCount) + float(falseCount))
            df.at[index, "essentialDensity"] = density

        print(df.head())

        df['zip'] = df['zip'].astype(str)
        df = df.drop(labels=['Count', 'essential'], axis=1)
        df.drop_duplicates(subset='zip', keep='first', inplace=True)

        print(df.head())

        print("Creating ny choro map...")

        nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)   
        folium.Choropleth(geo_data='nyczip.geojson', data=df, columns=['zip', 'essentialDensity'], \
                        key_on='feature.properties.postalCode', fill_color='OrRd', fill_opacity=.7, \
                        legend_name='Essentials Per Zip').add_to(nyMap)
        nyMap.save('nycEssentialDensityMap.html')
        webbrowser.open('nycEssentialDensityMap.html')
        cursor.close()  

test = essentialData()
test.create_essential_Map()



        