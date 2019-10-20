from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from threading import Thread
# https://flask-restplus.readthedocs.io/en/stable/example.html
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='DriverMVC API',
    description='A simple DriverMVC API',
)
from fetch.client_agent import makeAgent
ns = api.namespace('Drivers', description='Driver operations')



from flask_cors import CORS
CORS(app)


Driver = api.model('Driver', {
    'id': fields.String(readOnly=True,
                         description='The Driver unique identifier'),
    'name': fields.String(required=True,
                          description='The Drivers Name'),
    'currentLocationLat': fields.Float(required=True,
                          description='The Drivers current Latitude'),

    'currentLocationLong': fields.Float(required=True,
                          description='The Driver current Longitude'),

    'endLocationLat': fields.Float(required=True,
                          description='The Drivers current Latitude'),

    'distanceDest': fields.Float(required=True,
                          description='The Drivers preference for distance from the destination'),

    'timeOfStay': fields.Float(required=True,
                          description='The Drivers preference for distance from the destination'),

    'endLocationLong': fields.Float(required=True,
                          description='The Driver current Longitude'),

    'costPreference': fields.Float(required=True,
                          description='The Drivers Name'),
})



class DriverDAO(object):
    def __init__(self):
        self.counter = 0
        self.Drivers = []
        self.OEF_AGENTS = {}

    def get(self, id):
        for Driver in self.Drivers:
            if Driver['id'] == id:
                return Driver
        api.abort(404, "Driver {} doesn't exist".format(id))

    def create(self, data):
        Driver = data
        print(data)
        Driver['id'] = self.counter = self.counter + 1

        # here we create the agent for the passenger
        agent, idd = makeAgent(data)
        Driver['id'] = idd
        Thread(target=agent.run).start()

        self.OEF_AGENTS[idd] = agent
        self.Drivers.append(Driver)

        return Driver

    def update(self, id, data):
        Driver = self.get(id)
        Driver.update(data)
        self.OEF_AGENTS[id].preferences.update(data)
        return Driver

    def delete(self, id):
        Driver = self.get(id)
        self.Drivers.remove(Driver)



DAO = DriverDAO()

@ns.route('/')
class DriverList(Resource):
    '''Shows a list of all Drivers, and lets you POST to add new Drivers'''
    @ns.doc('list_Drivers')
    @ns.marshal_list_with(Driver)
    def get(self):
        '''List all Drivers'''
        return DAO.Drivers

    @ns.doc('create_Driver')
    @ns.expect(Driver)
    @ns.marshal_with(Driver, code=201)
    def post(self):
        '''Create a new Driver'''
        return DAO.create(api.payload), 201


@ns.route('/<string:id>')
@ns.response(404, 'Driver not found')
@ns.param('id', 'The Driver identifier')
class Driver(Resource):
    '''Show a single Driver item and lets you delete them'''
    @ns.doc('get_Driver')
    @ns.marshal_with(Driver)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_Driver')
    @ns.response(204, 'Driver deleted')
    def delete(self, id):
        '''Delete a Driver given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(Driver)
    @ns.marshal_with(Driver)
    def put(self, id):
        '''Update a Driver given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=5001)
