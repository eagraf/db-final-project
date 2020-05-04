from folium import plugins, LayerControl, FeatureGroup
import pandas as pd
import webbrowser
import folium
import json
import sample

#https://morioh.com/p/d896544d6977
#https://www.storybench.org/how-to-build-a-heatmap-in-python/

nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11) 

# should take longitude latitude data
def heatmap(name):
    df = pd.read_csv("sampleCoords.csv")
    with open('nyczip.geojson') as f: nycArea = json.load(f)
    folium.GeoJson(nycArea).add_to(nyMap)
    for i, row in df.iterrows():
        folium.CircleMarker((row.latitude, row.longitude), radius=3, weight=2, color='red', \
                            fill_color='red', fill_opacity=.5)
    nyMap.add_child(plugins.HeatMap(data=df[['latitude', 'longitude']].values, radius=24, blur=10))


# should take zicode data, black on the map=essentials
def choropleth(cLayer, name):
    choro = sample.generateSampleZips()  
    cLayer = folium.Choropleth(geo_data='nyczip.geojson', data=choro, columns=['zip', 'essentials'], \
                        key_on='feature.properties.postalCode', fill_color='OrRd', fill_opacity=.7, \
                        legend_name='Essentials Per Zip')
    nyMap.add_child(cLayer)
    cLayer.layer_name = name
    LayerControl().add_to(nyMap)

#heatmap()
c1, c2 = None, None
choropleth(c1, 'Layer1')

nyMap.save('nycLayering.html')
webbrowser.open('nycLayering.html')