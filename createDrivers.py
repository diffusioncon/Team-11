import json
import requests

# Change the endpoint as you need
endpoint_url = 'http://localhost:5002/Garages/'

with open('ParkingLotPreferences.json') as json_file:
    drivers = json.load(json_file)

headers = {"accept": "application/json",
           "Content-Type": "application/json",}
import json
for driver in drivers['drivers']:
    print(driver)
    res = requests.post(endpoint_url,
                        headers=headers,
                        data=json.dumps(driver),
                        timeout=3)
    print(f'Error during update {driver}.\n')
    print(res.content)
print('End of Script')
