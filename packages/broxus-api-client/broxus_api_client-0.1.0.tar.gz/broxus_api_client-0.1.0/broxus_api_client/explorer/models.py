from __future__ import annotations

import typing
from enum import Enum

from broxus_api_client.base_model import _BaseModel

Address = str


class AccountColumn(str, Enum):
    """
    Account column
    """
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
    BALANCE = "balance"


class AccountState(str, Enum):
    NON_EXIST = "NonExist"
    UNINIT = "Uninit"
    ACTIVE = "Active"
    FROZEN = "Frozen"
    DELETED = "Deleted"


class Direction(str, Enum):
    """
    Transactions ordering
    """
    ASC = "ASC"
    DESC = "DESC"


class AccountStatusChange(str, Enum):
    UNCHANGED = "Unchanged"
    FROZEN = "Frozen"
    DELETED = "Deleted"


class BlockColumn(str, Enum):
    """
    Transaction column
    """
    GEN_UTIME = "genUtime"
    SEQNO = "seqno"


class MessageType(str, Enum):
    INTERNAL = "Internal"
    EXTERNAL_IN = "ExternalIn"
    EXTERNAL_OUT = "ExternalOut"


class ComputeSkipReason(str, Enum):
    NO_STATE = "NoState"
    BAD_STATE = "BadState"
    NO_GAS = "NoGas"


class MessageColumn(str, Enum):
    """
    Message column
    """
    TRANSACTION_TIME = "transactionTime"
    MESSAGE_VALUE = "messageValue"


class TransactionType(str, Enum):
    ORDINARY = "Ordinary"
    STORAGE = "Storage"
    TICK_TOCK = "TickTock"
    SPLIT_PREPARE = "SplitPrepare"
    SPLIT_INSTALL = "SplitInstall"
    MERGE_PREPARE = "MergePrepare"
    MERGE_INSTALL = "MergeInstall"


class TransactionAccountStatus(str, Enum):
    UNINIT = "Uninit"
    ACTIVE = "Active"
    FROZEN = "Frozen"
    NON_EXIST = "NonExist"


class TransactionColumn(str, Enum):
    """
    Transaction column
    """
    TIME = "time"
    BALANCE_CHANGE = "balanceChange"


class TransactionTickTock(str, Enum):
    TICK = "Tick"
    TOCK = "Tock"


class AccountBlock(_BaseModel):
    address: Address
    newHash: str
    oldHash: str
    transactionCount: int
    wc: int


AccountBlocks = list[AccountBlock]


class AccountByIdRequest(_BaseModel):
    """
    Account by id request
    """

    id: Address


class AccountReferenceResponse(_BaseModel):
    """
    Account reference
    """

    address: str
    balance: int
    state: AccountState
    workchain: int


class AccountResponse(_BaseModel):
    """
    Account response
    """

    address: str
    balance: str
    codeHash: typing.Optional[str]
    createdAt: int
    creatorAddress: typing.Optional[str]
    creatorWc: int
    dataHash: typing.Optional[str]
    initCodeHash: typing.Optional[str]
    state: AccountState
    updatedAt: int
    updatedLt: int
    workchain: int


class AccountsCountRequest(_BaseModel):
    """
    Accounts count request
    """

    balanceGe: typing.Optional[int]
    balanceLe: typing.Optional[int]
    codeHash: typing.Optional[str]
    createdAtGe: typing.Optional[int]
    createdAtLe: typing.Optional[int]
    initCodeHash: typing.Optional[str]
    state: typing.Optional[AccountState]
    updatedAtGe: typing.Optional[int]
    updatedAtLe: typing.Optional[int]
    workchain: typing.Optional[int]


class AccountsOrdering(_BaseModel):
    """
    Transactions ordering
    """

    column: AccountColumn
    direction: Direction


class AccountsRequest(_BaseModel):
    """
    Accounts request
    """

    balanceGe: typing.Optional[int]
    balanceLe: typing.Optional[int]
    codeHash: typing.Optional[str]
    createdAtGe: typing.Optional[int]
    createdAtLe: typing.Optional[int]
    initCodeHash: typing.Optional[str]
    limit: int
    offset: int
    ordering: typing.Optional[AccountsOrdering]
    state: typing.Optional[AccountState]
    updatedAtGe: typing.Optional[int]
    updatedAtLe: typing.Optional[int]
    workchain: typing.Optional[int]


class AccountStateResponse(_BaseModel):
    """
    Account state response
    """

    state: RawAccountState


class RawAccountState(_BaseModel):
    codeBoc: typing.Optional[str]
    dataBoc: typing.Optional[str]
    storageStat: AccountStorageInfo


class AccountStorageInfo(_BaseModel):
    duePayment: typing.Optional[int]
    lastPaid: int
    used: AccountStorageUsed


class AccountStorageUsed(_BaseModel):
    bits: int
    cells: int
    publicCells: int


class BlkPrevInfo(_BaseModel):
    pass


class BlockBriefResponse(_BaseModel):
    """
    Block brief response
    """

    genSoftwareVersion: int
    genUtime: int
    isKeyBlock: bool
    rootHash: str
    seqno: int
    shard: str
    transactionCount: int
    workchain: int


class BlockChainStatsResponse(_BaseModel):
    """
    Blockhain stats
    """

    accountsActive1h: int
    accountsActive24h: int
    accountsActiveTotal: int
    accountsCreated1h: int
    accountsCreated24h: int
    circulationSupply: int
    fetchedAt: int
    latestMcSeqno: int
    messages1h: int
    messages24h: int
    messagesTotal: int
    totalSupply: int
    transactions1h: int
    transactions24h: int
    transactionTotal: int
    volume24h: int


class BlockInfo(_BaseModel):
    """
    Block info
    """

    afterMerge: typing.Optional[bool]
    """
    Is this block after shards merge
    """
    afterSplit: typing.Optional[bool]
    """
    Is this block after splitting the shards
    """
    beforeSplit: typing.Optional[bool]
    """
    Is this block before splitting the shards
    """
    endLt: str
    """
    Maximum logical time in block
    """
    flags: int
    """
    Block flags
    """
    genCatchainSeqno: int
    """
    The sequence number of catchain session which generated this block
    """
    genSoftware: GlobalVersion
    genValidatorListHashShort: int
    """
    Short hash of the set of validators that generated this block
    """
    keyBlock: typing.Optional[bool]
    """
    Is this block a key block
    """
    masterRef: typing.Optional[ExtBlkRef]
    minRefMcSeqno: int
    """
    Minimal references masterchain seqno
    """
    prevKeyBlockSeqno: int
    """
    Previous key block sequence number
    """
    prevRef: BlkPrevInfo
    prevVertRef: typing.Optional[BlkPrevInfo]
    startLt: str
    """
    Minimal logical time in block
    """
    version: typing.Optional[int]
    """
    Block version
    """
    vertSeqNo: typing.Optional[int]
    """
    Vertical sequence number
    """
    vertSeqNoIncr: typing.Optional[int]
    """
    Yes
    """
    wantMerge: typing.Optional[bool]
    """
    Will the current shard ever be merged
    """
    wantSplit: typing.Optional[bool]
    """
    Will the current shard ever be split
    """


class GlobalVersion(_BaseModel):
    capabilities: int
    version: int


class ExtBlkRef(_BaseModel):
    endLt: int
    rootHash: str
    seqNo: int


class BlockMessagesResponse(_BaseModel):
    """
    Block messages response
    """

    inMessages: list[TransactionMessageResponse]
    outMessages: list[TransactionMessageResponse]


class TransactionMessageResponse(_BaseModel):
    """
    Transaction Message Response 
    """

    bounce: bool
    bounced: bool
    dstAddress: typing.Optional[str]
    dstWorkchain: int
    indexInTransaction: int
    isOut: bool
    messageHash: str
    messageType: MessageType
    messageValue: int
    srcAddress: typing.Optional[str]
    srcWorkchain: int
    transactionHash: str
    transactionTime: int


class BlockResponse(_BaseModel):
    """
    Block response
    """

    accountBlocks: AccountBlocks
    blockInfo: BlockInfo
    fileHash: str
    genSoftwareVersion: int
    genUtime: int
    isKeyBlock: bool
    prev: PrevBlockId
    prevKeyBlock: int
    rootHash: str
    seqno: int
    shard: str
    shardRelations: ShardRelations
    shardsInfo: typing.Optional[list[ShardDescrInfoItem]]
    transactionCount: int
    valueFlow: ValueFlow
    workchain: int


class PrevBlockId(_BaseModel):
    pass


class ShardRelations(_BaseModel):
    leftChild: str
    parent: str
    rightChild: str


class ShardDescrInfoItem(_BaseModel):
    info: ShardDescrInfo
    shardIdent: ShardId


class ShardDescrInfo(_BaseModel):
    """
    Shard info description
    """

    beforeMerge: bool
    """
    Whether this shard is going to merge
    """
    beforeSplit: bool
    """
    Whether this shard is going to split
    """
    endLt: int
    """
    Logical time range upper bound
    """
    feesCollected: int
    """
    Total fees collected
    """
    fileHash: str
    """
    File hash of the latest block in this shard
    """
    flags: int
    """
    Shard flags
    """
    fundsCreated: int
    """
    Funds emission
    """
    genUtime: int
    """
    Unix timestamp of the latest block in shard
    """
    minRefMcSeqno: int
    """
    Minimal referenced masterchain block seqno
    """
    nextCatchainSeqno: int
    """
    Next catchain seqno
    """
    nextValidatorShard: str
    """
    Yes
    """
    nxCcUpdated: bool
    """
    Yes
    """
    regMcSeqno: int
    """
    Registration mc seqno
    """
    rootHash: str
    """
    Root hash of the latest block in this shard
    """
    seqNo: int
    """
    Latest block seqno
    """
    splitMergeAt: FutureSplitMerge
    startLt: int
    """
    Logical time range lower bound
    """
    wantMerge: bool
    """
    Whether this shard is ready to merge
    """
    wantSplit: bool
    """
    Whether this shard is ready to split
    """


class FutureSplitMerge(_BaseModel):
    pass


class ShardId(_BaseModel):
    shardPrefix: int
    wc: int


class ValueFlow(_BaseModel):
    """
    Block value flow
    """

    created: typing.Optional[int]
    """
    Value exported with external messages
    """
    exported: typing.Optional[int]
    """
    Value exported with external messages
    """
    feesCollected: typing.Optional[int]
    """
    Value exported with external messages
    """
    feesImported: typing.Optional[int]
    """
    Value exported with external messages
    """
    fromPrevBlk: typing.Optional[int]
    """
    Value from the previous block
    """
    imported: typing.Optional[int]
    """
    Value imported with external messages
    """
    minted: typing.Optional[int]
    """
    Value exported with external messages
    """
    recovered: typing.Optional[int]
    """
    Value exported with external messages
    """
    toNextBlk: typing.Optional[int]
    """
    Value to the next block
    """


class BlocksCountRequest(_BaseModel):
    """
    Blocks count request
    """

    genUtimeGe: typing.Optional[int]
    genUtimeLe: typing.Optional[int]
    seqnoGe: typing.Optional[int]
    seqnoLe: typing.Optional[int]
    shard: typing.Optional[int]
    transactionCountGe: typing.Optional[int]
    transactionCountLe: typing.Optional[int]
    workchain: typing.Optional[int]


class BlocksOrdering(_BaseModel):
    """
    Blocks ordering
    """

    column: BlockColumn
    direction: Direction


class BlocksRequest(_BaseModel):
    """
    Blocks request
    """

    genUtimeGe: typing.Optional[int]
    genUtimeLe: typing.Optional[int]
    limit: int
    offset: int
    ordering: typing.Optional[BlocksOrdering]
    seqnoGe: typing.Optional[int]
    seqnoLe: typing.Optional[int]
    shard: typing.Optional[str]
    transactionCountGe: typing.Optional[int]
    transactionCountLe: typing.Optional[int]
    workchain: typing.Optional[int]


class ConvertedAddressResponse(_BaseModel):
    """
    Different address representations
    """

    base64Bounceable: str
    base64NonBounceable: str
    base64UrlBounceable: str
    base64UrlNonBounceable: str
    unpacked: str


class CountResponse(_BaseModel):
    count: int


class CurrentElectionData(_BaseModel):
    """
    Current election info
    """

    electAt: int
    """
    Election start
    """
    electClose: int
    """
    Election end
    """
    failed: bool
    """
    Whether these elections were failed
    """
    finished: bool
    """
    Whether these elections were finished
    """
    members: list[ElectionMember]
    minStake: int
    """
    Minimal validator stake
    """
    totalStake: int
    """
    Total validator stakes
    """


class ElectionMember(_BaseModel):
    """
    Current election member
    """

    adnlAddr: str
    createdAt: int
    maxFactor: int
    msgValue: int
    pubkey: str
    srcAddr: str


class CurrentValidatorResponse(_BaseModel):
    """
    Current validator brief info
    """

    address: str
    bonuses: int
    weight: float


class ElectionBonusesResponse(_BaseModel):
    """
    Validator set bonuses
    """

    bonuses: int
    electionId: int


class ElectionsConfigResponse(_BaseModel):
    """
    Brief elector config
    """

    electionsEndBefore: int
    electionsStartBefore: int
    maxMainValidators: int
    maxStake: int
    maxStakeFactor: int
    maxValidators: int
    minStake: int
    minTotalStake: int
    minValidators: int
    stakeHeldFor: int
    validatorsElectedFor: int


class ElectorDataResponse(_BaseModel):
    """
    Elector data
    """

    activeHash: str
    """
    Active validator set hash
    """
    activeId: int
    """
    Active election id
    """
    currentElection: CurrentElectionData
    pastElections: list[PastElectionData]


class PastElectionData(_BaseModel):
    """
    Past election info
    """

    bonuses: int
    """
    Total bonuses received by this validator set
    """
    electionId: int
    """
    Election ID
    """
    frozenDict: list[FrozenStake]
    stakeHeld: int
    """
    Stake freeze duration
    """
    totalStake: int
    """
    Total validator stakes
    """
    unfreezeAt: int
    """
    Time of stakes unfreeze
    """
    vsetHash: str
    """
    Validator set hash
    """


class FrozenStake(_BaseModel):
    addr: str
    pubkey: str
    stake: int
    weight: int


class ExactBlockRequest(_BaseModel):
    """
    Request entity by hash
    """

    pass


class HashRequest(_BaseModel):
    """
    Request entity by hash
    """

    id: str


class MessageOccurrenceResponse(_BaseModel):
    """
    Message occurrence in transaction
    """

    indexInTransaction: int
    isOut: bool
    transactionHash: str
    transactionTime: int


class MessageReferenceResponse(_BaseModel):
    """
    Message reference
    """

    createdAt: int
    dstAddress: typing.Optional[str]
    dstWorkchain: int
    messageHash: str
    messageType: MessageType
    messageValue: int
    srcAddress: typing.Optional[str]
    srcWorkchain: int


class MessageResponse(_BaseModel):
    """
    Message response
    """

    body: typing.Optional[str]
    bounce: bool
    bounced: bool
    createdAt: int
    createdLt: int
    dstAddress: typing.Optional[str]
    dstWorkchain: int
    fwdFee: int
    ihrFee: int
    importFee: int
    messageHash: str
    messageType: MessageType
    messageValue: int
    srcAddress: typing.Optional[str]
    srcWorkchain: int
    stateInit: typing.Optional[str]


class MessagesCountRequest(_BaseModel):
    """
    Messages count request
    """

    block: typing.Optional[str]
    excludeAccounts: typing.Optional[list[Address]]
    excludeDstAccounts: typing.Optional[list[Address]]
    excludeSrcAccounts: typing.Optional[list[Address]]
    includeAccounts: typing.Optional[list[Address]]
    includeDstAccounts: typing.Optional[list[Address]]
    includeSrcAccounts: typing.Optional[list[Address]]
    messageTypes: typing.Optional[list[MessageType]]
    messageValueGe: typing.Optional[int]
    messageValueLe: typing.Optional[int]
    transactionTimeGe: typing.Optional[int]
    transactionTimeLe: typing.Optional[int]


class MessagesOrdering(_BaseModel):
    """
    Messages ordering
    """

    column: MessageColumn
    direction: Direction


class MessagesRequest(_BaseModel):
    """
    Messages request
    """

    block: typing.Optional[str]
    excludeAccounts: typing.Optional[list[Address]]
    excludeDstAccounts: typing.Optional[list[Address]]
    excludeSrcAccounts: typing.Optional[list[Address]]
    includeAccounts: typing.Optional[list[Address]]
    includeDstAccounts: typing.Optional[list[Address]]
    includeSrcAccounts: typing.Optional[list[Address]]
    limit: int
    messageTypes: typing.Optional[list[MessageType]]
    messageValueGe: typing.Optional[int]
    messageValueLe: typing.Optional[int]
    offset: int
    ordering: typing.Optional[MessagesOrdering]
    transactionTimeGe: typing.Optional[int]
    transactionTimeLe: typing.Optional[int]


class MessageWithoutDataResponse(_BaseModel):
    """
    Message response
    """

    bounce: bool
    bounced: bool
    createdAt: int
    createdLt: int
    dstAddress: typing.Optional[str]
    dstWorkchain: int
    fwdFee: int
    ihrFee: int
    importFee: int
    messageHash: str
    messageType: MessageType
    messageValue: int
    srcAddress: typing.Optional[str]
    srcWorkchain: int


class SearchMatchResponse(_BaseModel):
    """
    Message response
    """

    data: typing.Union[
        BlockBriefResponse, MessageReferenceResponse, TransactionReferenceResponse, AccountReferenceResponse]
    """
    Message response
    """
    kind: str
    """
    SearchMatchResponse type variant
    """


class TransactionReferenceResponse(_BaseModel):
    """
    Transaction reference
    """

    accountId: str
    hash: str
    time: int
    txType: TransactionType
    workchain: int


class SearchRequest(_BaseModel):
    """
    Search request
    """

    query: str


class StorageUsedShort(_BaseModel):
    bits: int
    cells: int


class TransactionActionPhase(_BaseModel):
    actionListHash: str
    msgsCreated: int
    noFunds: bool
    resultArg: typing.Optional[int]
    resultCode: int
    skippedActions: int
    specActions: int
    statusChange: AccountStatusChange
    success: bool
    totActions: int
    totalActionFees: int
    totalFwdFees: int
    totMsgSize: StorageUsedShort
    valid: bool


class TransactionBouncePhase(_BaseModel):
    pass


class TransactionBriefResponse(_BaseModel):
    """
    Transactions Info Response 
    """

    aborted: bool
    accountId: str
    balanceChange: str
    blockHash: str
    blockSeqno: int
    blockShard: str
    exitCode: typing.Optional[int]
    hash: str
    lt: str
    resultCode: typing.Optional[int]
    time: int
    txType: TransactionType
    workchain: int


class TransactionComputePhase(_BaseModel):
    pass


class TransactionCreditPhase(_BaseModel):
    credit: int
    dueFeesCollected: int


class TransactionDescription(_BaseModel):
    pass


class TransactionResponse(_BaseModel):
    """
    Transactions With Messages Response 
    """

    aborted: bool
    accountId: str
    balanceChange: int
    blockHash: str
    blockSeqno: int
    blockShard: str
    description: TransactionDescription
    destroyed: bool
    endStatus: TransactionAccountStatus
    hash: str
    inMessage: typing.Optional[MessageWithoutDataResponse]
    lt: int
    newHash: str
    oldHash: str
    origStatus: TransactionAccountStatus
    outMessages: list[MessageWithoutDataResponse]
    prevTransactionHash: str
    prevTransactionLt: int
    time: int
    totalFees: int
    workchain: int


class TransactionsOrdering(_BaseModel):
    """
    Transactions ordering
    """

    column: TransactionColumn
    direction: Direction


class TransactionsRequest(_BaseModel):
    """
    Transactions request
    """

    balanceChangeGe: typing.Optional[int]
    balanceChangeLe: typing.Optional[int]
    block: typing.Optional[str]
    excludeAccounts: typing.Optional[list[Address]]
    includeAccounts: typing.Optional[list[Address]]
    limit: int
    offset: int
    ordering: typing.Optional[TransactionsOrdering]
    timeGe: typing.Optional[int]
    timeLe: typing.Optional[int]
    txTypes: typing.Optional[list[TransactionType]]
    workchain: typing.Optional[int]


class TransactionStoragePhase(_BaseModel):
    statusChange: AccountStatusChange
    storageFeesCollected: int
    storageFeesDue: int


AccountByIdRequest.update_forward_refs()
AccountReferenceResponse.update_forward_refs()
AccountsOrdering.update_forward_refs()
AccountStateResponse.update_forward_refs()
BlockInfo.update_forward_refs()
BlockMessagesResponse.update_forward_refs()
BlockResponse.update_forward_refs()
CurrentElectionData.update_forward_refs()
ElectorDataResponse.update_forward_refs()
SearchMatchResponse.update_forward_refs()
