import psycopg2
import psycopg2.extras
from folium import plugins, LayerControl, FeatureGroup, Marker
import pandas as pd
import numpy as np
import webbrowser
import folium

class essentialData:
    def __init__(self):
        self.conn = psycopg2.connect("host='localhost' dbname='finalproject' user='finalproject' password='pass'")
        self.layered = False

    def check_connectivity(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM db_project.business LIMIT 1")
        records = cursor.fetchall()
        return len(records) == 1

    def create_essential_Map(self, map, dataset):
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

        dfCount = pd.DataFrame(essential, columns=['zip']).dropna() 
        dupes = dfCount.pivot_table(index=['zip'], aggfunc='size')

        dfCount.sort_values('zip', inplace=True)
        dfCount.drop_duplicates(subset=None, keep='first', inplace=True)

        dfCount['essential'] = np.asarray(dupes)
        dfCount['zip'] = dfCount['zip'].astype(str)

        print("Creating ny choro count map...")

        countMap = folium.Choropleth(geo_data='nyczip.geojson', data=dfCount, columns=['zip', 'essential'], \
                        key_on='feature.properties.postalCode', fill_color='OrRd', fill_opacity=.7, \
                        legend_name='Essentials Per Zip', show=False)
        map.add_child(countMap)

        query = "SELECT address_zip, essential FROM db_project.business"
        cursor.execute(query)
        essential = cursor.fetchall()
        cursor.close() 

        dfDense = pd.DataFrame(essential, columns=['zip', 'essential']).dropna() 
        dfDense = dfDense.groupby(['zip', 'essential']).size().reset_index(name='Count')
    
        # Create placeholder column for df density
        dfDense['essentialDensity'] = np.nan

        for index, row in dfDense.iterrows():
            zip_code = row["zip"]
            trueCount = (dfDense[(dfDense['essential'] == True) & (dfDense['zip'] == zip_code)])["Count"]
            falseCount = (dfDense[(dfDense['essential'] == False) & (dfDense['zip'] == zip_code)])["Count"]

            if(len(trueCount) == 0):
                trueCount = 0
            else:
                trueCount = trueCount.item()

            if(len(falseCount) == 0):
                falseCount = 0
            else:
                falseCount = falseCount.item()

            density = float(trueCount)/(float(trueCount) + float(falseCount))
            dfDense.at[index, "essentialDensity"] = density

        dfDense['zip'] = dfDense['zip'].astype(str)
        dfDense = dfDense.drop(labels=['Count', 'essential'], axis=1)
        dfDense.drop_duplicates(subset='zip', keep='first', inplace=True)

        print("Creating ny choro dense map...")

        densityMap = folium.Choropleth(geo_data='nyczip.geojson', data=dfDense, columns=['zip', 'essentialDensity'], \
                        key_on='feature.properties.postalCode', fill_color='OrRd', fill_opacity=.7, \
                        legend_name='Essentials Per Zip', show=False)
        map.add_child(densityMap)
    
    # Generalization of create_essential_Map() Function above
    # Ex Call: 
    # essential_map(nyMap, 'Essential Density', 'Density Range', From Query Script in form [zip, essential])
    def essential_map(self, map, name, legend, dataset):
        choro = pd.DataFrame()
        choro['zip'] = dataset[0].astype(str)
        choro['essentials'] = dataset[1]         
        cLayer = folium.Choropleth(geo_data='nyczip.geojson', data=choro, columns=['zip', 'essentials'], \
                            key_on='feature.properties.postalCode', fill_color='OrRd', fill_opacity=.7, \
                            legend_name=legend, show=False)
        map.add_child(cLayer)
        cLayer.layer_name = name

    def show(self, map):
        if self.layered == False:
            LayerControl(collapsed=False).add_to(map)
            self.layered = True
        map.save('nycLayeringEssential.html')
        webbrowser.open('nycLayeringEssential.html')



        
