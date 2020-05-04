import folium
import visualize as vs

# Query the Data and grab data
# put in 2d array [zip][essential]
# call function like below

nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)
dataset1, dataset2 = None, None 
vs.choropleth(nyMap, 'Layer1', "Test1", dataset1)
vs.choropleth(nyMap, 'Layer2', "Test2", dataset2)
vs.show(nyMap)
