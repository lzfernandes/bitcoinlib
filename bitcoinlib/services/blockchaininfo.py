# -*- coding: utf-8 -*-
#
#    BitcoinLib - Python Cryptocurrency Library
#    blockchain_info client
#    © 2017 June - 1200 Web Development <http://1200wd.com/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
from bitcoinlib.services.baseclient import BaseClient

PROVIDERNAME = 'blockchaininfo'

_logger = logging.getLogger(__name__)


class BlockchainInfoClient(BaseClient):

    def __init__(self, network, base_url, denominator, api_key=''):
        super(self.__class__, self).__init__(network, PROVIDERNAME, base_url, denominator, api_key)

    def compose_request(self, cmd, parameter='', variables=None, method='get'):
        url_path = cmd
        if parameter:
            url_path += '/' + parameter
        return self.request(url_path, variables, method=method)

    def getbalance(self, addresslist):
        addresses = {'active': '|'.join(addresslist)}
        res = self.compose_request('balance', variables=addresses)
        balance = 0
        for address in res:
            balance += res[address]['final_balance']
        return balance

    def getutxos(self, addresslist):
        utxos = []
        for address in addresslist:
            variables = {'active': address, 'limit': 1000}
            res = self.compose_request('unspent', variables=variables)
            if len(res['unspent_outputs']) > 299:
                _logger.warning("BlockchainInfoClient: Large number of outputs for address %s, "
                                "UTXO list may be incomplete" % address)
            for utxo in res['unspent_outputs']:
                utxos.append({
                    'address': address,
                    'tx_hash': utxo['tx_hash_big_endian'],
                    'confirmations': utxo['confirmations'],
                    'output_n': utxo['tx_output_n'],
                    'index':  utxo['tx_index'],
                    'value': int(round(utxo['value'] * self.units, 0)),
                    'script': utxo['script'],
                })
        return utxos

    def address_transactions(self, addresslist):
        # TODO: write this method if possible
        pass

    def getrawtransaction(self, txid):
        res = self.compose_request('rawtx', txid, {'format': 'hex'})
        return res

