import folium
import essentialData as ess

# Define our variables
nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)
mapDisp = ess.essentialData()

while(1):
    print("Running Database Systems Final Project...")
    print("Enter 'info' for a list of our features and how to use them")
    print("Enter 'quit' to Exit")
    val = input("Type a Command: ")
    if val == 'quit':
        print("Exiting Program...")
        break
    if val == 'display':
        mapDisp.show(nyMap)
    if val == 'add'
      #...
    if val == #...
      #...
