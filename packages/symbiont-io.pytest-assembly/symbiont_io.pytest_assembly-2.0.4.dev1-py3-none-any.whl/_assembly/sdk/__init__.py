import os
from pathlib import Path

DEFAULT_LANGUAGE_VERSION = 8
MOCK_NETWORK_CONFIG = os.path.join(Path(__file__).parent, 'mock_network/mock_network_config.json')

def get_network_config(network_name):
    return os.path.join(Path.home(), f'.symbiont/assembly-dev/mock-network/{network_name}/network-config.json')
