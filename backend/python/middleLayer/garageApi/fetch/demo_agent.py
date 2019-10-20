import oef
from oef.agents import OEFAgent

import os, sys
import json
import time

import base58
from oef.proxy import  OEFProxy, PROPOSE_TYPES
from oef.query import Eq, Range, Constraint, Query, AttributeSchema, Distance
from oef.schema import DataModel, Description , Location
from oef.messages import CFP_TYPES

from .agent_dataModel import TIME_AGENT

import random
import json
import datetime
import copy
import random
import asyncio

import uuid
import time

from .contractUtils import generateEntity


class Demo_Agent(OEFAgent):

    def __init__(self, public_key: str, oef_addr: str, preferences: dict, oef_port: int = 3333,
                ):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())
        self.preferences = preferences
        self.scheme = {}
        self.scheme['timezone'] = None
        self.scheme['id'] = None

        # here we create our entity
        self.entity = generateEntity()
        self.preferences["driver_pub_key"] = self.entity.public_key

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))

        #data = self.get_latest(0)
        if self.preferences["currentCapacity"] < self.preferences['maxAllowed']:
            proposal = Description({"data" : True, "driverVect": json.dumps(self.preferences)})
        else:
            proposal = Description({"data": False})
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Received accept from {1}.".format(self.public_key, origin))

        command = {}
        msg = json.dumps(command)
        self.send_message(0,dialogue_id, origin, msg.encode())
        self.preferences["currentCapacity"] += 1


    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        print("declined")


    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode())
        print ("message received: "  + json.dumps(data))


def makeAgent(preferences):
    idd = str(base58.b58encode("Driver{}".format(preferences["id"]))).replace("'", str(random.randint(0,9999999999999999999999999999)))
    print(idd)

    OEF_Address = os.environ.get('OEF_ADDRESS')
    OEF_Port = os.environ.get('OEF_PORT')
    print("HERE!", OEF_Address, OEF_Port) #)
    server_agent = Demo_Agent(idd,
                              oef_addr=OEF_Address,
                              oef_port=OEF_Port,
                              preferences=preferences) # oef.economicagents.com
    server_agent.scheme['timezone'] = 2
    server_agent.scheme['id'] = str(uuid.uuid4())
    server_agent.connect()
    # register a service on the OEF
    server_agent.description = Description(server_agent.scheme, TIME_AGENT())
    server_agent.register_service(0,server_agent.description)
    # server_agent.run()
    return server_agent, idd

if __name__ == '__main__':
    # create agent and connect it to OEF
    server_agent = Demo_Agent("Time{}".format(str(random.randint(0,9999999999999999999999999999))),
                              oef_addr="oef.economicagents.com",
                              oef_port=3333) # oef.economicagents.com
    server_agent.scheme['timezone'] = 2
    server_agent.scheme['id'] = str(uuid.uuid4())
    server_agent.connect()
    # register a service on the OEF
    server_agent.description = Description(server_agent.scheme, TIME_AGENT())
    server_agent.register_service(0,server_agent.description)
    server_agent.run()


