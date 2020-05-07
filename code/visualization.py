import psycopg2
import psycopg2.extras
from folium import plugins, LayerControl, FeatureGroup, Marker
import pandas as pd
import numpy as np
import webbrowser
import folium
import os
from load_data import connection_string
from folium.plugins import MarkerCluster


class visualization:
    valid_zips = (10453, 10457, 10460, 10458, 10467,
            10468, 10451, 10452, 10456, 10454,
            10455, 10459, 10474, 10463, 10471,
            10466, 10469, 10470, 10475, 10461,
            10462, 10464, 10465, 10472, 10473,
            11212, 11213, 11216, 11233, 11238,
            11209, 11214, 11228, 11204, 11218,
            11219, 11230, 11234, 11236, 11239,
            11223, 11224, 11229, 11235, 11201,
            11205, 11215, 11217, 11231, 11203,
            11210, 11225, 11226, 11207, 11208,
            11211, 11222, 11220, 11232, 11206,
            11221, 11237, 10026, 10027, 10030,
            10037, 10039, 10001, 10011, 10018,
            10019, 10020, 10036, 10029, 10035,
            10010, 10016, 10017, 10022, 10012,
            10013, 10014, 10004, 10005, 10006,
            10007, 10038, 10280, 10002, 10003,
            10009, 10021, 10028, 10044, 10065,
            10075, 10128, 10023, 10024, 10025,
            10031, 10032, 10033, 10034, 10040,
            11361, 11362, 11363, 11364, 11354,
            11355, 11356, 11357, 11358, 11359,
            11360, 11365, 11366, 11367, 11412,
            11423, 11432, 11433, 11434, 11435,
            11436, 11101, 11102, 11103, 11104,
            11105, 11106, 11374, 11375, 11379,
            11385, 11691, 11692, 11693, 11694,
            11695, 11697, 11004, 11005, 11411,
            11413, 11422, 11426, 11427, 11428,
            11429, 11414, 11415, 11416, 11417,
            11418, 11419, 11420, 11421, 11368,
            11369, 11370, 11372, 11373, 11377,
            11378, 10302, 10303, 10310, 10306,
            10307, 10308, 10309, 10312, 10301,
            10304, 10305, 10314)

    def __init__(self):
        self.conn = psycopg2.connect(connection_string)
        self.layered = False

    # Generate a dataframe with a zips column and a result column that is the "func" applied to all
    # the zips in NYC
    def generateZips(self, func, businessType=None):
        # Connect to db and get zips of nyc
        cursor = self.conn.cursor()
        zips = self.valid_zips

        # Create df w/ zip column and empty result column
        df = pd.DataFrame(zips, columns=['zip']).dropna()
        df['result'] = 0.0

        # Apply func to each zip code
        for index, row in df.iterrows():
            zip_code = row["zip"]
            if(businessType is None):
                result = func(int(zip_code))
            else:
                result = func(int(zip_code), businessType)
            # print(result, zip_code)
            df.at[index, "result"] = result
        
        # Pass completed df to essential_map which creates layer, and then show, which presents map
        nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)
        self.essential_map(nyMap, str(func.__name__), str(func.__name__), df)
        self.show(nyMap)

    # Ex Call:
    # essential_map(nyMap, 'Essential Density', 'Density Range', From Query Script in form [zip, essential])
    def essential_map(self, map, name, legend, dataset):
        choro = pd.DataFrame()
        choro['zip'] = dataset['zip'].astype(str)
        choro['essentials'] = dataset['result']
        # Put percent data on a scale so you can see differences better
        if(choro['essentials'].max() <= 1 and choro['essentials'].max() > 0.2):
            print("Percentages put on a square root scale to visualize differences (see visualization).")
            choro['essentials'] = np.power(choro['essentials'], 1/2)*100
        if(choro['essentials'].max() <= 0.2):
            print("Percentages all less than 20%, put on a scale to visualize difference (see visualization).")
            choro['essentials'] = np.power(choro['essentials'], 1)*100
        # print(choro['essentials'][50])
        tooltip = folium.GeoJsonTooltip(fields = ('zip','essential'))
        cLayer = folium.Choropleth(geo_data='nyczip.geojson', data=choro, columns=['zip', 'essentials'],
                                   key_on='feature.properties.postalCode', fill_color='OrRd', fill_opacity=.7,
                                   legend_name=legend, show=True, highlight=True)
        cLayer.geojson.add_child(folium.features.GeoJsonTooltip(['postalCode']))

        map.add_child(cLayer)
        cLayer.layer_name = name

    def show(self, map):
        if self.layered == False:
            LayerControl(collapsed=False).add_to(map)
            self.layered = True
        map.save('nycLayeringEssential.html')
        return os.path.abspath('nycLayeringEssential.html')
