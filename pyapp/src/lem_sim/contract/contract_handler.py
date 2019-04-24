import json

from lem_sim import contract


class ContractHandler(object):

    def __init__(self, web3, artefact_name):
        self._web3 = web3
        self._contract_dir = contract.CONTRACT_DIR
        self._artefact_name = artefact_name
        self._contract_artefact = self.get_contract_artefact()
        self._contract_abi = self._contract_artefact['abi']
        self._contract_address = self.get_address()
        self._contract = self._web3.eth.contract(address=self._contract_address, abi=self._contract_abi)

    @property
    def contract(self):
        return self._contract

    def get_contract_artefact(self):
        with open(self._contract_dir + self._artefact_name) as artefact_json:
            return json.load(artefact_json)

    def get_address(self):
        networks = self._contract_artefact['networks']
        addresses = []

        for network, attribute in networks.items():
            addresses.append(attribute['address'])

        # artefact can have multiple networks, always returns the current/last network
        return addresses[-1]
