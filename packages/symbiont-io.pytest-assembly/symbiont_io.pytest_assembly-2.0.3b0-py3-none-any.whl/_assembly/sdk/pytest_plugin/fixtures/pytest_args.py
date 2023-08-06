import os

from _assembly.sdk.config.config_file import read_config_file, get_config_value
from _assembly.lib.util.contracts import CONTRACT_PATH


class PytestArgs():

    def __init__(self, request):
        self.request = request

    def __getattr__(self, item):

        import pdb
#        pdb.set_trace()
        # first priority is provided cli arguments
        hyphenated = item.replace('_', '-')
        cli_formatted = f'--{hyphenated}'
        value = self.request.config.getoption(cli_formatted)

        # this is a special hack for backwards compatibility! remove in the 3.2 release!
        # if we don't find the `contract_path` arg in the cli or the config, look for it as an environment variable
        if not value and item == 'contract_path':
            value = os.environ.get(CONTRACT_PATH)

        # if not found in either, return `None`
        return value

    def __getitem__(self, item):
        return self.__getattr__(item)
