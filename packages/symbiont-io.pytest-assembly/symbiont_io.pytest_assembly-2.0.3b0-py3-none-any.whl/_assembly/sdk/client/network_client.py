import random

import beeline
from _assembly.sdk import DEFAULT_LANGUAGE_VERSION
from _assembly.sdk.client import node_api_client, network_syncer
from _assembly.sdk.client.job_management import Job, ContractErrorInJob
from _assembly.lib.contract_ref import ContractRef
from typing import Optional


class NetworkClient():
    """
    provides api access to contract calls on a network
    """
    def __init__(self,
                 node_sessions,
                 contract_path,
                 language_version,
                 rng_seed=None,
                 use_sync_api=False,
                 neo_key=None,
                 neo_crt=None,
                 skip_consistency_check=False):
        """
        create a new client at the network level, automatically handling job asynchrony
        :param node_sessions: a dictionary of node fqdn to NodeSession enumerating available nodes
        :param rng_seed: override the seed used to generate randomness needed to make api calls
        :param use_sync_api: whether or not to use the underlying sync api
        """
        self.node_sessions = node_sessions
        self.contract_path = contract_path
        self.use_sync_api = use_sync_api
        self.query_tx_index = None
        self.neo_key = neo_key
        self.neo_crt = neo_crt
        self.language_version = language_version

        if rng_seed:
            random.seed(rng_seed)
        # there are some cases we can't safely run this, such as when we delete the network inside the test
        self.skip_cleanup_consistency_check = skip_consistency_check
        # when we register aliases, we need to remember what node we placed them on
        self.alias_locations = {}

    def _random_node(self):
        node_idx = random.randint(0, len(self.node_sessions.keys()) - 1)
        node = list(self.node_sessions.keys())[node_idx]
        return node

    def list_nodes(self):
        """
        list the nodes known by the client
        """
        return list(self.node_sessions.keys())

    def _fixed_node_0(self):
        return self._fixed_node(0)

    def _fixed_node_1(self):
        return self._fixed_node(1)

    def _fixed_node_2(self):
        return self._fixed_node(2)

    def _fixed_node_3(self):
        return self._fixed_node(3)

    def _fixed_node(self, node_idx):
        return list(self.node_sessions.keys())[node_idx]

    def _random_session(self):
        return self.node_sessions[self._random_node()]

    def _sync_sessions_for_sync_api(self, origin_session):
        """
        when using the sync api, we still need to sync between nodes in the network, so this
        helper abstracts over the details of doing that
        :param origin_session: node we want to ensure everyone is in sync with
        :return: None
        """
        tx_index = node_api_client.statusz(origin_session)['last_tx_index']
        self.sync_sessions(origin_session, tx_index, self.node_sessions.values())

    def record_key_alias(self, key_alias, node):
        """
        records an existing key alias in the network client
        :param key_alias: key-alias to record
        :param node: node the key-alias is associated with
        """
        self.alias_locations[key_alias] = node

    @beeline.traced(name="network.register_key_alias")
    def register_key_alias(self, node=None):
        """
        registers a key alias
        :param node: optionally give a specific node to place the alias on
        :return: new key alias as a `str`
        """
        if node is None:
            node = self._random_node()
        return self.register_key_alias_on_node(node)

    @beeline.traced(name="network.register_key_alias")
    def register_key_alias_on_node(self, node):
        """
        registers a key alias
        :param node: a specific node to place the alias on
        :return: new key alias as a `str`
        """

        session = self.node_sessions[node]
        if self.use_sync_api:
            key_alias = node_api_client.register_key_alias(session, sync=True)
            self._sync_sessions_for_sync_api(session)
        else:
            job = node_api_client.register_key_alias(session)
            job.network_client = self
            completed_job = job.sync_with(*self.alias_locations.keys())
            key_alias = completed_job.key_alias
            if key_alias is None:
                raise KeyError("No 'signing_key_alias' in job event: " + str(completed_job.event))

        self.record_key_alias(key_alias, node)
        return key_alias

    @beeline.traced(name="network.register_key_alias")
    def register_key_alias_on_node_index(self, node_index):
        """
        registers a key alias on a specific node (0-indexed)
        :return: new key alias as a `str`
        """
        return self.register_key_alias_on_node(self._fixed_node(node_index))

    @beeline.traced(name="network.register_key_alias")
    def register_key_alias_on_node_0(self):
        """
        registers a key alias
        :return: new key alias as a `str`
        """
        return self.register_key_alias_on_node(self._fixed_node_0())

    @beeline.traced(name="network.register_key_alias")
    def register_key_alias_on_node_1(self):
        """
        registers a key alias
        :return: new key alias as a `str`
        """
        return self.register_key_alias_on_node(self._fixed_node_1())

    @beeline.traced(name="network.register_key_alias")
    def register_key_alias_on_node_2(self):
        """
        registers a key alias
        :return: new key alias as a `str`
        """
        return self.register_key_alias_on_node(self._fixed_node_2())

    @beeline.traced(name="network.register_key_alias")
    def register_key_alias_on_node_3(self):
        """
        registers a key alias
        :return: new key alias as a `str`
        """
        return self.register_key_alias_on_node(self._fixed_node_3())

    @beeline.traced(name="network.deregister_key_alias")
    def deregister_key_alias(self, key_alias):
        """
        deregisters a key alias
        :param key_alias: The key alias to deregister
        :return: None
        """
        node = self.alias_locations[key_alias]
        session = self.node_sessions[node]
        if self.use_sync_api:
            node_api_client.deregister_key_alias(session, key_alias, sync=True)
            self._sync_sessions_for_sync_api(session)
        else:
            job = node_api_client.deregister_key_alias(session, key_alias)
            job.network_client = self
            job.sync_with(*self.alias_locations.keys())

    def publish_with_deps(self, contract_refs):
        """
        an alternate mode to publish that both publishes the target refs, but also all of their depenencies.
        it does this by doing a depth first search on the deps as identified by the validator. this function
        is only supported for language 5 onward.
        """
        self.publish(contract_refs_with_deps(self.contract_path, contract_refs))

    @beeline.traced(name="network.publish")
    def publish(self, contract_refs):
        """
        publishes the specified contracts to the network, however skip publishing
        any already published and consider those successful
        :param key_alias: what key_alias to publish as
        :param contract_refs: list of contract_refs to publish
        :return: None
        """
        session = self._random_session()
        published_already = [ContractRef.from_json(o['ref']) for o in node_api_client.list_contracts(session)]
        not_yet_published = [ref for ref in contract_refs if ref not in published_already]
        if len(not_yet_published) == 0:
            return

        # branch - we have two different types of publishing, neo publish or old style rest api publish

        # get the index of the last event before publishing
        events = node_api_client.events(session)
        last_event_index = events[-1]['index'] if len(events) > 0 else 1

        append_result = node_api_client.neo_publish_contracts(session, self.contract_path, not_yet_published,
                                                                  self.neo_key, self.neo_crt)
        self.sync_neo_tx(session, append_result)

        # get events resulting from the publishing
        events = node_api_client.events(session, start_index=last_event_index)

        # now because we can't get errors back, we have to figure out if we successfully published
        published_refs = [ContractRef.from_json(o['ref']) for o in node_api_client.list_contracts(session)]
        missing_refs = [ref for ref in contract_refs if ref not in published_refs]

        if len(missing_refs) > 0:
            try:
                # try to access the latest job fail event and extract the error
                failure = [event for event in events if "job_fail" in event['type']][-1]['data']['error']
                try:
                    # try to access the nested error if it has been created in another component
                    failure = failure['data'][0]['error']
                except Exception:
                    pass
            except Exception as e:
                failure = f'no error found in job failed events: {e}.\nThe events are\n{events}'
            raise Exception(f'Some contracts could not be published to publish: {missing_refs}'
                            + (f'\n(published refs are: {published_refs})' if len(published_refs) > 0 else '')
                            + f'\nFailure:\n {failure}\n')

    @beeline.traced(name="network.sync_call")
    def sync_call(self, key_alias, contract_ref, function, kwargs):
        """
        calls the specified contract function on a node
        :param key_alias: key_alias to invoke as
        :param contract_ref: contract to call
        :param function: function to invoke
        :param kwargs: dictionary of arguments to the contract, will be json serialized
        :return: the result of the call as a value
        """
        session = self.node_sessions[self.alias_locations[key_alias]]
        if self.use_sync_api:
            result = node_api_client.call(session, key_alias, contract_ref, function, kwargs,
                                          sync=True, query_tx_index=self.query_tx_index)
            self.query_tx_index = None  # this is ugly! please refactor!!
            self._sync_sessions_for_sync_api(session)
            return result
        else:
            # if this clientside does not post, it'll be the value read, otherwise a job
            maybe_job = node_api_client.call(session, key_alias, contract_ref, function, kwargs,
                                             query_tx_index=self.query_tx_index)
            self.query_tx_index = None
            if isinstance(maybe_job, Job):
                maybe_job.network_client = self
                try:
                    completed_job = maybe_job.sync_with(*self.alias_locations.keys())
                    return completed_job.result['result']
                except ContractErrorInJob as e:
                    language = contract_ref.language
                    from _assembly.lib.system import error_ctors
                    raise error_ctors[language](e.msg, e.data)
            else:
                return maybe_job

    @beeline.traced(name="network.async_call")
    def async_call(self, key_alias, contract_ref, function, kwargs):
        """
        calls the specified contract function on a node
        :param key_alias: key_alias to invoke as
        :param contract_ref: contract to call
        :param function: function to invoke
        :param kwargs: dictionary of arguments to the contract, will be json serialized
        :return: the result of the call as a value or job object
        """
        if self.use_sync_api:
            raise Exception('cannot perform async node api operations with sync mode client')

        session = self.node_sessions[self.alias_locations[key_alias]]

        # if this clientside does not post, it'll be the value read, otherwise a job
        maybe_job = node_api_client.call(session, key_alias, contract_ref, function, kwargs,
                                         query_tx_index=self.query_tx_index)
        self.query_tx_index = None

        if isinstance(maybe_job, Job):
            maybe_job.network_client = self
            return maybe_job
        else:
            return maybe_job

    @beeline.traced(name="network.list_key_aliases")
    def list_key_aliases(self, node=None, locality=None, channel=None):
        """
        lists the key aliases registered and known
        :return: list of key aliases known to the node
        """
        if node is None:
            node = self._random_node()

        session = self.node_sessions[node]
        return node_api_client.list_key_aliases(session, locality=locality, channel=channel)

    @beeline.traced(name="network.list_deregistered_key_aliases")
    def list_deregistered_key_aliases(self, node=None):
        """
        lists the key aliases registered and known
        :return: list of key aliases known to the node
        """
        if node is None:
            node = self._random_node()

        session = self.node_sessions[node]
        return node_api_client.list_deregistered_key_aliases(session)

    @beeline.traced(name="network.list_contracts")
    def list_contracts(self):
        """
        inspection for contracts on a network
        :return: information about each contract published
        """
        session = self._random_session()
        return node_api_client.list_contracts(session)

    def contract_info(self, contract_ref):
        """
        detailed inspection of a specific contract, will include function signatures
        :param contract_ref: contract to inspect
        :return: information about the contract
        """
        session = self._random_session()
        return node_api_client.contract_info(session, contract_ref)

    @beeline.traced(name='network.reset')
    def reset(self, txe_protocol=None, sympl_version=DEFAULT_LANGUAGE_VERSION):
        """
        reset the network, clearing all transaction history and all registered key_aliases
        """
        session = self._random_session()
        result = node_api_client.reset(session)
        # this takes a special route through the syncer and works based on network seed, as we reset
        # the tx_index so any delayed node happily shows up as "caught up"
        network_syncer.sync_sessions(session, None, self.node_sessions.values())

        self.upgrade_protocol(txe_protocol=txe_protocol, sympl_version=sympl_version)

        return result

    @beeline.traced(name='network.restart_at')
    def restart_at(self, tx_index: int):
        """
        restart all the nodes at a specific tx_index
        """
        for session in self.node_sessions.values():
            node_api_client.restart_at(session, tx_index)

        return None

    def upgrade_protocol(self,
                         txe_protocol: Optional[int] = None,
                         sympl_version: Optional[int] = None,
                         fail_silently=True):
        """
        sends a neo transaction to upgrade protocols
        :param txe_protocol: new maximum txe protocol, this is set to the minimum required for the target
                             `sympl_version` if not provided
        :param sympl_version: version of Symbiont Programming Language
        :param fail_silently: This is ignored here for a moment as we are not checking for upgrades error when using
                              network_client - we should once.
        :return: None
        """

        # this is a simple mapping of the txe protocol versions required for each sympl_version, having it here
        # removes it as a concern for basic use of the sdk
        if sympl_version and not txe_protocol:
            txe_protocol = {
                5: 8,
                6: 8,
                7: 11,
                8: 12,
                9: 13,
            }.get(sympl_version)

        # if on a network without neo ops, we just assume all protocol versions are available and skip this
        session = self._random_session()
        append_result = node_api_client.neo_upgrade_protocol(session,
                                                             txe_protocol=txe_protocol,
                                                             sympl_version=sympl_version,
                                                             neo_key=self.neo_key,
                                                             neo_crt=self.neo_crt)
        self.sync_neo_tx(session, append_result)

    def current_time(self):
        session = self._random_session()
        return node_api_client.current_time(session)

    def set_time(self, timestamp):
        """
        set the current time to approximately the desired value. this is approximate as the time
        will change as this executes, resulting in drift similar in magnitude to the time it takes to
        call this function
        :param timestamp: target timestamp in nanoseconds
        :return: None
        """
        session = self._random_session()
        result = node_api_client.set_time(session, timestamp)
        self._sync_sessions_for_sync_api(session)
        self.wait_for_ready()
        return result

    def add_timeshift(self, timeshift):
        """
        set the current time shift value
        :param timeshift: desired time shift value in nanoseconds
        :return: None
        """
        session = self._random_session()
        result = node_api_client.add_timeshift(session, timeshift)

        self._sync_sessions_for_sync_api(session)
        self.wait_for_ready()
        return result

    def get_timeshift(self):
        """
        get the current time shift value
        :return: current time shift in nanoseconds
        """
        session = self._random_session()
        return node_api_client.get_timeshift(session)

    def current_datetime(self):
        session = self._random_session()
        return node_api_client.current_datetime(session)

    def set_datetime(self, timestamp):
        """
        set the current time to approximately the desired value. this is approximate as the time
        will change as this executes, resulting in drift similar in magnitude to the time it takes to
        call this function
        :param timestamp: target timestamp in nanoseconds
        :return: None
        """
        session = self._random_session()
        result = node_api_client.set_datetime(session, timestamp)
        self._sync_sessions_for_sync_api(session)
        self.wait_for_ready()
        return result

    def add_datetime_shift(self, timeshift):
        """
        set the current time shift value
        :param timeshift: desired time shift value as DateTimeDelta
        :return: None
        """
        session = self._random_session()
        result = node_api_client.add_datetime_shift(session, timeshift)

        self._sync_sessions_for_sync_api(session)
        self.wait_for_ready()
        return result

    def get_datetime_shift(self):
        """
        get the current time shift value
        :return: current time shift as DateTimeDelta
        """
        session = self._random_session()
        return node_api_client.get_datetime_shift(session)

    def channels(self, key_alias):
        if key_alias in self.alias_locations:
            session = self.node_sessions[self.alias_locations[key_alias]]
        else:
            session = self._random_session()

        return node_api_client.channels(session, key_alias)

    @beeline.traced(name="network.consistency_check")
    def consistency_check(self, tx_index=None):
        # todo : we need a much more elegant way to handle this
        if not self.skip_cleanup_consistency_check:
            if tx_index is None:
                max_session = None
                max_tx_index = -1
                sessions = self.node_sessions.values()
                for session in sessions:
                    last_tx_index = node_api_client.statusz(session)['last_tx_index']
                    if last_tx_index > max_tx_index:
                        max_session = session
                        max_tx_index = last_tx_index

                network_syncer.sync_sessions(max_session, max_tx_index, sessions)
                tx_index = max_tx_index

            channels = {}
            for k in self.node_sessions:
                session = self.node_sessions[k]
                if self.use_sync_api:
                    res = node_api_client.digest(session, tx_index, sync=True)
                else:
                    job = node_api_client.digest(session, tx_index)
                    job.network_client = self
                    completed_job = job.sync_with()
                    res = completed_job.result['digest']

                digest = res['storage']
                for channel in digest:
                    if channel not in channels:
                        channels[channel] = {}

                    channels[channel][k] = digest[channel]

            diff = {}
            for channel in channels:
                if len(set(channels[channel].values())) != 1:
                    diff[channel] = channels[channel]

            if diff != {}:
                raise Exception(diff)

    def append_smartlog_transaction(self, key_alias, topics, data):
        """
        writes this transaction directly to the append transactions api on smartlog,
        bypassing epilog
        :param key_alias: target the specified key_alias's node
        :param topics: list of string topics
        :param data: transaction body in byte form
        :return: dictionary indicating sequenced at what tx_index
        """
        session = self.node_sessions[self.alias_locations[key_alias]]
        if key_alias not in self.alias_locations:
            raise Exception(f'attempting to act as key_alias {key_alias} that does not yet exist in network client')
        return node_api_client.append_smartlog_transaction(session, topics, data)

    def get_smartlog_transactions(self,
                                  key_alias,
                                  start_index,
                                  topics=None,
                                  max_count=100,
                                  include_invalid_transactions=False):
        """
        reads raw transactions directly from the smartlog api, as per
        /src/klyntar/network/distlog/api/rest/readme.md
        :param key_alias: target the specified key_alias's node
        :param start_index: the first index to retrieve
        :param max_count: maximum number of transactions to return
        :param include_invalid_transactions: should invalid neo transactions also be returned
        :return: a list of transactions packaged up in a dictionary with metadata info
        """
        session = self.node_sessions[self.alias_locations[key_alias]]
        if key_alias not in self.alias_locations:
            raise Exception(f'attempting to act as key_alias {key_alias} that does not yet exist in network client')
        return node_api_client.get_transactions(session, 'smartlog', start_index, topics, max_count,
                                                include_invalid_transactions)

    def __getitem__(self, key_alias):
        """
        syntactic sugar to allow accessing a particular key_alias's node via `[]` syntax
        """
        return KeyAliasClient(self, self.node_sessions[self.alias_locations[key_alias]], key_alias, is_async=False)

    def __getattr__(self, item):
        """
        syntactic sugar for using the async api directly
        """
        if item == 'use_async':
            return AsyncModeClient(self)
        else:
            self.__getattribute__(item)

    def sync_neo_tx(self, origin_session, append_result):
        """
        given a successful neo tx submission, synchronize the network. this will not work for networks with very
        large numbers of neo transactions, as each neo tx of the specified topic must be scanned linearly
        :param origin_session: session to use for initial lookups, any would work
        :param append_result: the dictionary of result info from submitting the txe
        :return: None or Exception if timeout
        """
        # todo : add timeout
        next_start = 1
        while True:
            """
            TODO: Assess if this is necessary following merge of epilog/smartlog
            """
            epilog_transactions = node_api_client.get_transactions(origin_session,
                                                                   'smartlog',
                                                                   next_start,
                                                                   topics=append_result['topics'][0])
            matches = [tx for tx in epilog_transactions['transactions'] if tx['hash'] == append_result['tx_hash']]
            if len(matches) == 1:
                epilog_index = matches[0]['tx_index']
                break
            else:
                next_start = epilog_transactions['last_index'] + 1

        # Now that reset is handled by TXE, we must adjust
        # the transaction index from smartlog as TXE would.
        status = node_api_client.statusz(origin_session)
        offset = status.get('last_reset_index', 0)

        network_syncer.sync_sessions(origin_session, epilog_index - offset, self.node_sessions.values())

    def sync_sessions(self, origin_session, tx_index, sessions, timeout=120):
        """
        an internal helper for syncing nodes, place here for avoiding circular imports
        :param origin_session: a session for the node that originated the work, we know it is already synced
        :param tx_index: the index we need each node to reach
        :param sessions: a session for each node we want caught up to this point
        :return: None
        """
        network_syncer.sync_sessions(origin_session, tx_index, sessions, timeout=timeout)

    def wait_for_ready(self):
        """
        ensures network is ready by firing a noop neo transaction and synchronizing on it flowing through
        """
        self.upgrade_protocol(sympl_version=DEFAULT_LANGUAGE_VERSION)

    def add_session(self, node_name, new_session):
        """
        sometimes the set of nodes changes over time, this function inserts a new one into the client
        :param new_session: `NodeSession` to insert
        """
        if node_name in self.node_sessions:
            raise Exception(f'attempted to add node {node_name} to network client but already present')
        self.node_sessions[node_name] = new_session

    def refresh_config(self, network_config_path):
        """
        update the current nodes with new nodes based on the provided network config. warning: could work
        unpredictably & lose key aliases if node count is changing. warning: drops event cache
        :param network_config_path: path of the new network config file
        :return: None
        """
        import json
        from _assembly.sdk.util.path_util import prep_path, prepare_cert
        from _assembly.sdk.client.node_client import NodeSession

        with open(prep_path(network_config_path)) as f:
            config = json.load(f)

        new_sessions = {}

        node_configs = config.get('nodes') or config
        for node_name, node_config in node_configs.items():
            new_sessions[node_name] = NodeSession(
                hostname=node_config['hostname'],
                certs=(
                    prepare_cert(node_config.get('client_cert'),     'client', 'crt', node_name),
                    prepare_cert(node_config.get('client_cert_key'), 'client', 'key', node_name)
                ),
                admin_certs=(
                    prepare_cert(node_config.get('admin_cert'),     'admin', 'crt', node_name),
                    prepare_cert(node_config.get('admin_cert_key'), 'admin', 'key', node_name),
                ),
                ca_cert=prepare_cert(node_config.get('ca_cert'), 'ca', 'crt', node_name),
                node_fqdn=node_name
            )

        self.node_sessions = new_sessions

    def at_tx_index(self, tx_index, minor_tx_index):
        self.query_tx_index = (tx_index, minor_tx_index)
        return self

    def at_timestamp(self, timestamp):
        return self


class AsyncModeClient():
    def __init__(self, network_client):
        self.network_client = network_client

    def __getitem__(self, item):
        """
        proxy through calls but if getting a `KeyAliasClient` insert the async flag
        """
        return KeyAliasClient(self.network_client,
                              self.network_client.node_sessions[self.network_client.alias_locations[item]],
                              item,
                              is_async=True)

    def __getattr__(self, item):
        return self.network_client.__getattr__(item)


class KeyAliasClient():
    def __init__(self, network_client, session, key_alias, is_async):
        self.network_client = network_client
        self.session = session
        self.key_alias = key_alias
        self.is_async = is_async

    def events(self):
        return node_api_client.events(self.session)

    def __getattr__(self, contract_name):
        return ContractClient(self.network_client, self.session, self.key_alias, contract_name, self.is_async)


class ContractClient():
    def __init__(self, network_client, session, key_alias, contract_name, is_async):
        self.network_client = network_client
        self.session = session
        self.key_alias = key_alias
        self.is_async = is_async
        self.language_version = network_client.language_version
        self.contract_name = contract_name

    def __getitem__(self, version):
        s = version.split('-')
        if len(s) == 1:
            self.contract_ref = ContractRef(self.contract_name, version, self.language_version)
        elif len(s) == 2:
            self.contract_ref = ContractRef(self.contract_name, s[1], int(s[0]))
        else:
            raise Exception("Cannot parse {}, it needs to take a form `l-v.v.v` ir `v.v.v`".format(version))

        return self

    def __getattr__(self, function_name):
        if function_name == '__getstate__':
            raise AttributeError()

        if function_name == 'storage':
            return node_api_client.storage(self.session, self.key_alias, self.contract_ref)
        else:

            def _call(*args, **kwargs):
                # todo : remove this abomination, replace with a feature or just living without sugar
                if self.contract_ref.name == 'call_executable':
                    kwargs['contract_name'] = args[0]
                    kwargs['contract_version'] = args[1]
                    kwargs['func_name'] = args[2]
                    if len(args) == 4:
                        kwargs['fill'] = args[3]

                if self.is_async:
                    return self.network_client.async_call(self.key_alias, self.contract_ref, function_name, kwargs)
                else:
                    return self.network_client.sync_call(self.key_alias, self.contract_ref, function_name, kwargs)

            return _call
