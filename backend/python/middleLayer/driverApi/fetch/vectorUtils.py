import math
import numpy as np


def distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def calcPassengerWaitTime(driver, startLat, startLong):
    avgKMPerH = 30
    return distance((startLat, startLong),
                    (driver["currentLocationLat"], driver["currentLocationLong"])) / avgKMPerH

def calcDriverFunction(driver, passenger):
    avgKMPerH = 30
    startLocation = passenger["currentLocationLat"], passenger["currentLocationLong"]
    endLocation = passenger["endLocationLat"], passenger["endLocationLong"]
    distance_from_home_for_driver_start = distance((startLocation[0], startLocation[1]),
                                                   (driver["currentLocationLat"],
                                                    driver["currentLocationLong"])) / avgKMPerH
    print(driver)
    distance_from_home_for_driver_stop = distance((endLocation[0], endLocation[1]),
                                                   (passenger["endLocationLat"],
                                                    passenger["endLocationLong"])) / avgKMPerH

    return (distance_from_home_for_driver_stop +
            distance_from_home_for_driver_start)




def createPassengerContractVector(passenger, driver):
    print("Passenger",passenger )
    passengerVect = np.array(
        [passenger['costPreference'],
         calcPassengerWaitTime(driver,
            startLat=passenger["currentLocationLat"],
            startLong=passenger["currentLocationLong"])],     
         dtype=float)
    print(passengerVect)
    return passengerVect

def createDriverContractVector(driver, passenger):
    print("DRIVER", driver)
    driver = np.array([driver['pricePreference'],
                       calcDriverFunction(driver, passenger)],
                     dtype=float)

    print(driver)
    return driver



def check_match(driver, passenger):
    return abs(sum(createDriverContractVector(driver, passenger) - \
               createPassengerContractVector(passenger, driver)))

