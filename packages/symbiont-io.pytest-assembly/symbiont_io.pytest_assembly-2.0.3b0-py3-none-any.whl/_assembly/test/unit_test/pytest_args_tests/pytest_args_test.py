
# a simple test to load a few config files and validate they either raise correct
# exceptions or find the right config values

import os
import pytest

from _assembly.sdk.config.config_file import read_config_file
from _assembly.sdk.pytest_plugin.fixtures.pytest_args import PytestArgs

config_root = os.path.dirname(os.path.realpath(__file__))

configs = [
    ('almost_empty.json', None),
    ('bad_env_name.json', 'invalid configuration file: illegal environment name `defaults`'),
    ('good_config.json', None),
    ('ignored_field_defaults.json', 'invalid configuration file: keys are specified the sdk will ignore:'),
    ('ignored_field_env.json', 'invalid configuration file: keys are specified the sdk will ignore:'),
    ('missing_defaults.json', 'invalid configuration file: missing `defaults`'),
    ('missing_environments.json', 'invalid configuration file: missing `environments`'),
]

@pytest.mark.parametrize('config, error', configs)
def test_config_errors(config, error):
    try:
        read_config_file(f'{config_root}/{config}')
        assert not error
    except Exception as e:
        assert error in str(e)


class FakeRequest():
    def __init__(self):
        self.config = FakeConfig()


class FakeConfig():
    def __init__(self):
        self.answers = {
            '--config': f'{config_root}/good_config.json',
            '--environment': 'dev',
            '--kube-config': 'some_kube_config.json',
        }
    def getoption(self, arg):
        return self.answers.get(arg)


def test_building_pytest_args():

    sdk_args = PytestArgs(FakeRequest())
    assert sdk_args.network_config == None

