import folium
import essentialData as ed

nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)
test = ed.essentialData()

test.create_essentialDensity_Map(nyMap)
test.create_essential_Map(nyMap)
test.show(nyMap)
