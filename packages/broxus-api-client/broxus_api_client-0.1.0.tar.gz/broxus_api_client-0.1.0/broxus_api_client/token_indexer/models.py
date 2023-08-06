from __future__ import annotations

import typing
from enum import Enum

from broxus_api_client.base_model import _BaseModel


class BalancesOrdering(str, Enum):
    """
    Balances ordering
    """
    CREATEDATASCENDING = "createdatascending"
    CREATEDATDESCENDING = "createdatdescending"
    AMOUNTASCENDING = "amountascending"
    AMOUNTDESCENDING = "amountdescending"


class TransactionKind(str, Enum):
    """
    Event Type
    """
    MINT = "mint"
    BURN = "burn"
    SEND = "send"
    RECEIVE = "receive"
    SENDCANCELLATION = "sendcancellation"
    BURNCANCELLATION = "burncancellation"


class TransactionsOrdering(str, Enum):
    """
    Transactions ordering
    """
    BLOCKTIMEATASCENDING = "blocktimeatascending"
    BLOCKTIMEATDESCENDING = "blocktimeatdescending"


class AddressBalancesRequest(_BaseModel):
    """
    Pairs request
    """

    limit: int
    offset: typing.Optional[int]
    ordering: typing.Optional[BalancesOrdering]
    publicKey: typing.Optional[str]
    """
    Filter by token owner public key
    """
    rootAddress: typing.Optional[str]
    """
    Only search balances for specified root contracts
    """
    token: typing.Optional[str]
    """
    Filter by token symbol
    """


class AddressTransactionsInfoResponse(_BaseModel):
    """
    Address Transactions Info Response 
    """

    limit: int
    offset: int
    totalCount: int
    transactions: list[TransactionInfoResponse]


class TransactionInfoResponse(_BaseModel):
    """
    Transactions Info Response 
    """

    amount: str
    """
    amount
    """
    blockTime: int
    createdAt: int
    kind: TransactionKind
    receiver: TransactionSubjectResponse
    rootAddress: str
    sender: TransactionSubjectResponse
    token: str
    transactionHash: str


class TransactionSubjectResponse(_BaseModel):
    """
    Transactions Subject Response 
    """

    ownerAddress: str
    ownerPublicKey: typing.Optional[str]
    tokenWalletAddress: typing.Optional[str]


class AddressTransactionsRequest(_BaseModel):
    """
    Address Transactions Request
    """

    kind: typing.Optional[list[TransactionKind]]
    """
    Filter by transaction kind
    """
    limit: int
    messageHash: typing.Optional[str]
    """
    Filter by message hash
    """
    offset: typing.Optional[int]
    ordering: typing.Optional[TransactionsOrdering]
    publicKey: typing.Optional[str]
    """
    Filter by token owner public key
    """
    rootAddress: typing.Optional[list[str]]
    """
    Only search token transactions for specified root contracts
    """
    timestampBlockAtGe: typing.Optional[int]
    """
    Filter by timestamp in milliseconds (&gt;=)
    """
    timestampBlockAtLe: typing.Optional[int]
    """
    Filter by timestamp in milliseconds (&lt;=)
    """
    token: typing.Optional[str]
    """
    Filter by token symbol
    """
    transactionHash: typing.Optional[str]
    """
    Filter by transaction hash
    """


class BalanceResponse(_BaseModel):
    """
    Balance response
    """

    amount: str
    """
    amount
    """
    blockTime: int
    ownerAddress: str
    ownerPublicKey: typing.Optional[str]
    rootAddress: str
    token: str


class BalancesAndCountResponse(_BaseModel):
    balances: list[BalanceResponse]
    limit: int
    offset: int
    totalCount: int


class BalancesRequest(_BaseModel):
    """
    Pairs request
    """

    limit: int
    offset: typing.Optional[int]
    ordering: typing.Optional[BalancesOrdering]
    ownerAddress: typing.Optional[str]
    """
    Filter by token owner address
    """
    publicKey: typing.Optional[str]
    """
    Filter by token owner public key
    """
    rootAddress: typing.Optional[str]
    """
    Only search balances for specified root contracts
    """
    token: typing.Optional[str]
    """
    Filter by token symbol
    """


class RootContractInfoWithTotalSupplyResponse(_BaseModel):
    codeHash: str
    decimals: int
    name: str
    rootAddress: str
    rootOwnerAddress: str
    rootPublicKey: str
    symbol: str
    totalSupply: str
    """
    totalSupply
    """


class RootTokenContractsSearchRequest(_BaseModel):
    """
    Root token contract by substring request
    """

    limit: int
    offset: int
    substring: typing.Optional[str]
    """
    Token symbol substring
    """


class RootTokenContractsSearchResponse(_BaseModel):
    """
    Root token contract by substring response
    """

    limit: int
    offset: int
    rootTokenContracts: list[RootContractInfoWithTotalSupplyResponse]
    totalCount: int


class TokenOwnerResponse(_BaseModel):
    """
    Token owner response
    """

    address: str
    codeHash: str
    createdAt: int
    ownerAddress: str
    ownerPublicKey: typing.Optional[str]
    rootAddress: str
    scale: int
    token: str


class TransactionsInfoAndCountResponse(_BaseModel):
    limit: int
    offset: int
    totalCount: int
    transactions: list[TransactionInfoResponse]


class TransactionsRequest(_BaseModel):
    """
    Transactions request
    """

    kind: typing.Optional[list[TransactionKind]]
    """
    Filter by transaction kind
    """
    limit: int
    messageHash: typing.Optional[str]
    """
    Filter by message hash
    """
    offset: typing.Optional[int]
    ordering: typing.Optional[TransactionsOrdering]
    ownerAddress: typing.Optional[str]
    """
    Filter by token owner address
    """
    ownerPublicKey: typing.Optional[str]
    """
    Filter by token owner public key
    """
    rootAddress: typing.Optional[list[str]]
    """
    Only search token transactions for specified root contracts
    """
    timestampBlockAtGe: typing.Optional[int]
    """
    Filter by timestamp in milliseconds (&gt;=)
    """
    timestampBlockAtLe: typing.Optional[int]
    """
    Filter by timestamp in milliseconds (&lt;=)
    """
    token: typing.Optional[str]
    """
    Filter by token symbol
    """
    transactionHash: typing.Optional[str]
    """
    Filter by transaction hash
    """


AddressBalancesRequest.update_forward_refs()
AddressTransactionsInfoResponse.update_forward_refs()
AddressTransactionsRequest.update_forward_refs()
TransactionInfoResponse.update_forward_refs()
