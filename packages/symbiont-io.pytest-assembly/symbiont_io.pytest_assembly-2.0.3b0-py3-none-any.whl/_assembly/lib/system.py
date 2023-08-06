from abc import abstractmethod, ABC
from contextlib import contextmanager
from typing import Optional
from _assembly.lib.error_types import LanguageVersionNotAllowed
from _assembly.lib.metadata_inspector import MetadataInspector


from _assembly.api.types.error_types import ContractError as ContractError

error_ctors = {8: ContractError, 9: ContractError}

