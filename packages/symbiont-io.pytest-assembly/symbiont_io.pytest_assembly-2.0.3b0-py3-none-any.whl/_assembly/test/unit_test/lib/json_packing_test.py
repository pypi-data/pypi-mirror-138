import pytest

from _assembly.lib.contract_ref import ContractRef
from _assembly.lib.util import json


# Make sure this tries all supported Python types
# Mark failures so we know it isn't supported.


class SampleClass:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


python_types = [
    True, False, None, -10, 0, 10, -3.14, 0.0, 3.14,
    pytest.param(3 + 4j, marks=pytest.mark.xfail), "hello world", "'quotes'",
    "<français>Comment ça va? Très bien ?</français>",
    pytest.param((1, ), marks=pytest.mark.xfail),
    pytest.param((1, 2, 3), marks=pytest.mark.xfail), [1, 2, 3], [],
    ContractRef('foo', '1.0.0', 8),
    pytest.param(SampleClass(1, 2, 3), marks=pytest.mark.xfail)
]


@pytest.mark.parametrize("data", python_types)
def test_json_packing(data):
    assert data == json.loads(json.dumps(data))


def test_unserializable():
    class A:
        pass

    with pytest.raises(ValueError):
        json.dumps({"id": A})

    with pytest.raises(ValueError):
        json.dumps({"id": id})


@pytest.mark.parametrize(
    'i, o', [('{"5": {"2": 0, "1": 0}, "3": {"4": 0, "3": 0}}', '{"3": {"3": 0, "4": 0}, "5": {"1": 0, "2": 0}}')])
def test_dict_sorting(i, o):
    assert json.dumps(json.loads(i)) == o
