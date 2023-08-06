"""
Provides the starting point for a series of tests to be devleoped for NetworkClient
"""
from assembly_client.network_client import NetworkClient, DEFAULT_CONFIG, DEFAULT_CONFIG_PATH, DEFAULT_NODE_CONFIG
import json

# TODO Needs to be built out with unit tests for the network class methods and for tests of network stability

network_config = json.loads(open(DEFAULT_CONFIG_PATH).read())
network = NetworkClient(config=network_config)
#network = NetworkClient(config_path=DEFAULT_CONFIG_PATH)

print('network type:', type(network))

print('network.nodes type:', type(network.nodes), network.nodes)
print('network.sessions type:', type(network.sessions), network.sessions)

node_clients = network.node_clients
print('node_clients type:', type(node_clients), node_clients)

key_alias = network.register_key_alias()
print('key_alias type:', type(key_alias), key_alias)

key_aliases = network.list_key_aliases()
print('key aliases list:', key_aliases)

assert key_aliases == network.key_aliases

key_alias_map = network.get_key_alias_map()
print('key_alias_map type:', type(key_alias_map), key_alias_map)

chat = network.publish(contract_dir='sympl_chat/')
print('published contract chat type:', type(chat), chat)

network.publish(contract_dir='sympl_auction/')
network.publish(contract_dir='sympl_hello/')

contracts = network.list_contracts()
print('contracts type:', type(contracts), contracts)

assert contracts == network.contracts

contract_map = network.get_contract_map()
print('contract_map type:', type(contract_map), contract_map)

chat_fn_output = network.call_contract('chat', 'create_room', key_alias, {'room_name': 'TestRoom'})
print('chat_fn_output type:', type(chat_fn_output))

rooms = network.call_contract('chat', 'get_rooms', key_alias)
for room in rooms:
    print(room['name'])

network.reset()

# print('--- After network reset')
# assert network.key_aliases == []
# assert network.contracts == []
#
# network = NetworkClient(config=DEFAULT_CONFIG)

assert network.node_session_configs == DEFAULT_NODE_CONFIG
print(network.node_session_configs == DEFAULT_NODE_CONFIG)

print(NetworkClient.__doc__)
print(NetworkClient.call_contract.__doc__)