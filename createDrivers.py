import json
import requests

# Change the endpoint as you need
endpoint_url = 'http://localhost:5002/Garages/'

import json
headers = {"Content-Type": "application/json" ,
           "Accept": 'application/json'}

with open('ParkingLotPreferences.json') as json_file:
    drivers = json.load(json_file)

for driver in drivers['drivers']:
    try:
        res = requests.post(endpoint_url, data=json.dumps(driver), headers=headers,timeout=3)
    except Exception as e:
        print(e)
        print(f'Error during update {driver}.\n')

print('End of Script')
