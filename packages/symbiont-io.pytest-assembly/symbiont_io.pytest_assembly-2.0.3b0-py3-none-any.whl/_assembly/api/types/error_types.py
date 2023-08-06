import logging
from _assembly.lib.error_types import BaseContractError, VmError

logger = logging.getLogger(__name__)


class ContractError(BaseContractError):
    """execution time error, type thrown by user code"""
    def __init__(self, message, inner=None):
        super().__init__(message, inner=inner)


class UnrecoverableVmError(ContractError):
    """errors where we cannot recover"""
    def log(self):
        logger.error(str(self))


class ContractImplementationError(ContractError):
    """for any errors determined to be independent of inputs, static bugs"""


class ContractNotFoundError(VmError):
    """for when the contract is not found in the database"""
    def __init__(self, contract_ref):
        super().__init__(404, type(self).__name__, "no such contract: '{}'".format(contract_ref))


class ContractFunctionNotFoundError(VmError):
    """for when the specified function does not exist on the contract"""
    def __init__(self, contract_ref, function_name):
        super().__init__(404,
                         type(self).__name__, "no such contract function: '{}.{}'".format(contract_ref, function_name))


class KeyAliasNotFoundError(VmError):
    def __init__(self, key_alias):
        super().__init__(404, type(self).__name__, "no such key alias: '{}'".format(key_alias))


class PublishContractsError(VmError):
    def __init__(self, contract_ref_error_pairs):
        super().__init__(400,
                         type(self).__name__,
                         "some or all contracts are invalid and failed to publish",
                         inner=[{'ref': contract_ref.to_json(), 'error': str(error)}
                                for (contract_ref, error) in contract_ref_error_pairs])
