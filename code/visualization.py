import psycopg2
import psycopg2.extras
from folium import plugins, LayerControl, FeatureGroup, Marker
import pandas as pd
import numpy as np
import webbrowser
import folium
import os
from load_data import connection_string

class visualization:
    def __init__(self):
        self.conn = psycopg2.connect(connection_string)
        self.layered = False

    # Generate a dataframe with a zips column and a result column that is the "func" applied to all
    # the zips in NYC 
    def generateZips(self, func):
        # Connect to db and get zips of nyc 
        cursor = self.conn.cursor()
        query = "SELECT DISTINCT address_zip FROM db_project.business"
        cursor.execute(query)
        zips = cursor.fetchall()

        # Create df w/ zip column and empty result column 
        df = pd.DataFrame(essential, columns=['zip']).dropna() 
        df['result'] = 0

        # Apply func to each zip code 
        for index, row in df.iterrows():
            zip_code = row["zip"]
            result = func(zip_code)
            df.at[index, "result"] = result

        # Pass completed df to essential_map which creates layer, and then show, which presents map
        nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)
        self.essential_map(nyMap, func.__qualname__, func.__qualname__, df)
        self.show(nyMap)
    
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
        return os.path.abspath('nycLayeringEssential.html')



        
