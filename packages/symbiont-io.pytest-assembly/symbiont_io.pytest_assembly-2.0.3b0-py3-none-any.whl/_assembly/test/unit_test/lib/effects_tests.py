import json

from _assembly.lib.effect_types import ModOwner, ADD_OWNER, REMOVE_OWNER, is_valid_key_alias, is_valid_channel_name

alice = "KA-2000000000000006"
channel_name = "TCN-1133F9CJLeo73cgGetfxHGLvo6QHx4WNtPwHBra6iew48cHcQ"

def testModOwnerAdd():
    loads = (lambda x: json.loads(x))
    ntf = ModOwner(ADD_OWNER, channel_name, alice)
    raw = ('{"owner":"KA-2000000000000006", "state_name": "TCN-1133F9CJLeo73cgGetfxHGLvo6QHx4WNtPwHBra6iew48cHcQ", '
           '"tag": "AddOwner"}')
    j = loads(raw)
    ntfj = ModOwner.from_json(j)
    assert ntf.to_json() == ntfj.to_json()


def testModOwnerRemove():
    loads = (lambda x: json.loads(x))
    ntf = ModOwner(REMOVE_OWNER, channel_name, alice)
    raw = ('{"owner": "KA-2000000000000006", "state_name": "TCN-1133F9CJLeo73cgGetfxHGLvo6QHx4WNtPwHBra6iew48cHcQ", '
           '"tag": "RemoveOwner"}')
    j = loads(raw)
    ntfj = ModOwner.from_json(j)
    assert ntf.to_json() == ntfj.to_json()
