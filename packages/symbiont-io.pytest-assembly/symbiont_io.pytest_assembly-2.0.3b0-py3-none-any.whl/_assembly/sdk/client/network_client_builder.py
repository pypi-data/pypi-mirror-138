# this module provides functionality for building a `NetworkClient` instance from a list of node fqdns and a network
# name, done by reading information as needed from the XDG_DATA_DIR

from _assembly.sdk.client.node_client import NodeSession
from _assembly.sdk.client.network_client import NetworkClient


def load_text_file(file):
    with open(file, 'r') as f:
        return f.read()


def node_session_from_xdg(node_fqdn, xdg_data_home, ca_cert=None):
    node_dir = f'{xdg_data_home}/symbiont/node/{node_fqdn}'
    return NodeSession(hostname=f'https://{node_fqdn}',
                       certs=(f'{node_dir}/node-client.crt', f'{node_dir}/node-client.key'),
                       admin_certs=(f'{node_dir}/node-admin.crt', f'{node_dir}/node-admin.key'),
                       ca_cert=ca_cert,
                       node_fqdn=node_fqdn)


def load_neo_creds(network_name, neo_name, xdg_data_home):

    network_dir = f'{xdg_data_home}/symbiont/network/{network_name}'
    neo_crt = load_text_file(f'{network_dir}/{neo_name}.crt').encode('utf-8')
    neo_key = load_text_file(f'{network_dir}/{neo_name}.key').encode('utf-8')

    return {
        'crt': neo_crt,
        'key': neo_key,
    }


def network_from_xdg(network_name, neo_name, node_fqdns, xdg_data_home, contract_path, ca_cert=None):

    sessions = {node_fqdn: node_session_from_xdg(node_fqdn, xdg_data_home, ca_cert) for node_fqdn in node_fqdns}
    neo_creds = load_neo_creds(network_name, neo_name, xdg_data_home)

    return NetworkClient(
        sessions,
        contract_path,
        use_sync_api=False,
        neo_key=neo_creds['key'],
        neo_crt=neo_creds['crt'],
    )


def mock_network(contract_path, port=8888):
    node_name = 'localhost'
    sessions = {node_name: NodeSession(hostname=f'http://localhost:{port}',
                                       certs=(None, None),
                                       admin_certs=(None, None),
                                       ca_cert=None,
                                       node_fqdn=node_name)}
    return NetworkClient(
        sessions,
        contract_path,
        use_sync_api=False,
        neo_key=b'',
        neo_crt=b'',
    )
