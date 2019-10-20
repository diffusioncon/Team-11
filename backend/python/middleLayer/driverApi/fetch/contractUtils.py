from typing import List
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity, Address


HOST = "ledger_node"


CONTRACT_TEXT = """
@init
function setup(owner : Address)
  var rentalStarting = State<UInt64>("startTimeStamp");

  var price = State<UInt64>("pricePerMin");
  var owner_balance = State<UInt64>(owner);
  owner_balance.set(1000000u64);
  var depositeAmount = State<UInt64>("deposite");
  depositeAmount.set(0u64);
endfunction
@action
function transfer(from: Address, to: Address, amount: UInt64)
  // define the accounts
  var from_account = State<UInt64>(from);
  var to_account = State<UInt64>(to); // if new sets to 0u
  // Check if the sender has enough balance to proceed
  if (from_account.get() >= amount)
    // update the account balances
    from_account.set(from_account.get() - amount);
    to_account.set(to_account.get(0u64) + amount);
  endif
endfunction
@action
function setEscrew(from: Address, amount: UInt64, inputRentalStarting: UInt64, inputPrice: UInt64)
  // define the accounts
  var price = State<UInt64>("pricePerMin");
  price.set(inputPrice);

  var rentalStarting = State<UInt64>("startTimeStamp");
  rentalStarting.set(inputRentalStarting);
  var from_account = State<UInt64>(from);
  var escrew_holdings = State<UInt64>("escrew");
  // Check if the sender has enough balance to proceed
  if (from_account.get() >= amount)
    // update the account balances
    from_account.set(from_account.get() - amount);
    escrew_holdings.set(escrew_holdings.get(0u64) + amount);
  endif
endfunction
@action
function releaseEscrew(to: Address, rentalEnds: UInt64)
  //another parameter
  // define the accounts
  var to_account = State<UInt64>(to);
  var escrew_holdings = State<UInt64>("escrew");
  // Check if the sender has enough balance to proceed
  var amount: UInt64;
  var finAmt: UInt64;
  amount = escrew_holdings.get();

  var price = State<UInt64>("pricePerMin");
  var rentalStarting = State<UInt64>("startTimeStamp");
  var totalMinutes = rentalEnds-rentalStarting.get();
  //finAmt = to_account.get(0u64) + amount;
  to_account.set(finAmt);



  escrew_holdings.set(escrew_holdings.get(0u64) - amount);
endfunction
@query


function balance(address: Address) : UInt64
  var account = State<UInt64>(address);
  return account.get(0u64);
endfunction
"""


SYNERGYSTIC = """
@problem
function createProblem(data : Array<StructuredData>) : Array<Int32>
  var myArray = Array<Int32>(data.count());
  for (i in 0:data.count() - 1)
    myArray[i] = data[i].getInt32("value");
  endfor
  return myArray;
endfunction
@objective
function evaluateWork(problem :  Array<Int32>, solution : Int32 ) : Int64
  return toInt64(0);
endfunction
@work
function doWork(problem : Array<Int32>, nonce : UInt256) :  Int32
  var result = 0;
  for (i in 0:4)
    result += (abs(problem[i]) - abs(problem[i+5]));
  endfor
  return result;
endfunction
@clear
function applyWork(problem : Int32, solution : Int32)
  var result = State<Int32>("solution");
  result.set(solution);
endfunction
"""



def print_address_balances(api: LedgerApi,
                           contract: Contract,
                           addresses: List[Address]):
    for idx, address in enumerate(addresses):
        continue
        print('Address{}: {:<6d} bFET {:<10d} TOK'.format(idx,
                                                          api.tokens.balance(address),
                                                          contract.query(api,
                                                                         'balance',
                                                                         address=Address(address))))


def submitSynergy(entity, values):
    api = LedgerApi(HOST, 8100)
    synergy_contract = SynergeticContract(SYNERGYSTIC)
    print(synergy_contract.digest)

    api.sync(api.contracts.create(entity, synergy_contract, 4096))

    api.sync([api.synergetic.submit_data(entity, synergy_contract.digest, value=value) for value in values])

    return synergy_contract


def generateEntity():
    print('Creating private key...')

    # create our first private key pair
    entity1 = Entity()

    # save the private key to disk
#    with open('private.key', 'w') as private_key_file:
#         entity1.dump(private_key_file)

    print('Creating private key...complete')

    # build the ledger API
    api = LedgerApi(HOST, 8100)

    print('Creating initial balance...')

    # create wealth so that we have the funds to be able to create contracts on the network
    api.sync(api.tokens.wealth(entity1, 100000))

    print('Creating initial balance...complete')
    return entity1

def deployContract(entity):
    api = LedgerApi(HOST, 8100)

    # create the smart contract
    contract = Contract(CONTRACT_TEXT)

    print('Deploying contract...')

    # deploy the contract to the network
    api.sync(api.contracts.create(entity, contract, 6000))

    print('Deploying contract...complete')

    return contract

def setEscrew(entity, contract, amount):
    api = LedgerApi(HOST, 8100)
    fet_tx_fee = 40
    print('-- BEFORE --')
    print_address_balances(api, contract, [entity])
    api.sync(contract.action(api, 'setEscrew', fet_tx_fee,
                              [entity], Address(entity),
                              amount))
    print('-- AFTER --')
    print_address_balances(api, contract, [entity])


def releaseEscrew(entity1, contract, entity2):
    api = LedgerApi(HOST, 8100)
    fet_tx_fee = 40
    api.sync(contract.action(api, 'releaseEscrew', fet_tx_fee,
                             [entity1], entity2,
                             ))
    print("Escrew Released.")
    # print_address_balances(api, contract,[entity1, entity2])

if __name__ == "__main__":
    ent = generateEntity()
    deployContract(ent)

