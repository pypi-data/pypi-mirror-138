from _assembly.lib.contract_ref import ContractRef
from _assembly.lib.util.contracts import local_code_from_ref

# from _assembly.lang_7.validator.utils import extract_contract_imports as extract_contract_imports_7


# def contract_refs_with_deps(contract_path, contract_refs):
#     """
#     do a depth first search of the contract imports to identify all dependencies of a list of contracts
#     """

#     # python is adversarial to fp, so even a pure recursive traversal is best done without...
#     all_contract_refs = []

#     def kernel(contract_ref):

#         if contract_ref in all_contract_refs:
#             return

#         if contract_ref.language == 5:
#             extract_contract_imports = extract_contract_imports_5
#         elif contract_ref.language == 6:
#             extract_contract_imports = extract_contract_imports_6
#         elif contract_ref.language == 7:
#             extract_contract_imports = extract_contract_imports_7
#         elif contract_ref.language == 8:
#             # We are not going to make changes to validators
#             extract_contract_imports = extract_contract_imports_7
#         else:
#             raise Exception('publishing with deps only supported for lang >= 5')

#         raw_deps = extract_contract_imports(local_code_from_ref(contract_path, contract_ref))
#         deps = [ContractRef(raw_dep.name, raw_dep.version, int(raw_dep.language)) for raw_dep in raw_deps]

#         # we generate the tree in-order, so be sure to add the children first by recursing, building the tree up
#         # from the leaves
#         for dep in deps:
#             kernel(dep)
#         all_contract_refs.extend([contract_ref])

#     for contract_ref in contract_refs:
#         kernel(contract_ref)

#     return all_contract_refs
