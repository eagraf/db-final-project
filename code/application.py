import folium
import database as db
import essentialData as ess

# Define our variables
nyMap = folium.Map(location=[40.7128, -74.0060], titles='Stamen Toner', zoom_start=11)
mapObj = ess.essentialData()
dbObj = db.database()

print('\nRunning Database Systems Final Project...')
print("\n-Enter 'info' for a list of our features and how to use them")
print("-Enter 'exit' to Exit\n")
while(1):
    val = input('Type a Command: ')
    if val == 'exit':
        print('\nExiting Program...\n')
        break
    elif val == 'display':
        print('\nDisplaying Map...\n')
        mapObj.show(nyMap)
    elif val == 'add':
        print('Enter a list of your essential businesses: ')
    elif val == 'query':
        print('querying')
    else:
        print('\nInvalid Input\n')
    
