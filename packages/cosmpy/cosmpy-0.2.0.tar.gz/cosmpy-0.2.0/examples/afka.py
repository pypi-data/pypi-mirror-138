from cosmpy.clients.crypto import CosmosCrypto
from cosmpy.clients.ledger import CosmosLedger
from cosmpy.common.rest_client import RestClient
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin
from cosmpy.protos.tendermint.abci.types_pb2 import Response

RPC_ENDPOINT_ADDRESS = "rpc-capricorn.fetch.ai:443"  # capricorn testnet
CHAIN_ID = "capricorn-1"
# Private key of sender's account
crypto = CosmosCrypto(private_key=PrivateKey(b"abcdabcdabcdabcdabcdabcdabcdabcd"))
# Create client

ledger = CosmosLedger(
    rpc_node_address=RPC_ENDPOINT_ADDRESS, secure_channel=True, chain_id=CHAIN_ID
)
balance = ledger.get_balance(crypto.get_address(), "atestfet")

print(balance)
