import re


class ContractRef():
    """class used to reference contracts in tests"""

    @staticmethod
    def parse_version(v):
        match = re.fullmatch(r"(\d+-)?(\d+\.\d+\.\d+)", v)
        if not match:
            raise RuntimeError('Cannot parse the contract version expected something like 1.0.1 or 2-1.0.1')
        r = match.groups()
        if r[0] is None:
            return 1, r[1]
        else:
            return int(r[0].strip('-')), r[1]

    def version_to_use_on_api(self):
        return "{}-{}".format(self.language, self.version)

    def __init__(self, name, version, language):
        assert isinstance(language, int)
        self.name = name
        self.version = version
        self.language = language

    def __eq__(self, other):
        if isinstance(other, ContractRef):
            return self.name == other.name and self.version == other.version and self.language == other.language
        else:
            return False

    def __repr__(self):
        if self.language == 1:
            return '{}<{}>'.format(self.name, self.version)
        else:
            return '{}<{}>-<{}>'.format(self.name, self.language, self.version)

    def to_json(self):
        return {'name': self.name, 'version': self.version, 'language': self.language}

    @staticmethod
    def from_repr(repr):
        match = re.fullmatch(r"([\w_]+)<(\d+)>-<(\d+\.\d+\.\d+)>", repr)
        if not match:
            match = re.fullmatch(r"([\w_]+)<(\d+\.\d+\.\d+)>", repr)
            if not match:
                raise RuntimeError('could not build ContractRef from {}'.format(repr))
            name, version = match.groups()
            return ContractRef(name, version, 1)
        name, language, version = match.groups()
        return ContractRef(name, version, int(language))

    @staticmethod
    def from_json(obj):
        if 'name' not in obj or 'version' not in obj:
            raise RuntimeError('could not build ContractRef from {}'.format(obj))
        # this is a horrid hack which we will once pay dearly for but we do not have to change the interface of anything
        # client facing
        # if there is `language` explicitly provided in `obj` we will use it:
        if 'language' in obj:
            language = int(obj['language'])
            _, version = ContractRef.parse_version(obj['version'])
        else:
            # otherwise we will try to infer it from the version field
            language, version = ContractRef.parse_version(obj['version'])
        return ContractRef(obj['name'], version, language)
