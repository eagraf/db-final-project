import folium
import sys

sys.path.append('../visualization')

import database as db
import visualization as vis

# Define our variables
nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)
mapObj = vis.visualization()
dbObj = db.database()

print('\nRunning Database Systems Final Project...')
print("\n-Enter 'info' for a list of our features and how to use them")
print("-Enter 'exit' to Exit\n")
while(1):
    inp = input('Type a Command: ')

    values = inp.split()
    val = values[0]
    zipcode = 11001
    if(len(values) == 2):
        zipcode = int(values[1])
    elif(len(values) >= 3):
        zipcode = int(values[1])
        newBiz = values[2:]
    elif(len(values) != 1):
        print("Invalid input")
    
    if val == 'exit':
        print('\nExiting Program...\n')
        break
    elif val == 'info':
        print("Please see readme.md for command documentation.")
    elif val == 'display':
        print('\nDisplaying Map...\n')
        print(mapObj.show(nyMap))
    elif val == 'listEssential':
        print("Displaying essential businesses")
        print(dbObj.essential_Businesses)
    elif val == "listBusinesses":
        print("Displaying all business categories")
        print(dbObj.listValidBiz())
    elif val == "listValidZips":
        print("Displaying all valid zip codes")
        print(dbObj.listValidZips())
    elif val == 'getEssentialPercent':
        print("Displaying the essential percentage for", zipcode)
        print(dbObj.getEssentialDensity(zipcode)) #TODO Format as a percentage
        mapObj.generateZips(dbObj.getEssentialDensity)
    elif val == "getEssentialDelta":
        print("Displaying the delta in essential percentage if","was an essential business.")
        print(dbObj.getEssentialDensityDelta(zipcode, newBiz))
        mapObj.generateZips(dbObj.getEssentialDensityDelta)
    elif val == "totalEssential":
        print("The essential percentage for all of NYC is:")
        print(dbObj.getTotalEssential())
        mapObj.generateZips(dbObj.getEssentialDensity)
    elif val == "population":
        print("The population in", "is:")
        print(dbObj.getPopulation(zipcode))
        mapObj.generateZips(dbObj.getPopulation)
    elif val == "popToEssential":
        print("The population to number of essential businesses is:")
        print(dbObj.getPopToEssential(zipcode))
        mapObj.generateZips(dbObj.getPopToEssential)
    elif val == "denToEssential":
        print("The population to number of essential businesses is:")
        print(dbObj.getDenToEssential(zipcode))
        mapObj.generateZips(dbObj.getDenToEssential)
    else:
        print('\nInvalid Input\n')
    
