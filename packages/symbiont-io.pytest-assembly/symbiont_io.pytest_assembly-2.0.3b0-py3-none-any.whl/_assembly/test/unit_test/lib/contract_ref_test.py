import pytest

from _assembly.lib.contract_ref import ContractRef


def test_round_trip():
    cr = ContractRef("name", "1.0.0", 1)
    assert cr.__repr__() == "name<1.0.0>"
    json = cr.to_json()
    assert json == {'name': "name", 'version': "1.0.0", 'language': 1}
    assert ContractRef.from_json(json) == cr

    cr = ContractRef("name", "1.0.0", 8)
    assert cr.__repr__() == "name<8>-<1.0.0>"
    json = cr.to_json()
    assert json == {'name': "name", 'version': "1.0.0", 'language': 8}
    assert ContractRef.from_json(json) == cr

    cr = ContractRef("name", "1.0.0", 2)
    assert cr.__repr__() == "name<2>-<1.0.0>"
    json = cr.to_json()
    assert json == {'name': "name", 'version': "1.0.0", 'language': 2}
    assert ContractRef.from_json(json) == cr

    cr = ContractRef("name", "1.0.0", 2)
    json = {'name': "name", 'version': "2-1.0.0"}
    assert ContractRef.from_json(json) == cr
    json2 = cr.to_json()
    assert json2 == {'name': "name", 'version': "1.0.0", 'language': 2}

    cr = ContractRef("name", "1.0.0", 10)
    json = {'name': "name", 'version': "10-1.0.0"}
    assert ContractRef.from_json(json) == cr
    json2 = cr.to_json()
    assert json2 == {'name': "name", 'version': "1.0.0", 'language': 10}

    cr = ContractRef("name", "12.123.1234", 1)
    json = {'name': "name", 'version': "1-12.123.1234"}
    assert ContractRef.from_json(json) == cr
    json2 = cr.to_json()
    assert json2 == {'name': "name", 'version': "12.123.1234", 'language': 1}

    json = {'name': 'name', 'version': '1-1-1.0.0'}
    with pytest.raises(RuntimeError, match='Cannot parse the contract version'):
        ContractRef.from_json(json)
