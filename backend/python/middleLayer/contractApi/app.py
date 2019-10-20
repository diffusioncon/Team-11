from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
import json
# https://flask-restplus.readthedocs.io/en/stable/example.html
from flask_cors import CORS
app = Flask(__name__, )
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='ContractMVC API',
    description='A simple ContractMVC API',
)
CORS(app)

from multiprocessing import Queue

import math
PATHS_TO_UPDATE = Queue()


ns = api.namespace('Contracts', description='Contract operations')

Contract = api.model('Contract', {
    'id': fields.Integer(readOnly=True,
                         description='The Contract unique identifier'),
    'status': fields.String(required=True,
                          description='The Contracts status'),
    'passengerId': fields.String(required=True,
                          description='The Contracts passengerId Latitude'),

    'driverId': fields.String(required=True,
                          description='The Contracts clientId Latitude'),

    'startLocationLat': fields.Float(required=True,
                          description='The Contracts start Latitude'),


    'startLocationLong': fields.Float(required=True,
                          description='The Contract start Longitude'),

    'destinationLocationLat': fields.Float(required=True,
                          description='The Contracts destination Latitude'),

    'destinationLocationLong': fields.Float(required=True,
                          description='The Contract destination Longitude'),

    'cost': fields.Float(required=True,
                          description='The Contracts cost')

})


from threading import Thread
from pathFinding import pathFinder

pathFinder = pathFinder()




def generateUpdatePath(path):

    def driveToLoc(currentPos, nextPos):
        speed = 1
        driverX, driverY = currentPos
        nextX, nextY = nextPos
        dx, dy = nextX - driverX, nextY-driverY
        theta = math.atan2(dy, dx);
        newX = driverX + (5 * math.cos(theta))
        newY = driverY + (5 * math.sin(theta))
        return (newX, newY)

    def isAtNode(nodePos, currPos):
        diff = 5
        if currPos[0] - diff < nodePos[0] < currPos[0] + diff and currPos[1] - diff < nodePos[1] < currPos[1] + diff:
            return True
        return False
    updatePath = []
    currPos = path.pop()
    while path:
        nextNode = path.pop()
        while not isAtNode(nextNode, currPos):
            currPos = driveToLoc(currPos, nextNode)
            # print(currPos)
            updatePath.append(currPos)
            if currPos[0] > 1000 or currPos[1] > 1000:
                break
    return updatePath



import requests
class ContractDAO(object):

    def __init__(self):
        self.counter = 0
        self.OEF_AGENTS = {}
        self.Contracts = []

    def get(self, id):
        for Contract in self.Contracts:
            if Contract['id'] == id:
                return Contract
        api.abort(404, "Contract {} doesn't exist".format(id))

    def create(self, data):
        Contract = data
        Contract['id'] = self.counter = self.counter + 1
        # here we need to calculate the cost
        # plus convert the lat and the long to a node
        # we find out how long the driver will take to get to the passenger
        print(data, "<<<<<<<<<<<<<<<<<<<<<<")
        res = requests.get("http://garage_api:5000/Garages/{}".format(data["driverId"]))

        driver = json.loads(res.content)
        end = pathFinder.convertLatLongtoNode(data["startLocationLat"],
                           data["startLocationLong"])
        start = pathFinder.convertLatLongtoNode(data["destinationLocationLat"],
                           data["destinationLocationLong"])
        pathToDest = (pathFinder.findPath(start[0], end[0]))


        start = pathFinder.convertLatLongtoNode(data["startLocationLat"],
                           data["startLocationLong"])

        print(driver)
        end = pathFinder.convertLatLongtoNode(driver["currentLocationLat"],
                           driver["currentLocationLong"])

        pathToPassenger = (pathFinder.findPath(start[0], end[0]))


        # we update our contract with our costs
        print("To Passenger", pathToPassenger)

        journeyRoute = generateUpdatePath(pathToDest)
        pickupRoute = generateUpdatePath(pathToPassenger)

        print("To Passenger", pickupRoute)


        Contract["cost"] = len(journeyRoute)  * driver["pricePreference"]# must implement driver cost pref

        PATHS_TO_UPDATE.put((Contract, pickupRoute, journeyRoute))


        self.Contracts.append(Contract)
        return Contract

    def update(self, id, data):
        Contract = self.get(id)
        Contract.update(data)
        return Contract

    def delete(self, id):
        Contract = self.get(id)
        self.Contracts.remove(Contract)

DAO = ContractDAO()
@ns.route('/')
class ContractList(Resource):
    '''Shows a list of all Contracts, and lets you POST to add new Contracts'''
    @ns.doc('list_Contracts')
    @ns.marshal_list_with(Contract)
    def get(self):
        '''List all Contracts'''
        return DAO.Contracts

    @ns.doc('create_Contract')
    @ns.expect(Contract)
    @ns.marshal_with(Contract, code=201)
    def post(self):
        '''Create a new Contract'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Contract not found')
@ns.param('id', 'The Contract identifier')
class Contract(Resource):
    '''Show a single Contract item and lets you delete them'''
    @ns.doc('get_Contract')
    @ns.marshal_with(Contract)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_Contract')
    @ns.response(204, 'Contract deleted')
    def delete(self, id):
        '''Delete a Contract given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(Contract)
    @ns.marshal_with(Contract)
    def put(self, id):
        '''Update a Contract given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=5000)
