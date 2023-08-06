from .models import *
from .. import constants
from ..base_client import BaseClient


class TokenIndexerClient(BaseClient):
    def __init__(self):
        super().__init__(constants.TOKEN_INDEXER_API_URL)

    async def address_balances(self, string: str, body: AddressBalancesRequest) -> BalancesAndCountResponse:
        """
        Balances data
        Search user balances by owner address
        """
        return await self.post(
            "/address/{string}/balances".format(string=string),
            body=body,
            response_model=BalancesAndCountResponse,
        )

    async def address_transactions(
            self,
            string: str,
            body: AddressTransactionsRequest
    ) -> AddressTransactionsInfoResponse:
        """
        User token transactions
        Search token transactions by owner address
        """
        return await self.post(
            "/address/{string}/transactions".format(string=string),
            body=body,
            response_model=AddressTransactionsInfoResponse,
        )

    async def balances(self, body: BalancesRequest) -> BalancesAndCountResponse:
        """
        Balances data
        Get all balances for different tokens
        """
        return await self.post(
            "/balances",
            body=body,
            response_model=BalancesAndCountResponse,
        )

    async def search_root_contracts(self, body: RootTokenContractsSearchRequest) -> RootTokenContractsSearchResponse:
        """
        Search root contracts
        Search root contracts by symbol substring with pagination
        """
        return await self.post(
            "/root_contract",
            body=body,
            response_model=RootTokenContractsSearchResponse,
        )

    async def root_contract_by_address(self, string: str) -> RootContractInfoWithTotalSupplyResponse:
        """
        Get root contract
        Get root contract data by its address
        """
        return await self.get(
            "/root_contract/root_address/{string}".format(string=string),
            response_model=RootContractInfoWithTotalSupplyResponse,
        )

    async def root_contract_by_symbol(self, string: str) -> list[RootContractInfoWithTotalSupplyResponse]:
        """
        Search root contracts
        Search root contracts by symbol substring
        """
        return await self.get(
            "/root_contract/symbol_substring/{string}".format(string=string),
            response_model=list[RootContractInfoWithTotalSupplyResponse],
        )

    async def token_wallet_by_address(self, string: str) -> TokenOwnerResponse:
        """
        Get token wallet data
        Get token wallet data by its address
        """
        return await self.get(
            "/token_owner/address/{string}".format(string=string),
            response_model=TokenOwnerResponse,
        )

    async def transactions(self, body: TransactionsRequest) -> TransactionsInfoAndCountResponse:
        """
        Search transactions
        """
        return await self.post(
            "/transactions",
            body=body,
            response_model=TransactionsInfoAndCountResponse,
        )
