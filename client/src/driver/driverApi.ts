const getAgentsApi = async () => {
    const response = await window.fetch(`localhost:5001/Passengers`, {
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

const agentMock = [
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent2",
        "name": "agentName",
        "currentLocationLat": "56'34",
        "currentLocationLong": "53'23",
        "endLocationLat": "52'34",
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
    {
        "id": "agent1",
        "name": "string",
        "currentLocationLat": 0,
        "currentLocationLong": 0,
        "endLocationLat": 0,
        "endLocationLong": 0,
        "costPreference": 0
    },
]

export {getAgentsApi, agentMock}
