from .models import *
from .. import constants
from ..base_client import BaseClient


class ExplorerClient(BaseClient):
    def __init__(self):
        super().__init__(constants.EXPLORER_API_URL)

    async def accounts(self, body: AccountByIdRequest) -> AccountResponse:
        """
        Account data
        Get Account data.
        """
        return await self.post("/accounts", body=body, response_model=AccountResponse)

    async def accounts_count(self, body: AccountsCountRequest) -> CountResponse:
        """
        Accounts count data
        Get Accounts count data.
        """
        return await self.post("/accounts/count", body=body, response_model=CountResponse)

    async def accounts_list(self, body: AccountsRequest) -> list[AccountResponse]:
        """
        Accounts data
        Get Accounts data.
        """
        return await self.post("/accounts/list", body=body, response_model=list[AccountResponse])

    async def accounts_state(self, body: AccountByIdRequest) -> AccountStateResponse:
        """
        Account state
        """
        return await self.post("/accounts/state", body=body, response_model=AccountStateResponse)

    async def blocks(self, body: ExactBlockRequest) -> BlockResponse:
        """
        Blocks data
        Get Blocks data.
        """
        return await self.post("/blocks", body=body, response_model=BlockResponse)

    async def blocks_count(self, body: BlocksCountRequest) -> CountResponse:
        """
        Blocks count data
        Get Blocks count data.
        """
        return await self.post("/blocks/count", body=body, response_model=CountResponse)

    async def blocks_list(self, body: BlocksRequest) -> list[BlockBriefResponse]:
        """
        Blocks list data
        Get Blocks list data.
        """
        return await self.post("/blocks/list", body=body, response_model=list[BlockBriefResponse])

    async def blocks_messages(self, body: HashRequest) -> BlockMessagesResponse:
        """
        Blocks in and out messages
        """
        return await self.post("/blocks/messages", body=body, response_model=BlockMessagesResponse)

    async def convert_address(self, body: AccountByIdRequest) -> ConvertedAddressResponse:
        """
        Convert address
        """
        return await self.post("/convert_address", body=body, response_model=ConvertedAddressResponse)

    async def elections_bonuses(self) -> list[ElectionBonusesResponse]:
        """
        Validator set bonuses for recent election
        """
        return await self.make_request("get", "/elections/bonuses", response_model=list[ElectionBonusesResponse])

    async def elections_config(self) -> ElectionsConfigResponse:
        """
        Brief elections config
        """
        return await self.make_request("get", "/elections/config", response_model=ElectionsConfigResponse)

    async def elections_current_validators_top(self) -> list[CurrentValidatorResponse]:
        """
        Brief current validators set (at most 10 items)
        """
        return await self.make_request(
            "get",
            "/elections/current_validators_top",
            response_model=list[CurrentValidatorResponse],
        )

    async def elections_state(self) -> ElectorDataResponse:
        """
        Full elections state
        """
        return await self.make_request("get", "/elections/state", response_model=ElectorDataResponse)

    async def messages(self, body: HashRequest) -> MessageResponse:
        """
        Message data
        Get Message data.
        """
        return await self.post("/messages", body=body, response_model=MessageResponse)

    async def messages_count(self, body: MessagesCountRequest) -> CountResponse:
        """
        Messages count data
        Get Messages count data.
        """
        return await self.post("/messages/count", body=body, response_model=CountResponse)

    async def messages_list(self, body: MessagesRequest) -> list[TransactionMessageResponse]:
        """
        Messages data
        Get Messages data.
        """
        return await self.post("/messages/list", body=body, response_model=list[TransactionMessageResponse])

    async def messages_occurrences(self, body: HashRequest) -> list[MessageOccurrenceResponse]:
        """
        Message occurrences in transactions
        """
        return await self.post("/messages/occurrences", body=body, response_model=list[MessageOccurrenceResponse])

    async def search(self, body: SearchRequest) -> list[SearchMatchResponse]:
        """
        Search in all tables
        Search accounts by code hash, address, blocks by seqno, root hash, messages by hash, transaction by hash.
        """
        return await self.post("/search", body=body, response_model=list[SearchMatchResponse])

    async def stats(self) -> BlockChainStatsResponse:
        """
        Blockchain statistics
        """
        return await self.make_request("get", "/stats", response_model=BlockChainStatsResponse)

    async def time(self) -> int:
        """
        Server UTC timestamp (milliseconds)
        """
        return await self.make_request("get", "/time", response_model=int)

    async def transactions(self, body: HashRequest) -> TransactionResponse:
        """
        Transaction data
        Get Transaction data.
        """
        return await self.post("/transactions", body=body, response_model=TransactionResponse)

    async def transactions_count(self, body: TransactionsRequest) -> CountResponse:
        """
        Transactions count data
        Get Transactions count data.
        """
        return await self.post("/transactions/count", body=body, response_model=CountResponse)

    async def transactions_list(self, body: TransactionsRequest) -> list[TransactionBriefResponse]:
        """
        Transactions data
        Get Transactions data.
        """
        return await self.post("/transactions/list", body=body, response_model=list[TransactionBriefResponse])
