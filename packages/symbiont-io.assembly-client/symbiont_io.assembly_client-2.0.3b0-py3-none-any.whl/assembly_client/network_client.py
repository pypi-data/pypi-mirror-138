import assembly_client.client_utils as client
import os
from pathlib import Path
from typing import Dict, List, Union, Optional

'''
Examples of usage:

    network = NetworkClient()
    network.register_key_alias()
    key_aliases = network.list_key_aliases()

    chat = network.publish('sympl_chat/')
    print('--- chat:', chat)
    network.publish('sympl_auction/')
    network.publish('sympl_hello/')
    contracts = network.list_contracts()

    print('--- key_aliases:', key_aliases)
    print('--- contracts:', contracts)
    print('--- contracts:', network.contracts)

    network.call_contract('chat', 'create_room', {'room_name': 'TestRoom'})
    rooms = network.call_contract('chat', 'get_rooms')
    for room in rooms:
        print(room['name'])

    network.reset()

    print('--- After network reset')

    print('--- key_aliases:', network.list_key_aliases())
    print('--- contracts:', network.list_contracts())

Output:

    --- chat: chat<8>-<3.0.0>
    --- key_aliases: ['KA-2589683863771109']
    --- contracts: [{'ref': {'language': 8, 'name': 'auction', 'version': '1.0.0'}}, {'ref': {'language': 8, 
    'name': 'chat', 'version': '3.0.0'}}, {'ref': {'language': 8, 'name': 'hello', 'version': '1.0.1'}}]
    --- contracts: [{'ref': {'language': 8, 'name': 'auction', 'version': '1.0.0'}}, {'ref': {'language': 8, 
    'name': 'chat', 'version': '3.0.0'}}, {'ref': {'language': 8, 'name': 'hello', 'version': '1.0.1'}}]
    TestRoom
    --- After network reset
    --- key_aliases: []
    --- contracts: []
'''

DEFAULT_PORT = 8888

DEFAULT_NODE = 'default-0'

DEFAULT_HOST = 'localhost'

DEFAULT_CONFIG_PATH = client.get_network_config()

DEFAULT_HOSTNAME = f'http://{DEFAULT_HOST}:{DEFAULT_PORT}'

DEFAULT_CONFIG = {
    "neo_config": {
        "private": "",
        "public" : ""
        },
    "nodes"     : {
        'default-0': {
            "hostname"       : 'http://localhost:8888',
            "admin_cert"     : "",
            "admin_cert_key" : "",
            "client_cert"    : "",
            "client_cert_key": "",
            "vault_token"    : ""
            }
        }
    }

DEFAULT_NODE_CONFIG = {
    DEFAULT_NODE: {
        'hostname'   : DEFAULT_HOSTNAME,
        'certs'      : (
            f'/tmp/client-{DEFAULT_NODE}.crt',
            f'/tmp/client-{DEFAULT_NODE}.key'
            ),
        'admin_certs': (
            f'/tmp/admin-{DEFAULT_NODE}.crt',
            f'/tmp/admin-{DEFAULT_NODE}.key'
            ),
        'ca_cert'    : None,
        'node_fqdn'  : DEFAULT_NODE
        }
    }

DEFAULT_NODE_CLIENTS = {
    DEFAULT_NODE: client.NodeSession(
        hostname=DEFAULT_HOSTNAME,
        certs=(
            f'/tmp/client-{DEFAULT_NODE}.crt',
            f'/tmp/client-{DEFAULT_NODE}.key'
            ),
        admin_certs=(
            f'/tmp/admin-{DEFAULT_NODE}.crt',
            f'/tmp/admin-{DEFAULT_NODE}.key'
            ),
        ca_cert=None,
        node_fqdn=DEFAULT_NODE)
    }


class NetworkClient:
    """
    Provides api access to contract calls on a network
    """
    def __init__(self,
                 config_path: str = None,
                 config: Dict[str, Dict] = None,
                 sync: bool = True):
        self.config_path = config_path
        self.config = config
        self.sync = sync
        self.nodes = []
        self.sessions = []
        self.node_clients = {}
        self.node_session_configs = {}

        self.load_config()

    @property
    def _primary_session(self) -> client.NodeSession:
        return self.sessions[0]

    @property
    def contracts(self) -> List[Dict[str, Union[int, str]]]:
        """Property for convenience to return list of all contracts published on the network

        Returns
        -------
        List[Dict[str, Union[int, str]]]
            list of basic information for each contract
        """
        return self.list_contracts()

    @property
    def key_aliases(self) -> List[str]:
        """Property for convenience to return a list of all key aliases registered on the network

        Returns
        -------
        List[str]
            list of all key aliases registered on the network
        """
        return self.list_key_aliases()

    def load_config(self) -> None:
        """Loads network configuration from provided config or config at config_path
        Assigns values to self.nodes, self.sessions, self.node_clients, self.node_session_configs
        """

        if self.config is not None:
            node_clients, node_session_configs = client.node_clients_from_network_config(self.config)
        elif self.config_path is not None:
            node_clients, node_session_configs = client.node_clients_from_network_config_path(self.config_path)
        else:
            node_clients, node_session_configs = client.node_clients_from_network_config(DEFAULT_CONFIG)

        self.node_clients = node_clients
        self.node_session_configs = node_session_configs
        self.nodes = list(self.node_clients.keys())
        self.sessions = list(self.node_clients.values())

    def reset(self, node_session: client.NodeSession = None) -> None:
        """Resets network, clearing all transaction history and all registered key_aliases

        Parameters
        ----------
        node_session : assembly_client.api.node_client.NodeSession, optional
            Optionally provided node to reset, otherwise self._primary_session
        """

        if node_session is None:
            node_session = self._primary_session

        client.reset(node_session)

    def register_key_alias(self, node_session: client.NodeSession = None) -> str:
        """Creates a new key alias and registers on node_session

        Parameters
        ----------
        node_session : assembly_client.api.node_client.NodeSession, optional
            optionally give a specific node to place the alias on

        Returns
        -------
        str
            new key alias registered on node_session
        """

        if node_session is None:
            node_session = self._primary_session
        return client.register_key_alias(node_session, sync=self.sync)

    def get_key_alias_map(self) -> Dict[str, List[str]]:
        """Provides a mapping between nodes and key aliases for all nodes on the network

        Returns
        -------
        Dict[str, List[str]]
            map from all nodes to a list of the key aliases published on the node
        """

        return {node: client.list_key_aliases(node_session) for node, node_session in self.node_clients.items()}

    def list_key_aliases(self) -> List[str]:
        """Provides a list of all key aliases on any node of the network

        Returns
        -------
        List[str]
            list of all key aliases registered on a node in the network
        """

        return sum([client.list_key_aliases(session) for session in self.sessions], [])

    def publish(self,
                contract_refs: List[client.ContractRef] = None,
                contract_dir: str = './',
                node_session: client.NodeSession = None
                ) -> client.ContractRef:
        """Publishes contract found at contract_dir on node targeted at node_session

        Parameters
        ----------
        contract_refs : List[ContractRef]
            a list of contract refs of the contracts to be published
        contract_dir : str
            directory where contract is stored
        node_session : NodeSession, optional
            node to target

        Returns
        -------
        client.ContractRef
            contract reference for published contract
        """

        if node_session is None:
            node_session = self._primary_session
        os.chdir(Path.home())
        client.publish(node_session, contract_dir, contract_refs, self.sync)
        return client.contract_ref_from_path(contract_dir)

    def get_contract_map(self) -> Dict[str, Dict[str, Union[int, str]]]:
        """Provides a mapping between nodes and contracts for all nodes on the network

        Returns
        -------
        Dict[str, Dict[str, Union[int, str]]]
            map from all nodes to a list of the contracts published on the node
        """

        return {node: [contract['ref'] for contract in client.list_contracts(session)] for node, session in self.node_clients.items()}

    def list_contracts(self):
        """Provides a list of all contracts published on any node of the network

        Returns
        -------
        List[Dict[str, Union[int, str]]]
            list of basic information for each contract
        """
        contract_list = sum([client.list_contracts(session) for session in self.sessions],[])
        return [contract['ref'] for contract in contract_list]

    def call_contract(self,
                      contract_name: str,
                      contract_function: str,
                      key_alias: str,
                      kwargs: dict = {},
                      node_session: client.NodeSession = None):
        """Calls the specified contract function on a node with arguments in kwargs

        Parameters
        ----------
        contract_name : str
            name of contract
        contract_function : str
            name of function being called
        key_alias : str
            key alias used to validate contract call
        kwargs: dict, optional
            keyword arguments to the contract, will be json serialized
        node_session : assembly_client.api.node_client.NodeSession, optional
            node to target

        Returns
        -------
        dict
            returns the result of the call
        """

        if node_session is None:
            node_session = self._primary_session

        contract_ref = client.contract_ref_from_name(contract_name, self.contracts)

        return client.call(node_session, key_alias, contract_ref, contract_function, kwargs)
