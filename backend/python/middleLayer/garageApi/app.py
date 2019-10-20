from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
# https://flask-restplus.readthedocs.io/en/stable/example.html
from flask_cors import CORS
app = Flask(__name__, )
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='GarageMVC API',
    description='A simple GarageMVC API',
)
from flask_cors import CORS
CORS(app)


from fetch.demo_agent import makeAgent

ns = api.namespace('Garages', description='Garage operations')

Garage = api.model('Garage', {
    'id': fields.String(readOnly=True,
                         description='The Garage unique identifier'),

    'name': fields.String(required=True,
                          description='The Garages Name'),

    'currentLocationLat': fields.Float(required=True,
                          description='The Garages current Latitude'),

    'currentLocationLong': fields.Float(required=True,
                          description='The Garage current Longitude'),

    'maxAllowed': fields.Float(required=True,
                          description='The Garages maximum allowed cars'), #

    'currentCapacity': fields.Float(required=True,
                          description='The Garages current capacity'),



    'pricePreference': fields.Float(required=True,
                          description='The Garage current Longitude'),

})


from threading import Thread


class GarageDAO(object):

    def __init__(self):
        self.counter = 0
        self.OEF_AGENTS = {}
        self.Garages = []

    def get(self, id):
        for Garage in self.Garages:
            if Garage['id'] == id:
                return Garage
        api.abort(404, "Garage {} doesn't exist".format(id))

    def create(self, data):
        Garage = data
        Garage['id'] = self.counter = self.counter + 1
        # here we crete the OEF registration and save as attibute on the driver
        self.Garages.append(Garage)
        agent, idd = makeAgent(data)
        Garage["id"] = idd
        Thread(target=agent.run).start()
        self.OEF_AGENTS[idd] = agent

        return Garage

    def update(self, id, data):
        Garage = self.get(id)
        Garage.update(data)
        self.OEF_AGENTS[id].preferences.update(data)
        return Garage

    def delete(self, id):
        Garage = self.get(id)
        self.Garages.remove(Garage)

DAO = GarageDAO()
@ns.route('/')
class GarageList(Resource):
    '''Shows a list of all Garages, and lets you POST to add new Garages'''
    @ns.doc('list_Garages')
    @ns.marshal_list_with(Garage)
    def get(self):
        '''List all Garages'''
        return DAO.Garages

    @ns.doc('create_Garage')
    @ns.expect(Garage)
    @ns.marshal_with(Garage, code=201)
    def post(self):
        '''Create a new Garage'''
        return DAO.create(api.payload), 201


@ns.route('/<string:id>')
@ns.response(404, 'Garage not found')
@ns.param('id', 'The Garage identifier')
class Garage(Resource):
    '''Show a single Garage item and lets you delete them'''
    @ns.doc('get_Garage')
    @ns.marshal_with(Garage)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_Garage')
    @ns.response(204, 'Garage deleted')
    def delete(self, id):
        '''Delete a Garage given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(Garage)
    @ns.marshal_with(Garage)
    def put(self, id):
        '''Update a Garage given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True,
            port=5000,
            host="0.0.0.0")
