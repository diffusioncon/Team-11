const getContractsApi = async () => {
    const response = await window.fetch(`localhost:5003/Contracts`, {
        method: "GET",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
    })
    return {
        status: response.status,
        data: await (response.json())
    }
}

const contractsMock = [{
    "id": 1,
    "status": "funds_in_escrow",
    "passengerId": "Passenger12659487954",
    "driverId": "b39324486804719734017653823513bSefYMABS3932448680471973401765382351",
    "startLocationLat": 0,
    "startLocationLong": 0,
    "destinationLocationLat": 0,
    "destinationLocationLong": 0,
    "cost": 0
},
    {
        "id": 2,
        "status": "funds_in_escrow",
        "passengerId": "Passenger223936716259",
        "driverId": "b39324486804719734017653823513bSefYMABS3932448680471973401765382351",
        "startLocationLat": 0,
        "startLocationLong": 0,
        "destinationLocationLat": 0,
        "destinationLocationLong": 0,
        "cost": 0
    }
]


export {getContractsApi, contractsMock}