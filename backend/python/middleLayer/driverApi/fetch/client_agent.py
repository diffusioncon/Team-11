import base64
import os
import hashlib
import binascii
from typing import List
import base58
import oef
from oef.agents import OEFAgent
from oef.proxy import  OEFProxy, PROPOSE_TYPES
from oef.query import Eq, Range, Constraint, Query, AttributeSchema, Distance
from oef.schema import DataModel, Description , Location
from oef.messages import CFP_TYPES
import requests
import random
from .agent_dataModel import TIME_AGENT

from multiprocessing import Process
import json
import datetime

import time
import uuid
import asyncio

from .contractUtils import generateEntity, deployContract, setEscrew, releaseEscrew

# here we import over vector matching utils
from .vectorUtils import check_match



class ClientAgent(OEFAgent):
    """
    The class that defines the behaviour of the echo client agent.
    """
    def __init__(self, public_key: str, oef_addr: str, preferences: dict, oef_port: int = 3333):
        super().__init__(public_key, oef_addr, oef_port, loop=asyncio.new_event_loop())
        self.cost = 0
        self.pending_cfp = 0
        self.received_proposals = []
        self.received_declines = 0
        self.preferences = preferences
        self.driverVectors = {}

        self.APIContractId = None
        # here we create an entity on our local ledger;
        self.entity = generateEntity()
        # here we create our contract;
        self.contract = deployContract(self.entity)

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        #print("Received message: origin={}, dialogue_id={}, content={}".format(origin, dialogue_id, content))
        data = json.loads(content.decode())
        print ("message...")
        print(data)
        Process(target=self.checkStatusOfContract,).start()



    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: No agent found. Stopping...".format(self.public_key))
            self.stop()
            return

        print("[{0}]: Agent found: {1}".format(self.public_key, agents))

        for agent in agents:
            print("HEREEEEE!!!", self.pending_cfp)
            print("[{0}]: Sending to agent {1}".format(self.public_key, agent))
            self.pending_cfp += 1
            self.send_cfp(1, 0, agent, 0, None)

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, answer with an Accept."""
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin, proposals))
        print("PROPOSAL", proposals)
        for i,p in enumerate(proposals):

            self.received_proposals.append({"agent" : origin,
                                            "proposal":p.values})
            if p.values["data"] is True:
                # here we create a matched between the 2 preferences.
                # we would submit as a synergystic contracts, however we are
                # unable to query the deployed contacts
                # please see synergystic contracts for the ETCH implementation
                self.driverVectors[origin] = (check_match(json.loads(p.values["driverVect"]),
                                                          self.preferences),
                                            json.loads(p.values["driverVect"]))
        received_cfp = len(self.received_proposals) + self.received_declines
        # once everyone has responded, let's accept them.
        if received_cfp == self.pending_cfp:
            rankings = sorted(self.driverVectors,
                              key=lambda x:self.driverVectors[x][0])
     #       if len(rankings) == 0:
     #           return
            if len(rankings) >= 1:
                print("Best Ranked agent is {}".format(rankings[0]))
                self.send_accept(msg_id, dialogue_id,
                                 rankings[0],
                                 # self.received_proposals[0]['agent'],
                                 msg_id + 1)
                print ("Accept", self.driverVectors[rankings[0]])

#                 print(json.loads(rankings[1]))
                # we need to call the Contract api to generate the contract,
                data = {
                        "status": "funds_in_escrow",
                         "passengerId": self.preferences["id"],
                          "driverId": self.driverVectors[rankings[0]][1]["id"],
                          "startLocationLat": self.preferences["currentLocationLat"],
                          "startLocationLong": self.preferences["currentLocationLong"],
                          "destinationLocationLat": self.preferences["endLocationLat"],
                          "destinationLocationLong": self.preferences["endLocationLong"],
                         }

                headers = {
                                "Content-Type": "application/json" ,
                                "Accept": 'application/json'
                            }
                res = requests.post("http://contract_api:5000/Contracts/",
                                        data=json.dumps(data), headers=headers)
                # we need to set the escre with a vale from the api
                print(res.content)
                self.toKey = self.driverVectors[rankings[0]][1]["driver_pub_key"]
                setEscrew(self.entity, self.contract, json.loads(res.content)['cost'])
                self.APIContractId = json.loads(res.content)['id']
            else :
                print("They don't have data")
                self.pending_cfp -= 1
                self.received_declines = 0
                self.received_proposals = []
                self.search_services(0, self.QUERY)

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int) :
        print("Received a decline!")
        self.received_declines += 1



    def checkStatusOfContract(self):
        while True:
            time.sleep(1)
            if self.APIContractId is None:
                pass
            else:
                res = requests.get("http://contract_api:5000/Contracts/{}".format(self.APIContractId))
                res = json.loads(res.content)
                if res["status"] == "passengerDropped":
                    releaseEscrew(self.entity, self.contract, self.toKey)
                    data = {
                   "status": "completed",
                     }

                    headers = {
                        "Content-Type": "application/json" ,
                        "Accept": 'application/json'
                    }
                    res = requests.put("http://contract_api:5000/Contracts/{}".format(self.APIContractId),
                                       data=json.dumps(data),
                                       headers=headers)
                    break



def makeAgent(preferences):
    OEF_Address = os.environ.get('OEF_ADDRESS')
    OEF_Port = os.environ.get('OEF_PORT')
    Agent_id =  "Passenger{}".format(str(random.randint(0,9999999999999))).replace("0", "")
    print (Agent_id, OEF_Address, OEF_Port)
    client_agent = ClientAgent(str(Agent_id),
                               oef_addr=OEF_Address,
                               oef_port=OEF_Port, preferences=preferences)

    # connect it to the OEF Node
    client_agent.connect()

    # query OEF for DataService providers
    echo_query = Query([Constraint("timezone", Eq(2))],TIME_AGENT())
    client_agent.QUERY = echo_query
    client_agent.search_services(0, echo_query)
    return client_agent, Agent_id
    # client_agent.run()


if __name__ == '__main__':

    OEF_Address = os.environ.get('OEF_ADDRESS')
    OEF_Port = os.environ.get('OEF_PORT')
    # oef.economicagents.com, 3333


    # define an OEF Agent
    Agent_id =  base58.b58encode("Passenger{}".format(str(random.randint(0,9999999999999))).replace("0", ""))
    print (Agent_id)
    client_agent = ClientAgent(Agent_id,
                               oef_addr=OEF_Address,
                               oef_port=OEF_Port)

    # connect it to the OEF Node
    client_agent.connect()

    # query OEF for DataService providers
    echo_query = Query([Constraint("timezone", Eq(2))],TIME_AGENT())


    client_agent.search_services(0, echo_query)
    client_agent.run()
