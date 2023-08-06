from assembly_client.api.contracts import ContractRef, local_code_from_ref, contract_ref_from_path
from assembly_client.api.node_client import NodeSession, query_node
from assembly_client.api.network_client import NetworkClient
from assembly_client.api.types.error_types import ContractNotFoundError
from assembly_client.api.util.path_util import prep_path, prepare_cert
import json
import os
from pathlib import Path


def get_network_config(network_type='mock', network_name='default'):
    return os.path.join(Path.home(), f'.symbiont/assembly-dev/{network_type}-network/{network_name}/network-config.json')


def sandbox(contract_path='./', port=8888):
    node_name = 'localhost'
    sessions = {node_name: NodeSession(hostname=f'http://localhost:{port}',
                                       certs=(None, None),
                                       admin_certs=(None, None),
                                       ca_cert=None,
                                       node_fqdn=node_name)}
    return NetworkClient(
        sessions,
        contract_path,
        language_version=8,
        use_sync_api=True,
        neo_key=b'',
        neo_crt=b'',
    )


def events(node_session, job_ids=[], start_index=None):
    """
    returns all events available
    :param node_session: node to target
    :param job_ids: job ids to filter the events by
    :return: a list of events in dictionary representation
    """
    max_count = 100
    timeout = 0
    job_ids_param = ",".join(job_ids)
    query_params = {'max_count': max_count, 'timeout_secs': timeout}
    if job_ids_param != '':
        query_params['job_ids'] = job_ids_param
    event_cache = node_session.event_cache
    if start_index is None:
        if len(job_ids) > 0:
            start_index = min([event_cache.get(job_id) for job_id in job_ids])
        else:
            start_index = 1
    all_events = []
    while True:
        data = query_node(node_session, 'GET', '/events/{}'.format(start_index), query_params)

        events = data['events']
        if len(events) > 0:
            for event in events:
                event_cache.event_received(event['job_id'], event['index'])
            all_events.extend(events)
            last_index = data['last_index']
            start_index = last_index + 1
            max_index = data['max_index']
            if last_index == max_index:
                break
        else:
            break
    return all_events


def register_key_alias(node_session, sync=True):
    """
    creates a new key alias on the node
    :param node_session: node to target
    :param sync: if the underlying sync api should be used
    :return: if sync is false, a `Job`, else a string for the created key_alias
    """
    maybe_job = query_node(node_session, 'POST', '/key_aliases?sync={}'.format(str(sync).lower()), {})
    if sync:
        return maybe_job['key_alias']

    return maybe_job


def reset(node_session):
    """
    reset the network, clearing all transaction history and all registered key_aliases
    :param node_session: node to target
    :return: new network-seed for the network
    """
    node_session.event_cache.reset()
    return query_node(node_session, 'POST', '/config/reset', None, role='admin')


def list_contracts(node_session):
    """
    inspection for contracts on a network
    :param node_session: node to target
    :return: information about each contract published
    """
    return query_node(node_session, 'GET', '/contracts', None)


def list_key_aliases(node_session, channel=None):
    """
    lists the key aliases registered and known
    :param node_session: node to target
    :return: list of key aliases known to the node
    """
    return query_node(node_session, 'GET', '/key_aliases?locality=local', None)


def publish(node_session, contract_path='./', contract_refs=None, sync=True):
    """Publishes contracts to a mock-network instance

    Args:
        node_session (NodeSession): node to target
        contract_path (str): path to contract file
        contract_refs (list): list of contract refs to publish
        sync (bool): if the underlying sync api should be used

    Returns:
        None
        if sync is false, a `Job`, else None after contracts finish publishing
    """
    if contract_refs is None:
        contract_refs = [contract_ref_from_path(contract_path)]

    def to_payload(contract_ref):
        """

        Args:
            contract_ref ():

        Returns:

        """
        return {
            'ref': {
                'name': contract_ref.name,
                'version': contract_ref.version_to_use_on_api()
            },
            'code': local_code_from_ref(contract_path, contract_ref)
        }

    data = [to_payload(contract_ref) for contract_ref in contract_refs]

    path = '/contracts?sync={}'.format(str(sync).lower())
    language = contract_refs[0].language
    return query_node(node_session, 'POST', path, data, language_version=language, role='admin')


def call(node_session, key_alias, contract_ref, function, kwargs, sync=True, retries=5, query_tx_index=None):
    """
    calls the specified contract function on a node
    :param node_session: node to target
    :param key_alias: key_alias to invoke as
    :param contract_ref: contract to call
    :param function: function to invoke
    :param kwargs: dictionary of arguments to the contract, will be json serialized
    :param sync: if the underlying sync api should be used
    :param retries: maximum number of retry attempts to make of the underlying call
    :param query_tx_index: a tuple of (tx_index, minor_tx_index) to run clientside as-of a point in time
    :return: if sync is false _or_ the function is purely `@clientside`, returns the result of the call, else
             returns a `Job`
    """
    version_to_use = contract_ref.version_to_use_on_api()

    query_params = {'sync': str(sync).lower()}
    if query_tx_index:
        (tx_index, minor_tx_index) = query_tx_index
        query_params['tx_index'] = tx_index
        query_params['minor_tx_index'] = minor_tx_index

    query_params_str = '&'.join(['{}={}'.format(k, r) for k, r in query_params.items()])

    path = '/contracts/{}/{}/{}?{}'.format(contract_ref.name, version_to_use, function, query_params_str)

    result = query_node(node_session, 'POST', path, kwargs, key_alias=key_alias,
                        language_version=contract_ref.language, retries=retries)

    return result['result']


def contract_ref_from_name(contract_name, contract_list):
    name = None
    version = None
    language = None
    for ref in contract_list:
        if ref['name'] == contract_name:
            name, version, language = ref['name'], ref['version'], ref['language']
            break
    print(f'name: {name} --- version: {version} --- language: {language}')
    try:
        return ContractRef(name, version, language)
    except:
        raise ContractNotFoundError


def node_clients_from_network_config(network_config):
    node_session_configs = {}
    node_clients = {}
    node_configs = network_config.get('nodes') or network_config
    for node_name, node_config in node_configs.items():
        node_clients[node_name] = NodeSession(
            hostname=node_config['hostname'],
            certs=(
                prepare_cert(node_config.get('client_cert'), 'client', 'crt', node_name),
                prepare_cert(node_config.get('client_cert_key'), 'client', 'key', node_name)
            ),
            admin_certs=(
                prepare_cert(node_config.get('admin_cert'), 'admin', 'crt', node_name),
                prepare_cert(node_config.get('admin_cert_key'), 'admin', 'key', node_name),
            ),
            ca_cert=prepare_cert(node_config.get('ca_cert'), 'ca', 'crt', node_name),
            node_fqdn=node_name
        )
        node_session_configs[node_name] = {
            'hostname': node_clients[node_name].hostname,
            'certs': node_clients[node_name].certs,
            'admin_certs': node_clients[node_name].admin_certs,
            'ca_cert': node_clients[node_name].ca_cert,
            'node_fqdn': node_clients[node_name].node_fqdn
        }

    return node_clients, node_session_configs


def node_clients_from_network_config_path(network_config_path):
    with open(prep_path(network_config_path)) as f:
        network_config = json.load(f)
    return node_clients_from_network_config(network_config)

