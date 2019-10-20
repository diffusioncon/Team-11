from middleLayer.driverApi import app as driverApi
from middleLayer.garageApi import app as garageApi
from middleLayer.contractApi import app as contractApi
from middleLayer.contractApi import pathFinding as pF


import json
import requests

from multiprocessing import Process
import time
"""
Main entry to the application. Here we spin up our API's

"""
# here we configure our endpoints
currentApis = {5001:driverApi.app,
               5002:garageApi.app,
               5003:contractApi.app,
               }

# helper function to start the server
def startSterver(server, port):
    server.run(port=port, host="0.0.0.0", debug=True)

# here we spin up a thread for each api
SERVERS = list()

def movePieces(newRoute):
    contract, pathToPassenger, pathToDest = newRoute
    interval = 105
    #  here we need to generate the path from the driver to the passenger
    print("Here!")
    while True:
        time.sleep(interval)
        print("Here!")
        if not pathToPassenger:
            break
        else:
            nextCurX, nextCurY  = pathToPassenger.pop(0)
            pathFinder = pF.pathFinder()
            nextCurX, nextCurY = pathFinder.XYToLatLong(nextCurX, nextCurY)
            print(nextCurX, nextCurY)

            headers = {"Content-Type": "application/json" ,
                       "Accept": 'application/json'}
            data = {
                   "currentLocationLat": nextCurX,
                   "currentLocationLong": nextCurY
            }

            res = requests.put("http://localhost:5002/Drivers/{}".format(contract["driverId"]),
                               data=json.dumps(data),
                               headers=headers)

    # here we move both passenger and driver
    while True:
        time.sleep(interval)
        if not pathToDest:
            break
        else:
            nextCurX, nextCurY  = pathToDest.pop(0)
            pathFinder = pF.pathFinder()
            nextCurX, nextCurY = pathFinder.XYToLatLong(nextCurX, nextCurY)
            print(nextCurX, nextCurY)

            data = {"currentLocationLat": nextCurX,
                    "currentLocationLong": nextCurY}

            headers = {"Content-Type": "application/json" ,
                       "Accept": 'application/json'}
            res = requests.put("http://localhost:5002/Drivers/{}".format(contract["driverId"]), data=json.dumps(data),
                               headers=headers)
            res = requests.put("http://localhost:5001/Passengers/{}".format(contract["passengerId"]), data=json.dumps(data),
                               headers=headers)

    # here we update the status of the contract to passenger dropped
    data = {"status": "passengerDropped"}
    res = requests.put("http://localhost:5003/Contracts/{}".format(contract["id"]),
                                       data=json.dumps(data),
                                       headers=headers)

    # now we update the driver to be free again
    data = {"status": "available"}

    res = requests.put("http://localhost:5002/Drivers/{}".format(contract["driverId"]),
                                       data=json.dumps(data),
                                       headers=headers)
    # now we clear the remaining passenger
    res = requests.delete("http://localhost:5001/Passengers/{}".format(contract["passengerId"]),
                          headers=headers)

def main():
    threads = [Process(target=startSterver,
                       args=[s, i]) for i, s in currentApis.items()]
    [t.start() for t in threads]
    [SERVERS.append(t) for t in threads]
    # we wait for our ledger to spin up
  #  while True:
  #      print("HERE ABOUT TO PICK UP")
  #      newRoute = contractApi.PATHS_TO_UPDATE.get()
  #      time.sleep(100)
  #      Process(target=movePieces, args=[newRoute]).start()



def kill():
    [t.stop() for t in SERVERS]






if __name__ == "__main__":
    main()

