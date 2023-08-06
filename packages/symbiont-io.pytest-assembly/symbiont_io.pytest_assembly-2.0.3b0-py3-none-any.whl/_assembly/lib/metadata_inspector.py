import inspect

MAX_MINOR_TX_INDEX = 1000000
SYMBIONT_FUNCTION_TYPE = '_symbiont_function_type'


class MetadataInspector():
    """this class is an implementation for a metadata retrieval api"""

    def __init__(self, module_loader):
        self.module_loader = module_loader

    def list_contracts(self, tx_index):
        """
        :param tx_index: look for contracts up to this tx_index, inclusive
        :return: a json-ready list of strings for the available contracts
        """
        refs = self.module_loader.list_contracts(tx_index, MAX_MINOR_TX_INDEX)
        return [{'ref': ref.to_json()} for ref in refs]

    def contract_info(self, contract_ref, tx_index):
        """
        :param tx_index: look for contracts up to this tx_index, inclusive
        :param contract_ref: ref for a contract to produce information about
        :return: json-ready structure including contract function signatures and code
        """
        code = self.module_loader.get_code(str(contract_ref), tx_index, MAX_MINOR_TX_INDEX)
        module = self.module_loader.get_module(contract_ref, tx_index, MAX_MINOR_TX_INDEX)

        members = inspect.getmembers(module, inspect.isfunction)
        symbiont_functions = [m for m in members if SYMBIONT_FUNCTION_TYPE in m[1].__dict__]
        formatted_functions = [self._format_function(f) for f in symbiont_functions]

        data = {
            'ref': contract_ref.to_json(),
            'functions': formatted_functions,
            'code': code
        }

        return data

    def _format_function(self, func):
        """
        :param func: an annotated contract function
        :return: json-ready signature information
        """
        return {
            'name': func[0],
            'symbiont_function_types': [str(t) for t in func[1].__dict__[SYMBIONT_FUNCTION_TYPE]],
            'signature': str(inspect.signature(func[1]))
        }
