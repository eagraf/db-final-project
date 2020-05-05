import folium
import sys
sys.path.insert(0, '../visualization')
import essentialData as ess

nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)
test = ess.essentialData()
dataset1, dataset2 = None, None
# Should accept dataset of ['zip', 'essentials']
test.create_essential_Map(nyMap, dataset1)
test.create_essentialDensity_Map(nyMap, dataset2)
test.show(nyMap)