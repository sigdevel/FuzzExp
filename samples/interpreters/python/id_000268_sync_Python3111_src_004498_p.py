import json
import math
import pytest
from random import (
    randint,
)
from typing import (
    TYPE_CHECKING,
    Callable,
    Union,
    cast,
)

from eth_typing import (
    BlockNumber,
    ChecksumAddress,
    HexAddress,
    HexStr,
)
from eth_utils import (
    is_boolean,
    is_bytes,
    is_checksum_address,
    is_dict,
    is_integer,
    is_list_like,
    is_same_address,
    is_string,
)
from eth_utils.toolz import (
    assoc,
)
from hexbytes import (
    HexBytes,
)

from web3._utils.empty import (
    empty,
)
from web3._utils.ens import (
    ens_addresses,
)
from web3._utils.method_formatters import (
    to_hex_if_integer,
)
from web3._utils.module_testing.module_testing_utils import (
    assert_contains_log,
    async_mock_offchain_lookup_request_response,
    mine_pending_block,
    mock_offchain_lookup_request_response,
)
from web3._utils.type_conversion import (
    to_hex_if_bytes,
)
from web3.exceptions import (
    BlockNotFound,
    ContractLogicError,
    InvalidAddress,
    InvalidTransaction,
    MultipleFailedRequests,
    NameNotFound,
    OffchainLookup,
    TimeExhausted,
    TooManyRequests,
    TransactionNotFound,
    TransactionTypeMismatch,
    ValidationError,
)
from web3.middleware import (
    async_geth_poa_middleware,
)
from web3.middleware.fixture import (
    async_construct_error_generator_middleware,
    async_construct_result_generator_middleware,
    construct_error_generator_middleware,
)
from web3.types import (  
    ENS,
    BlockData,
    FilterParams,
    LogReceipt,
    Nonce,
    RPCEndpoint,
    SyncStatus,
    TxParams,
    Wei,
)

UNKNOWN_ADDRESS = ChecksumAddress(
    HexAddress(HexStr("0xdEADBEeF00000000000000000000000000000000"))
)

UNKNOWN_HASH = HexStr(
    "0xdeadbeef00000000000000000000000000000000000000000000000000000000"
)
"test offchain lookup" as an abi-encoded string
OFFCHAIN_LOOKUP_TEST_DATA = "0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001474657374206f6666636861696e206c6f6f6b7570000000000000000000000000"  
"web3py" as an abi-encoded string
WEB3PY_AS_HEXBYTES = "0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000067765623370790000000000000000000000000000000000000000000000000000"  

if TYPE_CHECKING:
    from web3 import Web3  
    from web3.contract import Contract  
    from _pytest.monkeypatch import MonkeyPatch  


class AsyncEthModuleTest:
    @pytest.mark.asyncio
    async def test_eth_gas_price(self, async_w3: "Web3") -> None:
        gas_price = await async_w3.eth.gas_price  
        assert gas_price > 0

    @pytest.mark.asyncio
    async def test_is_connected(self, async_w3: "Web3") -> None:
        is_connected = await async_w3.is_connected()  
        assert is_connected is True

    @pytest.mark.asyncio
    async def test_eth_send_transaction_legacy(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": await async_w3.eth.gas_price,  
        }
        txn_hash = await async_w3.eth.send_transaction(txn_params)  
        txn = await async_w3.eth.get_transaction(txn_hash)  

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["gasPrice"] == txn_params["gasPrice"]

    @pytest.mark.asyncio
    async def test_eth_send_transaction(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": async_w3.to_wei(3, "gwei"),
            "maxPriorityFeePerGas": async_w3.to_wei(1, "gwei"),
        }
        txn_hash = await async_w3.eth.send_transaction(txn_params)  
        txn = await async_w3.eth.get_transaction(txn_hash)  

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["maxFeePerGas"] == txn_params["maxFeePerGas"]
        assert txn["maxPriorityFeePerGas"] == txn_params["maxPriorityFeePerGas"]
        assert txn["gasPrice"] == txn_params["maxFeePerGas"]

    @pytest.mark.asyncio
    async def test_eth_send_transaction_default_fees(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
        }
        txn_hash = await async_w3.eth.send_transaction(txn_params)  
        txn = await async_w3.eth.get_transaction(txn_hash)  

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["maxPriorityFeePerGas"] == 1 * 10**9
        assert txn["maxFeePerGas"] >= 1 * 10**9
        assert txn["gasPrice"] == txn["maxFeePerGas"]

    @pytest.mark.asyncio
    async def test_eth_send_transaction_hex_fees(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": hex(250 * 10**9),
            "maxPriorityFeePerGas": hex(2 * 10**9),
        }
        txn_hash = await async_w3.eth.send_transaction(txn_params)  
        txn = await async_w3.eth.get_transaction(txn_hash)  

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["maxFeePerGas"] == 250 * 10**9
        assert txn["maxPriorityFeePerGas"] == 2 * 10**9

    @pytest.mark.asyncio
    async def test_eth_send_transaction_no_gas(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "maxFeePerGas": Wei(250 * 10**9),
            "maxPriorityFeePerGas": Wei(2 * 10**9),
        }
        txn_hash = await async_w3.eth.send_transaction(txn_params)  
        txn = await async_w3.eth.get_transaction(txn_hash)  

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 121000  

    @pytest.mark.asyncio
    async def test_eth_send_transaction_with_gas_price(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": Wei(1),
            "maxFeePerGas": Wei(250 * 10**9),
            "maxPriorityFeePerGas": Wei(2 * 10**9),
        }
        with pytest.raises(TransactionTypeMismatch):
            await async_w3.eth.send_transaction(txn_params)  

    @pytest.mark.asyncio
    async def test_eth_send_transaction_no_priority_fee(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": Wei(250 * 10**9),
        }
        with pytest.raises(
            InvalidTransaction, match="maxPriorityFeePerGas must be defined"
        ):
            await async_w3.eth.send_transaction(txn_params)  

    @pytest.mark.asyncio
    async def test_eth_send_transaction_no_max_fee(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        maxPriorityFeePerGas = async_w3.to_wei(2, "gwei")
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxPriorityFeePerGas": maxPriorityFeePerGas,
        }
        txn_hash = await async_w3.eth.send_transaction(txn_params)  
        txn = await async_w3.eth.get_transaction(txn_hash)  

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000

        block = await async_w3.eth.get_block("latest")  
        assert txn["maxFeePerGas"] == maxPriorityFeePerGas + 2 * block["baseFeePerGas"]

    @pytest.mark.asyncio
    async def test_eth_send_transaction_max_fee_less_than_tip(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": Wei(1 * 10**9),
            "maxPriorityFeePerGas": Wei(2 * 10**9),
        }
        with pytest.raises(
            InvalidTransaction, match="maxFeePerGas must be >= maxPriorityFeePerGas"
        ):
            await async_w3.eth.send_transaction(txn_params)  

    @pytest.mark.asyncio
    async def test_validation_middleware_chain_id_mismatch(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        wrong_chain_id = 1234567890
        actual_chain_id = await async_w3.eth.chain_id  

        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": Wei(21000),
            "maxFeePerGas": async_w3.to_wei(2, "gwei"),
            "maxPriorityFeePerGas": async_w3.to_wei(1, "gwei"),
            "chainId": wrong_chain_id,
        }
        with pytest.raises(
            ValidationError,
            match=f"The transaction declared chain ID {wrong_chain_id}, "
            f"but the connected node is on {actual_chain_id}",
        ):
            await async_w3.eth.send_transaction(txn_params)  

    @pytest.mark.asyncio
    async def test_geth_poa_middleware(self, async_w3: "Web3") -> None:
        return_block_with_long_extra_data = (
            await async_construct_result_generator_middleware(
                {
                    RPCEndpoint("eth_getBlockByNumber"): lambda *_: {
                        "extraData": "0x" + "ff" * 33
                    },
                }
            )
        )
        async_w3.middleware_onion.inject(async_geth_poa_middleware, "poa", layer=0)
        async_w3.middleware_onion.inject(
            return_block_with_long_extra_data, "extradata", layer=0
        )
        block = await async_w3.eth.get_block("latest")  
        assert "extraData" not in block
        assert block.proofOfAuthorityData == b"\xff" * 33

        
        async_w3.middleware_onion.remove("poa")
        async_w3.middleware_onion.remove("extradata")

    @pytest.mark.asyncio
    async def test_eth_send_raw_transaction(self, async_w3: "Web3") -> None:
        
        
        
        
        
        
        raw_txn = HexBytes(
            "0xf8650180825208940000000000000000000000000000000000000000808086eecac466e115a0ffdd42d7dee4ac85427468bc616812e49432e285e4e8f5cd9381163ac3b28108a04ec6b0d89ecbd5e89b0399f336ad50f283fafd70e86593250bf5a2adfb93d17e"  
        )
        expected_hash = HexStr(
            "0x52b0ff9cb472f25872fa8ec6a62fa59454fc2ae7901cfcc6cc89d096f49b8fc1"
        )
        txn_hash = await async_w3.eth.send_raw_transaction(raw_txn)  
        assert txn_hash == async_w3.to_bytes(hexstr=expected_hash)

    @pytest.mark.asyncio
    async def test_gas_price_strategy_middleware(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
        }
        two_gwei_in_wei = async_w3.to_wei(2, "gwei")

        def gas_price_strategy(w3: "Web3", txn: TxParams) -> Wei:
            return two_gwei_in_wei

        async_w3.eth.set_gas_price_strategy(gas_price_strategy)

        txn_hash = await async_w3.eth.send_transaction(txn_params)  
        txn = await async_w3.eth.get_transaction(txn_hash)  

        assert txn["gasPrice"] == two_gwei_in_wei
        async_w3.eth.set_gas_price_strategy(None)  

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "max_fee", (1000000000, None), ids=["with_max_fee", "without_max_fee"]
    )
    async def test_gas_price_from_strategy_bypassed_for_dynamic_fee_txn(
        self,
        async_w3: "Web3",
        unlocked_account_dual_type: ChecksumAddress,
        max_fee: Wei,
    ) -> None:
        max_priority_fee = async_w3.to_wei(1, "gwei")
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxPriorityFeePerGas": max_priority_fee,
        }
        if max_fee is not None:
            txn_params = assoc(txn_params, "maxFeePerGas", max_fee)

        def gas_price_strategy(w3: "Web3", txn: TxParams) -> Wei:
            return async_w3.to_wei(2, "gwei")

        async_w3.eth.set_gas_price_strategy(gas_price_strategy)

        txn_hash = await async_w3.eth.send_transaction(txn_params)  
        txn = await async_w3.eth.get_transaction(txn_hash)  

        latest_block = await async_w3.eth.get_block("latest")  
        assert (
            txn["maxFeePerGas"] == max_fee
            if max_fee is not None
            else 2 * latest_block["baseFeePerGas"] + max_priority_fee
        )
        assert txn["maxPriorityFeePerGas"] == max_priority_fee
        assert txn["gasPrice"] == txn["maxFeePerGas"]

        async_w3.eth.set_gas_price_strategy(None)  

    @pytest.mark.asyncio
    async def test_gas_price_from_strategy_bypassed_for_dynamic_fee_txn_no_tip(
        self,
        async_w3: "Web3",
        unlocked_account_dual_type: ChecksumAddress,
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": Wei(1000000000),
        }

        def gas_price_strategy(_w3: "Web3", _txn: TxParams) -> Wei:
            return async_w3.to_wei(2, "gwei")

        async_w3.eth.set_gas_price_strategy(gas_price_strategy)

        with pytest.raises(
            InvalidTransaction, match="maxPriorityFeePerGas must be defined"
        ):
            await async_w3.eth.send_transaction(txn_params)  

        async_w3.eth.set_gas_price_strategy(None)  

    @pytest.mark.asyncio
    async def test_eth_estimate_gas(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        gas_estimate = await async_w3.eth.estimate_gas(
            {  
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
            }
        )
        assert is_integer(gas_estimate)
        assert gas_estimate > 0

    @pytest.mark.asyncio
    async def test_eth_fee_history(self, async_w3: "Web3") -> None:
        fee_history = await async_w3.eth.fee_history(1, "latest", [50])  
        assert is_list_like(fee_history["baseFeePerGas"])
        assert is_list_like(fee_history["gasUsedRatio"])
        assert is_integer(fee_history["oldestBlock"])
        assert fee_history["oldestBlock"] >= 0
        assert is_list_like(fee_history["reward"])
        assert is_list_like(fee_history["reward"][0])

    @pytest.mark.asyncio
    async def test_eth_fee_history_with_integer(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        fee_history = await async_w3.eth.fee_history(  
            1, empty_block["number"], [50]
        )
        assert is_list_like(fee_history["baseFeePerGas"])
        assert is_list_like(fee_history["gasUsedRatio"])
        assert is_integer(fee_history["oldestBlock"])
        assert fee_history["oldestBlock"] >= 0
        assert is_list_like(fee_history["reward"])
        assert is_list_like(fee_history["reward"][0])

    @pytest.mark.asyncio
    async def test_eth_fee_history_no_reward_percentiles(
        self, async_w3: "Web3"
    ) -> None:
        fee_history = await async_w3.eth.fee_history(1, "latest")  
        assert is_list_like(fee_history["baseFeePerGas"])
        assert is_list_like(fee_history["gasUsedRatio"])
        assert is_integer(fee_history["oldestBlock"])
        assert fee_history["oldestBlock"] >= 0

    @pytest.mark.asyncio
    async def test_eth_max_priority_fee(self, async_w3: "Web3") -> None:
        max_priority_fee = await async_w3.eth.max_priority_fee  
        assert is_integer(max_priority_fee)

    @pytest.mark.asyncio
    async def test_eth_max_priority_fee_with_fee_history_calculation(
        self, async_w3: "Web3"
    ) -> None:
        fail_max_prio_middleware = await async_construct_error_generator_middleware(
            {RPCEndpoint("eth_maxPriorityFeePerGas"): lambda *_: ""}
        )
        async_w3.middleware_onion.add(
            fail_max_prio_middleware, name="fail_max_prio_middleware"
        )

        with pytest.warns(
            UserWarning,
            match="There was an issue with the method eth_maxPriorityFeePerGas. "
            "Calculating using eth_feeHistory.",
        ):
            max_priority_fee = await async_w3.eth.max_priority_fee  
            assert is_integer(max_priority_fee)

        async_w3.middleware_onion.remove("fail_max_prio_middleware")  

    @pytest.mark.asyncio
    async def test_eth_getBlockByHash(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        block = await async_w3.eth.get_block(empty_block["hash"])  
        assert block["hash"] == empty_block["hash"]

    @pytest.mark.asyncio
    async def test_eth_getBlockByHash_not_found(self, async_w3: "Web3") -> None:
        with pytest.raises(BlockNotFound):
            await async_w3.eth.get_block(UNKNOWN_HASH)  

    @pytest.mark.asyncio
    async def test_eth_getBlockByHash_pending(self, async_w3: "Web3") -> None:
        block = await async_w3.eth.get_block("pending")  
        assert block["hash"] is None

    @pytest.mark.asyncio
    async def test_eth_getBlockByNumber_with_integer(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        block = await async_w3.eth.get_block(empty_block["number"])  
        assert block["number"] == empty_block["number"]

    @pytest.mark.asyncio
    async def test_eth_getBlockByNumber_latest(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        current_block_number = await async_w3.eth.block_number  
        block = await async_w3.eth.get_block("latest")  
        assert block["number"] == current_block_number

    @pytest.mark.asyncio
    async def test_eth_getBlockByNumber_not_found(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        with pytest.raises(BlockNotFound):
            await async_w3.eth.get_block(BlockNumber(12345))  

    @pytest.mark.asyncio
    async def test_eth_getBlockByNumber_pending(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        current_block_number = await async_w3.eth.block_number  
        block = await async_w3.eth.get_block("pending")  
        assert block["number"] == current_block_number + 1

    @pytest.mark.asyncio
    async def test_eth_getBlockByNumber_earliest(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        genesis_block = await async_w3.eth.get_block(BlockNumber(0))  
        block = await async_w3.eth.get_block("earliest")  
        assert block["number"] == 0
        assert block["hash"] == genesis_block["hash"]

    @pytest.mark.asyncio
    @pytest.mark.xfail(reason="Integration test suite not yet set up for PoS")
    async def test_eth_getBlockByNumber_safe(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        block = await async_w3.eth.get_block("safe")  
        assert block is not None
        assert isinstance(block["number"], int)

    @pytest.mark.asyncio
    @pytest.mark.xfail(reason="Integration test suite not yet set up for PoS")
    async def test_eth_getBlockByNumber_finalized(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        block = await async_w3.eth.get_block("finalized")  
        assert block is not None
        assert isinstance(block["number"], int)

    @pytest.mark.asyncio
    async def test_eth_getBlockByNumber_full_transactions(
        self, async_w3: "Web3", block_with_txn: BlockData
    ) -> None:
        block = await async_w3.eth.get_block(  
            block_with_txn["number"], True
        )
        transaction = block["transactions"][0]
        assert transaction["hash"] == block_with_txn["transactions"][0]

    @pytest.mark.asyncio
    async def test_eth_get_raw_transaction(
        self, async_w3: "Web3", mined_txn_hash: HexStr
    ) -> None:
        raw_transaction = await async_w3.eth.get_raw_transaction(  
            mined_txn_hash
        )
        assert is_bytes(raw_transaction)

    @pytest.mark.asyncio
    async def test_eth_get_raw_transaction_raises_error(self, async_w3: "Web3") -> None:
        with pytest.raises(
            TransactionNotFound, match=f"Transaction with hash: '{UNKNOWN_HASH}'"
        ):
            await async_w3.eth.get_raw_transaction(UNKNOWN_HASH)  

    @pytest.mark.asyncio
    async def test_eth_get_raw_transaction_by_block(
        self,
        async_w3: "Web3",
        block_with_txn: BlockData,
        unlocked_account_dual_type: ChecksumAddress,
    ) -> None:
        
        
        await async_w3.eth.send_transaction(  
            {
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
            }
        )
        pending_block = await async_w3.eth.get_block("pending")  
        last_pending_txn_index = len(pending_block["transactions"]) - 1
        raw_txn = await async_w3.eth.get_raw_transaction_by_block(  
            "pending", last_pending_txn_index
        )
        assert is_bytes(raw_txn)

        
        block_with_txn_number = block_with_txn["number"]
        raw_transaction = await async_w3.eth.get_raw_transaction_by_block(  
            block_with_txn_number, 0
        )
        assert is_bytes(raw_transaction)

        
        block_with_txn_hash = block_with_txn["hash"]
        raw_transaction = await async_w3.eth.get_raw_transaction_by_block(  
            block_with_txn_hash, 0
        )
        assert is_bytes(raw_transaction)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("unknown_block_num_or_hash", (1234567899999, UNKNOWN_HASH))
    async def test_eth_get_raw_transaction_by_block_raises_error(
        self, async_w3: "Web3", unknown_block_num_or_hash: Union[int, HexBytes]
    ) -> None:
        with pytest.raises(
            TransactionNotFound,
            match=(
                f"Transaction index: 0 on block id: "
                f"{to_hex_if_integer(unknown_block_num_or_hash)!r} "
                f"not found."
            ),
        ):
            await async_w3.eth.get_raw_transaction_by_block(  
                unknown_block_num_or_hash, 0
            )

    @pytest.mark.asyncio
    async def test_eth_get_raw_transaction_by_block_raises_error_block_identifier(
        self, async_w3: "Web3"
    ) -> None:
        unknown_identifier = "unknown"
        with pytest.raises(
            ValueError,
            match=(
                "Value did not match any of the recognized block identifiers: "
                f"{unknown_identifier}"
            ),
        ):
            await async_w3.eth.get_raw_transaction_by_block(
                unknown_identifier, 0  
            )

    @pytest.mark.asyncio
    async def test_eth_get_balance(self, async_w3: "Web3") -> None:
        coinbase = await async_w3.eth.coinbase  

        with pytest.raises(InvalidAddress):
            await async_w3.eth.get_balance(  
                ChecksumAddress(HexAddress(HexStr(coinbase.lower())))
            )

        balance = await async_w3.eth.get_balance(coinbase)  

        assert is_integer(balance)
        assert balance >= 0

    @pytest.mark.asyncio
    async def test_eth_get_code(
        self, async_w3: "Web3", math_contract_address: ChecksumAddress
    ) -> None:
        code = await async_w3.eth.get_code(math_contract_address)  
        assert isinstance(code, HexBytes)
        assert len(code) > 0

    @pytest.mark.asyncio
    async def test_eth_get_code_invalid_address(
        self, async_w3: "Web3", math_contract: "Contract"
    ) -> None:
        with pytest.raises(InvalidAddress):
            await async_w3.eth.get_code(  
                ChecksumAddress(HexAddress(HexStr(math_contract.address.lower())))
            )

    @pytest.mark.asyncio
    async def test_eth_get_code_with_block_identifier(
        self, async_w3: "Web3", emitter_contract: "Contract"
    ) -> None:
        block_id = await async_w3.eth.block_number  
        code = await async_w3.eth.get_code(  
            emitter_contract.address, block_id
        )
        assert isinstance(code, HexBytes)
        assert len(code) > 0

    @pytest.mark.asyncio
    async def test_eth_get_transaction_count(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        transaction_count = await async_w3.eth.get_transaction_count(unlocked_account_dual_type)  
        assert is_integer(transaction_count)
        assert transaction_count >= 0

    @pytest.mark.asyncio
    async def test_eth_call(self, async_w3: "Web3", math_contract: "Contract") -> None:
        coinbase = await async_w3.eth.coinbase  
        txn_params = math_contract._prepare_transaction(
            fn_name="add",
            fn_args=(7, 11),
            transaction={"from": coinbase, "to": math_contract.address},
        )
        call_result = await async_w3.eth.call(txn_params)  
        assert is_string(call_result)
        (result,) = async_w3.codec.decode(["uint256"], call_result)
        assert result == 18

    @pytest.mark.asyncio
    async def test_eth_call_with_override(
        self, async_w3: "Web3", revert_contract: "Contract"
    ) -> None:
        coinbase = await async_w3.eth.coinbase  
        txn_params = revert_contract._prepare_transaction(
            fn_name="normalFunction",
            transaction={"from": coinbase, "to": revert_contract.address},
        )
        call_result = await async_w3.eth.call(txn_params)  
        (result,) = async_w3.codec.decode(["bool"], call_result)
        assert result is True

        
        override_code = HexStr(
            "0x6080604052348015600f57600080fd5b5060043610603c5760003560e01c8063185c38a4146041578063c06a97cb146049578063d67e4b84146051575b600080fd5b60476071565b005b604f60df565b005b605760e4565b604051808215151515815260200191505060405180910390f35b6040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601b8152602001807f46756e6374696f6e20686173206265656e2072657665727465642e000000000081525060200191505060405180910390fd5b600080fd5b60008090509056fea2646970667358221220bb71e9e9a2e271cd0fbe833524a3ea67df95f25ea13aef5b0a761fa52b538f1064736f6c63430006010033"  
        )
        call_result = await async_w3.eth.call(  
            txn_params, "latest", {revert_contract.address: {"code": override_code}}
        )
        (result,) = async_w3.codec.decode(["bool"], call_result)
        assert result is False

    @pytest.mark.asyncio
    async def test_eth_call_with_0_result(
        self, async_w3: "Web3", math_contract: "Contract"
    ) -> None:
        coinbase = await async_w3.eth.coinbase  
        txn_params = math_contract._prepare_transaction(
            fn_name="add",
            fn_args=(0, 0),
            transaction={"from": coinbase, "to": math_contract.address},
        )
        call_result = await async_w3.eth.call(txn_params)  
        assert is_string(call_result)
        (result,) = async_w3.codec.decode(["uint256"], call_result)
        assert result == 0

    @pytest.mark.asyncio
    async def test_eth_call_revert_with_msg(
        self,
        async_w3: "Web3",
        revert_contract: "Contract",
        unlocked_account: ChecksumAddress,
    ) -> None:
        with pytest.raises(
            ContractLogicError, match="execution reverted: Function has been reverted"
        ):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            await async_w3.eth.call(txn_params)  

    @pytest.mark.asyncio
    async def test_eth_call_revert_without_msg(
        self,
        async_w3: "Web3",
        revert_contract: "Contract",
        unlocked_account: ChecksumAddress,
    ) -> None:
        with pytest.raises(ContractLogicError, match="execution reverted"):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithoutMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            await async_w3.eth.call(txn_params)  

    @pytest.mark.asyncio
    async def test_eth_call_offchain_lookup(
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            async_offchain_lookup_contract.address
        ).lower()

        async_mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_json_data=WEB3PY_AS_HEXBYTES,
        )
        response_caller = await async_offchain_lookup_contract.caller().testOffchainLookup(  
            OFFCHAIN_LOOKUP_TEST_DATA
        )
        response_function_call = await async_offchain_lookup_contract.functions.testOffchainLookup(  
            OFFCHAIN_LOOKUP_TEST_DATA
        ).call()
        assert async_w3.codec.decode(["string"], response_caller)[0] == "web3py"
        assert async_w3.codec.decode(["string"], response_function_call)[0] == "web3py"

    @pytest.mark.asyncio
    async def test_eth_call_offchain_lookup_raises_when_ccip_read_is_disabled(
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
    ) -> None:
        
        with pytest.raises(OffchainLookup):
            await async_offchain_lookup_contract.caller(
                ccip_read_enabled=False
            ).testOffchainLookup(  
                OFFCHAIN_LOOKUP_TEST_DATA
            )

        
        with pytest.raises(OffchainLookup):
            await async_offchain_lookup_contract.functions.testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            ).call(ccip_read_enabled=False)

        
        async_w3.provider.global_ccip_read_enabled = False

        with pytest.raises(OffchainLookup):
            await async_offchain_lookup_contract.functions.testOffchainLookup(  
                OFFCHAIN_LOOKUP_TEST_DATA
            ).call()

        async_w3.provider.global_ccip_read_enabled = True  

    @pytest.mark.asyncio
    async def test_eth_call_offchain_lookup_call_flag_overrides_provider_flag(
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            async_offchain_lookup_contract.address
        ).lower()

        async_mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_json_data=WEB3PY_AS_HEXBYTES,
        )

        async_w3.provider.global_ccip_read_enabled = False

        response = await async_offchain_lookup_contract.functions.testOffchainLookup(
            
            OFFCHAIN_LOOKUP_TEST_DATA
        ).call(ccip_read_enabled=True)
        assert async_w3.codec.decode(["string"], response)[0] == "web3py"

        async_w3.provider.global_ccip_read_enabled = True  

    @pytest.mark.asyncio
    @pytest.mark.parametrize("max_redirects", range(-1, 4))
    async def test_eth_call_offchain_lookup_raises_if_max_redirects_is_less_than_4(
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
        max_redirects: int,
    ) -> None:
        default_max_redirects = async_w3.provider.ccip_read_max_redirects

        async_w3.provider.ccip_read_max_redirects = max_redirects
        with pytest.raises(ValueError, match="at least 4"):
            await async_offchain_lookup_contract.caller().testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            )

        async_w3.provider.ccip_read_max_redirects = default_max_redirects  

    @pytest.mark.asyncio
    async def test_eth_call_offchain_lookup_raises_for_improperly_formatted_rest_request_response(  
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            async_offchain_lookup_contract.address
        ).lower()

        async_mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_json_data=WEB3PY_AS_HEXBYTES,
            json_data_field="not_data",
        )
        with pytest.raises(ValidationError, match="missing 'data' field"):
            await async_offchain_lookup_contract.caller().testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code_non_4xx_error", [100, 300, 500, 600])
    async def test_eth_call_offchain_lookup_tries_next_url_for_non_4xx_error_status_and_tests_POST(  
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
        status_code_non_4xx_error: int,
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            async_offchain_lookup_contract.address
        ).lower()

        
        
        
        
        
        async_mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_status_code=status_code_non_4xx_error,
            mocked_json_data=WEB3PY_AS_HEXBYTES,
        )
        async_mock_offchain_lookup_request_response(
            monkeypatch,
            http_method="POST",
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}.json",  
            mocked_status_code=200,
            mocked_json_data=WEB3PY_AS_HEXBYTES,
            sender=normalized_contract_address,
            calldata=OFFCHAIN_LOOKUP_TEST_DATA,
        )
        response = await async_offchain_lookup_contract.caller().testOffchainLookup(
            OFFCHAIN_LOOKUP_TEST_DATA
        )
        assert async_w3.codec.decode(["string"], response)[0] == "web3py"

    @pytest.mark.asyncio
    async def test_eth_call_offchain_lookup_calls_raise_for_status_for_4xx_status_code(
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            async_offchain_lookup_contract.address
        ).lower()

        async_mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_status_code=randint(400, 499),
            mocked_json_data=WEB3PY_AS_HEXBYTES,
        )
        with pytest.raises(Exception, match="called raise_for_status\\(\\)"):
            await async_offchain_lookup_contract.caller().testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            )

    @pytest.mark.asyncio
    async def test_eth_call_offchain_lookup_raises_when_all_supplied_urls_fail(
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
    ) -> None:
        
        with pytest.raises(
            MultipleFailedRequests, match="Offchain lookup failed for supplied urls"
        ):
            await async_offchain_lookup_contract.caller().testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            )

    @pytest.mark.asyncio
    async def test_eth_call_continuous_offchain_lookup_raises_with_too_many_requests(
        self,
        async_w3: "Web3",
        async_offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            async_offchain_lookup_contract.address
        ).lower()

        async_mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/0x.json",  
        )
        with pytest.raises(TooManyRequests, match="Too many CCIP read redirects"):
            await async_offchain_lookup_contract.caller().continuousOffchainLookup()  

    @pytest.mark.asyncio
    async def test_async_eth_hashrate(self, async_w3: "Web3") -> None:
        hashrate = await async_w3.eth.hashrate  
        assert is_integer(hashrate)
        assert hashrate >= 0

    @pytest.mark.asyncio
    async def test_async_eth_chain_id(self, async_w3: "Web3") -> None:
        chain_id = await async_w3.eth.chain_id  
        
        assert chain_id == 131277322940537

    @pytest.mark.asyncio
    async def test_async_eth_mining(self, async_w3: "Web3") -> None:
        mining = await async_w3.eth.mining  
        assert is_boolean(mining)

    @pytest.mark.asyncio
    async def test_async_eth_get_transaction_receipt_mined(
        self, async_w3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        receipt = await async_w3.eth.get_transaction_receipt(  
            mined_txn_hash
        )
        assert is_dict(receipt)
        assert receipt["blockNumber"] == block_with_txn["number"]
        assert receipt["blockHash"] == block_with_txn["hash"]
        assert receipt["transactionIndex"] == 0
        assert receipt["transactionHash"] == HexBytes(mined_txn_hash)
        assert is_checksum_address(receipt["to"])
        assert receipt["from"] is not None
        assert is_checksum_address(receipt["from"])

        effective_gas_price = receipt["effectiveGasPrice"]
        assert isinstance(effective_gas_price, int)
        assert effective_gas_price > 0

    @pytest.mark.asyncio
    async def test_async_eth_get_transaction_receipt_unmined(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_hash = await async_w3.eth.send_transaction(
            {  
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
                "gas": 21000,
                "maxFeePerGas": async_w3.to_wei(3, "gwei"),
                "maxPriorityFeePerGas": async_w3.to_wei(1, "gwei"),
            }
        )
        with pytest.raises(TransactionNotFound):
            await async_w3.eth.get_transaction_receipt(txn_hash)  

    @pytest.mark.asyncio
    async def test_async_eth_get_transaction_receipt_with_log_entry(
        self,
        async_w3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract: "Contract",
        txn_hash_with_log: HexStr,
    ) -> None:
        receipt = await async_w3.eth.wait_for_transaction_receipt(  
            txn_hash_with_log
        )
        assert is_dict(receipt)
        assert receipt["blockNumber"] == block_with_txn_with_log["number"]
        assert receipt["blockHash"] == block_with_txn_with_log["hash"]
        assert receipt["transactionIndex"] == 0
        assert receipt["transactionHash"] == HexBytes(txn_hash_with_log)

        assert len(receipt["logs"]) == 1
        log_entry = receipt["logs"][0]

        assert log_entry["blockNumber"] == block_with_txn_with_log["number"]
        assert log_entry["blockHash"] == block_with_txn_with_log["hash"]
        assert log_entry["logIndex"] == 0
        assert is_same_address(log_entry["address"], emitter_contract.address)
        assert log_entry["transactionIndex"] == 0
        assert log_entry["transactionHash"] == HexBytes(txn_hash_with_log)

    @pytest.mark.asyncio
    async def test_async_eth_wait_for_transaction_receipt_mined(
        self, async_w3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        receipt = await async_w3.eth.wait_for_transaction_receipt(  
            mined_txn_hash
        )
        assert is_dict(receipt)
        assert receipt["blockNumber"] == block_with_txn["number"]
        assert receipt["blockHash"] == block_with_txn["hash"]
        assert receipt["transactionIndex"] == 0
        assert receipt["transactionHash"] == HexBytes(mined_txn_hash)
        assert is_checksum_address(receipt["to"])
        assert receipt["from"] is not None
        assert is_checksum_address(receipt["from"])

        effective_gas_price = receipt["effectiveGasPrice"]
        assert isinstance(effective_gas_price, int)
        assert effective_gas_price > 0

    @pytest.mark.asyncio
    async def test_async_eth_wait_for_transaction_receipt_unmined(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_hash = await async_w3.eth.send_transaction(
            {  
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
                "gas": 21000,
                "maxFeePerGas": async_w3.to_wei(3, "gwei"),
                "maxPriorityFeePerGas": async_w3.to_wei(1, "gwei"),
            }
        )

        timeout = 2
        with pytest.raises(TimeExhausted) as exc_info:
            await async_w3.eth.wait_for_transaction_receipt(
                txn_hash, timeout=timeout  
            )

        assert (_ in str(exc_info) for _ in [repr(txn_hash), timeout])

    @pytest.mark.asyncio
    async def test_async_eth_wait_for_transaction_receipt_with_log_entry(
        self,
        async_w3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract: "Contract",
        txn_hash_with_log: HexStr,
    ) -> None:
        receipt = await async_w3.eth.wait_for_transaction_receipt(  
            txn_hash_with_log
        )
        assert is_dict(receipt)
        assert receipt["blockNumber"] == block_with_txn_with_log["number"]
        assert receipt["blockHash"] == block_with_txn_with_log["hash"]
        assert receipt["transactionIndex"] == 0
        assert receipt["transactionHash"] == HexBytes(txn_hash_with_log)

        assert len(receipt["logs"]) == 1
        log_entry = receipt["logs"][0]

        assert log_entry["blockNumber"] == block_with_txn_with_log["number"]
        assert log_entry["blockHash"] == block_with_txn_with_log["hash"]
        assert log_entry["logIndex"] == 0
        assert is_same_address(log_entry["address"], emitter_contract.address)
        assert log_entry["transactionIndex"] == 0
        assert log_entry["transactionHash"] == HexBytes(txn_hash_with_log)

    @pytest.mark.asyncio
    async def test_async_eth_accounts(self, async_w3: "Web3") -> None:
        accounts = await async_w3.eth.accounts  
        assert is_list_like(accounts)
        assert len(accounts) != 0
        assert all((is_checksum_address(account) for account in accounts))
        assert await async_w3.eth.coinbase in accounts  

    @pytest.mark.asyncio
    async def test_async_eth_get_logs_without_logs(
        self, async_w3: "Web3", block_with_txn_with_log: BlockData
    ) -> None:
        

        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "toBlock": BlockNumber(block_with_txn_with_log["number"] - 1),
        }
        result = await async_w3.eth.get_logs(filter_params)  
        assert len(result) == 0

        
        filter_params = {
            "fromBlock": block_with_txn_with_log["number"],
            "toBlock": BlockNumber(block_with_txn_with_log["number"] - 1),
        }
        result = await async_w3.eth.get_logs(filter_params)  
        assert len(result) == 0

        

        
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": UNKNOWN_ADDRESS,
        }
        result = await async_w3.eth.get_logs(filter_params)  
        assert len(result) == 0

        

        
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": [UNKNOWN_ADDRESS, UNKNOWN_ADDRESS],
        }
        result = await async_w3.eth.get_logs(filter_params)  
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_async_eth_get_logs_with_logs(
        self,
        async_w3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract_address: ChecksumAddress,
        txn_hash_with_log: HexStr,
    ) -> None:

        

        
        filter_params: FilterParams = {
            "fromBlock": block_with_txn_with_log["number"],
            "toBlock": block_with_txn_with_log["number"],
        }
        result = await async_w3.eth.get_logs(filter_params)  
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

        
        filter_params = {
            "fromBlock": BlockNumber(0),
        }
        result = await async_w3.eth.get_logs(filter_params)  
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

        

        
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": emitter_contract_address,
        }
        result = await async_w3.eth.get_logs(filter_params)  
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

    @pytest.mark.asyncio
    async def test_async_eth_get_logs_with_logs_topic_args(
        self,
        async_w3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract_address: ChecksumAddress,
        txn_hash_with_log: HexStr,
    ) -> None:

        

        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "topics": [
                None,
                HexStr(
                    "0x000000000000000000000000000000000000000000000000000000000000d431"
                ),
            ],
        }

        result = await async_w3.eth.get_logs(filter_params)  
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

        
        filter_params = {
            "fromBlock": BlockNumber(0),
            "topics": [
                HexStr(
                    "0x057bc32826fbe161da1c110afcdcae7c109a8b69149f727fc37a603c60ef94ca"
                ),
                None,
            ],
        }
        result = await async_w3.eth.get_logs(filter_params)  
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

    @pytest.mark.asyncio
    async def test_async_eth_get_logs_with_logs_none_topic_args(
        self, async_w3: "Web3"
    ) -> None:
        
        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "topics": [None, None, None],
        }

        result = await async_w3.eth.get_logs(filter_params)  
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_async_eth_syncing(self, async_w3: "Web3") -> None:
        syncing = await async_w3.eth.syncing  

        assert is_boolean(syncing) or is_dict(syncing)

        if is_boolean(syncing):
            assert syncing is False
        elif is_dict(syncing):
            sync_dict = cast(SyncStatus, syncing)
            assert "startingBlock" in sync_dict
            assert "currentBlock" in sync_dict
            assert "highestBlock" in sync_dict

            assert is_integer(sync_dict["startingBlock"])
            assert is_integer(sync_dict["currentBlock"])
            assert is_integer(sync_dict["highestBlock"])

    @pytest.mark.asyncio
    async def test_async_eth_get_storage_at(
        self, async_w3: "Web3", emitter_contract_address: ChecksumAddress
    ) -> None:
        storage = await async_w3.eth.get_storage_at(  
            emitter_contract_address, 0
        )
        assert isinstance(storage, HexBytes)

    @pytest.mark.asyncio
    @pytest.mark.xfail
    async def test_async_eth_get_storage_at_ens_name(
        self, async_w3: "Web3", emitter_contract_address: ChecksumAddress
    ) -> None:
        with ens_addresses(async_w3, {"emitter.eth": emitter_contract_address}):
            storage = await async_w3.eth.get_storage_at(  
                ENS("emitter.eth"), 0
            )
            assert isinstance(storage, HexBytes)

    @pytest.mark.asyncio
    async def test_async_eth_get_storage_at_invalid_address(
        self, async_w3: "Web3"
    ) -> None:
        coinbase = await async_w3.eth.coinbase  
        with pytest.raises(InvalidAddress):
            await async_w3.eth.get_storage_at(
                ChecksumAddress(HexAddress(HexStr(coinbase.lower()))), 0
            )  

    def test_async_provider_default_account(
        self, async_w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:

        
        default_account = async_w3.eth.default_account
        assert default_account is empty

        
        async_w3.eth.default_account = unlocked_account_dual_type
        default_account = async_w3.eth.default_account
        assert default_account == unlocked_account_dual_type

        
        async_w3.eth.default_account = empty

    def test_async_provider_default_block(
        self,
        async_w3: "Web3",
    ) -> None:

        
        default_block = async_w3.eth.default_block
        assert default_block == "latest"

        
        async_w3.eth.default_block = BlockNumber(12345)
        default_block = async_w3.eth.default_block
        assert default_block == BlockNumber(12345)

        
        async_w3.eth.default_block = "latest"

    @pytest.mark.asyncio
    async def test_eth_getBlockTransactionCountByHash_empty_block(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        transaction_count = await async_w3.eth.get_block_transaction_count(  
            empty_block["hash"]
        )

        assert is_integer(transaction_count)
        assert transaction_count == 0

    @pytest.mark.asyncio
    async def test_eth_getBlockTransactionCountByNumber_empty_block(
        self, async_w3: "Web3", empty_block: BlockData
    ) -> None:
        transaction_count = await async_w3.eth.get_block_transaction_count(  
            empty_block["number"]
        )

        assert is_integer(transaction_count)
        assert transaction_count == 0

    @pytest.mark.asyncio
    async def test_eth_getBlockTransactionCountByHash_block_with_txn(
        self, async_w3: "Web3", block_with_txn: BlockData
    ) -> None:
        transaction_count = await async_w3.eth.get_block_transaction_count(  
            block_with_txn["hash"]
        )

        assert is_integer(transaction_count)
        assert transaction_count >= 1

    @pytest.mark.asyncio
    async def test_eth_getBlockTransactionCountByNumber_block_with_txn(
        self, async_w3: "Web3", block_with_txn: BlockData
    ) -> None:
        transaction_count = await async_w3.eth.get_block_transaction_count(  
            block_with_txn["number"]
        )

        assert is_integer(transaction_count)
        assert transaction_count >= 1

    @pytest.mark.asyncio
    async def test_async_eth_new_filter(self, async_w3: "Web3") -> None:
        filter = await async_w3.eth.filter({})  

        changes = await async_w3.eth.get_filter_changes(
            filter.filter_id
        )  
        assert is_list_like(changes)
        assert not changes

        logs = await async_w3.eth.get_filter_logs(filter.filter_id)  
        assert is_list_like(logs)
        assert not logs

        result = await async_w3.eth.uninstall_filter(filter.filter_id)  
        assert result is True

    @pytest.mark.asyncio
    async def test_async_eth_new_block_filter(self, async_w3: "Web3") -> None:
        filter = await async_w3.eth.filter("latest")  
        assert is_string(filter.filter_id)

        changes = await async_w3.eth.get_filter_changes(
            filter.filter_id
        )  
        assert is_list_like(changes)
        assert not changes

        result = await async_w3.eth.uninstall_filter(filter.filter_id)  
        assert result is True

    @pytest.mark.asyncio
    async def test_async_eth_new_pending_transaction_filter(
        self, async_w3: "Web3"
    ) -> None:
        filter = await async_w3.eth.filter("pending")  
        assert is_string(filter.filter_id)

        changes = await async_w3.eth.get_filter_changes(
            filter.filter_id
        )  
        assert is_list_like(changes)
        assert not changes

        result = await async_w3.eth.uninstall_filter(filter.filter_id)  
        assert result is True

    @pytest.mark.asyncio
    async def test_async_eth_uninstall_filter(self, async_w3: "Web3") -> None:
        filter = await async_w3.eth.filter({})  
        assert is_string(filter.filter_id)

        success = await async_w3.eth.uninstall_filter(filter.filter_id)  
        assert success is True

        failure = await async_w3.eth.uninstall_filter(filter.filter_id)  
        assert failure is False


class EthModuleTest:
    def test_eth_syncing(self, w3: "Web3") -> None:
        syncing = w3.eth.syncing

        assert is_boolean(syncing) or is_dict(syncing)

        if is_boolean(syncing):
            assert syncing is False
        elif is_dict(syncing):
            sync_dict = cast(SyncStatus, syncing)
            assert "startingBlock" in sync_dict
            assert "currentBlock" in sync_dict
            assert "highestBlock" in sync_dict

            assert is_integer(sync_dict["startingBlock"])
            assert is_integer(sync_dict["currentBlock"])
            assert is_integer(sync_dict["highestBlock"])

    def test_eth_coinbase(self, w3: "Web3") -> None:
        coinbase = w3.eth.coinbase
        assert is_checksum_address(coinbase)

    def test_eth_mining(self, w3: "Web3") -> None:
        mining = w3.eth.mining
        assert is_boolean(mining)

    def test_eth_hashrate(self, w3: "Web3") -> None:
        hashrate = w3.eth.hashrate
        assert is_integer(hashrate)
        assert hashrate >= 0

    def test_eth_chain_id(self, w3: "Web3") -> None:
        chain_id = w3.eth.chain_id
        
        assert chain_id == 131277322940537

    def test_eth_fee_history(self, w3: "Web3") -> None:
        fee_history = w3.eth.fee_history(1, "latest", [50])
        assert is_list_like(fee_history["baseFeePerGas"])
        assert is_list_like(fee_history["gasUsedRatio"])
        assert is_integer(fee_history["oldestBlock"])
        assert fee_history["oldestBlock"] >= 0
        assert is_list_like(fee_history["reward"])
        assert is_list_like(fee_history["reward"][0])

    def test_eth_fee_history_with_integer(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        fee_history = w3.eth.fee_history(1, empty_block["number"], [50])
        assert is_list_like(fee_history["baseFeePerGas"])
        assert is_list_like(fee_history["gasUsedRatio"])
        assert is_integer(fee_history["oldestBlock"])
        assert fee_history["oldestBlock"] >= 0
        assert is_list_like(fee_history["reward"])
        assert is_list_like(fee_history["reward"][0])

    def test_eth_fee_history_no_reward_percentiles(self, w3: "Web3") -> None:
        fee_history = w3.eth.fee_history(1, "latest")
        assert is_list_like(fee_history["baseFeePerGas"])
        assert is_list_like(fee_history["gasUsedRatio"])
        assert is_integer(fee_history["oldestBlock"])
        assert fee_history["oldestBlock"] >= 0

    def test_eth_gas_price(self, w3: "Web3") -> None:
        gas_price = w3.eth.gas_price
        assert is_integer(gas_price)
        assert gas_price > 0

    def test_eth_max_priority_fee(self, w3: "Web3") -> None:
        max_priority_fee = w3.eth.max_priority_fee
        assert is_integer(max_priority_fee)

    def test_eth_max_priority_fee_with_fee_history_calculation(
        self, w3: "Web3"
    ) -> None:
        fail_max_prio_middleware = construct_error_generator_middleware(
            {RPCEndpoint("eth_maxPriorityFeePerGas"): lambda *_: ""}
        )
        w3.middleware_onion.add(
            fail_max_prio_middleware, name="fail_max_prio_middleware"
        )

        with pytest.warns(
            UserWarning,
            match="There was an issue with the method eth_maxPriorityFeePerGas."
            " Calculating using eth_feeHistory.",
        ):
            max_priority_fee = w3.eth.max_priority_fee
            assert is_integer(max_priority_fee)

        w3.middleware_onion.remove("fail_max_prio_middleware")  

    def test_eth_accounts(self, w3: "Web3") -> None:
        accounts = w3.eth.accounts
        assert is_list_like(accounts)
        assert len(accounts) != 0
        assert all((is_checksum_address(account) for account in accounts))
        assert w3.eth.coinbase in accounts

    def test_eth_block_number(self, w3: "Web3") -> None:
        block_number = w3.eth.block_number
        assert is_integer(block_number)
        assert block_number >= 0

    def test_eth_get_block_number(self, w3: "Web3") -> None:
        block_number = w3.eth.get_block_number()
        assert is_integer(block_number)
        assert block_number >= 0

    def test_eth_get_balance(self, w3: "Web3") -> None:
        coinbase = w3.eth.coinbase

        with pytest.raises(InvalidAddress):
            w3.eth.get_balance(ChecksumAddress(HexAddress(HexStr(coinbase.lower()))))

        balance = w3.eth.get_balance(coinbase)

        assert is_integer(balance)
        assert balance >= 0

    def test_eth_get_balance_with_block_identifier(self, w3: "Web3") -> None:
        miner_address = w3.eth.get_block(1)["miner"]
        genesis_balance = w3.eth.get_balance(miner_address, 0)
        later_balance = w3.eth.get_balance(miner_address, 1)

        assert is_integer(genesis_balance)
        assert is_integer(later_balance)
        assert later_balance > genesis_balance

    @pytest.mark.parametrize(
        "address, expect_success",
        [("test-address.eth", True), ("not-an-address.eth", False)],
    )
    def test_eth_get_balance_with_ens_name(
        self, w3: "Web3", address: ChecksumAddress, expect_success: bool
    ) -> None:
        with ens_addresses(w3, {"test-address.eth": w3.eth.accounts[0]}):
            if expect_success:
                balance = w3.eth.get_balance(address)
                assert is_integer(balance)
                assert balance >= 0
            else:
                with pytest.raises(NameNotFound):
                    w3.eth.get_balance(address)

    def test_eth_get_storage_at(
        self, w3: "Web3", emitter_contract_address: ChecksumAddress
    ) -> None:
        storage = w3.eth.get_storage_at(emitter_contract_address, 0)
        assert isinstance(storage, HexBytes)

    def test_eth_get_storage_at_ens_name(
        self, w3: "Web3", emitter_contract_address: ChecksumAddress
    ) -> None:
        with ens_addresses(w3, {"emitter.eth": emitter_contract_address}):
            storage = w3.eth.get_storage_at(ENS("emitter.eth"), 0)
            assert isinstance(storage, HexBytes)

    def test_eth_get_storage_at_invalid_address(self, w3: "Web3") -> None:
        coinbase = w3.eth.coinbase
        with pytest.raises(InvalidAddress):
            w3.eth.get_storage_at(
                ChecksumAddress(HexAddress(HexStr(coinbase.lower()))), 0
            )

    def test_eth_get_transaction_count(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        transaction_count = w3.eth.get_transaction_count(unlocked_account_dual_type)
        assert is_integer(transaction_count)
        assert transaction_count >= 0

    def test_eth_get_transaction_count_ens_name(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        with ens_addresses(
            w3, {"unlocked-acct-dual-type.eth": unlocked_account_dual_type}
        ):
            transaction_count = w3.eth.get_transaction_count(
                ENS("unlocked-acct-dual-type.eth")
            )
            assert is_integer(transaction_count)
            assert transaction_count >= 0

    def test_eth_get_transaction_count_invalid_address(self, w3: "Web3") -> None:
        coinbase = w3.eth.coinbase
        with pytest.raises(InvalidAddress):
            w3.eth.get_transaction_count(
                ChecksumAddress(HexAddress(HexStr(coinbase.lower())))
            )

    def test_eth_getBlockTransactionCountByHash_empty_block(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        transaction_count = w3.eth.get_block_transaction_count(empty_block["hash"])

        assert is_integer(transaction_count)
        assert transaction_count == 0

    def test_eth_getBlockTransactionCountByNumber_empty_block(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        transaction_count = w3.eth.get_block_transaction_count(empty_block["number"])

        assert is_integer(transaction_count)
        assert transaction_count == 0

    def test_eth_getBlockTransactionCountByHash_block_with_txn(
        self, w3: "Web3", block_with_txn: BlockData
    ) -> None:
        transaction_count = w3.eth.get_block_transaction_count(block_with_txn["hash"])

        assert is_integer(transaction_count)
        assert transaction_count >= 1

    def test_eth_getBlockTransactionCountByNumber_block_with_txn(
        self, w3: "Web3", block_with_txn: BlockData
    ) -> None:
        transaction_count = w3.eth.get_block_transaction_count(block_with_txn["number"])

        assert is_integer(transaction_count)
        assert transaction_count >= 1

    def test_eth_getUncleCountByBlockHash(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        uncle_count = w3.eth.get_uncle_count(empty_block["hash"])

        assert is_integer(uncle_count)
        assert uncle_count == 0

    def test_eth_getUncleCountByBlockNumber(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        uncle_count = w3.eth.get_uncle_count(empty_block["number"])

        assert is_integer(uncle_count)
        assert uncle_count == 0

    def test_eth_get_code(
        self, w3: "Web3", math_contract_address: ChecksumAddress
    ) -> None:
        code = w3.eth.get_code(math_contract_address)
        assert isinstance(code, HexBytes)
        assert len(code) > 0

    def test_eth_get_code_ens_address(
        self, w3: "Web3", math_contract_address: ChecksumAddress
    ) -> None:
        with ens_addresses(w3, {"mathcontract.eth": math_contract_address}):
            code = w3.eth.get_code(ENS("mathcontract.eth"))
            assert isinstance(code, HexBytes)
            assert len(code) > 0

    def test_eth_get_code_invalid_address(
        self, w3: "Web3", math_contract: "Contract"
    ) -> None:
        with pytest.raises(InvalidAddress):
            w3.eth.get_code(
                ChecksumAddress(HexAddress(HexStr(math_contract.address.lower())))
            )

    def test_eth_get_code_with_block_identifier(
        self, w3: "Web3", emitter_contract: "Contract"
    ) -> None:
        code = w3.eth.get_code(
            emitter_contract.address, block_identifier=w3.eth.block_number
        )
        assert isinstance(code, HexBytes)
        assert len(code) > 0

    def test_eth_sign(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        signature = w3.eth.sign(
            unlocked_account_dual_type, text="Message tö sign. Longer than hash!"
        )
        assert is_bytes(signature)
        assert len(signature) == 32 + 32 + 1

        
        hexsign = w3.eth.sign(
            unlocked_account_dual_type,
            hexstr=HexStr(
                "0x4d6573736167652074c3b6207369676e2e204c6f6e676572207468616e206861736821"  
            ),
        )
        assert hexsign == signature

        intsign = w3.eth.sign(
            unlocked_account_dual_type,
            0x4D6573736167652074C3B6207369676E2E204C6F6E676572207468616E206861736821,
        )
        assert intsign == signature

        bytessign = w3.eth.sign(
            unlocked_account_dual_type, b"Message t\xc3\xb6 sign. Longer than hash!"
        )
        assert bytessign == signature

        new_signature = w3.eth.sign(
            unlocked_account_dual_type, text="different message is different"
        )
        assert new_signature != signature

    def test_eth_sign_ens_names(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        with ens_addresses(w3, {"unlocked-acct.eth": unlocked_account_dual_type}):
            signature = w3.eth.sign(
                "unlocked-acct.eth", text="Message tö sign. Longer than hash!"
            )
            assert is_bytes(signature)
            assert len(signature) == 32 + 32 + 1

    def test_eth_sign_typed_data(
        self,
        w3: "Web3",
        unlocked_account_dual_type: ChecksumAddress,
        skip_if_testrpc: Callable[["Web3"], None],
    ) -> None:
        validJSONMessage = """
            {
                "types": {
                    "EIP712Domain": [
                        {"name": "name", "type": "string"},
                        {"name": "version", "type": "string"},
                        {"name": "chainId", "type": "uint256"},
                        {"name": "verifyingContract", "type": "address"}
                    ],
                    "Person": [
                        {"name": "name", "type": "string"},
                        {"name": "wallet", "type": "address"}
                    ],
                    "Mail": [
                        {"name": "from", "type": "Person"},
                        {"name": "to", "type": "Person"},
                        {"name": "contents", "type": "string"}
                    ]
                },
                "primaryType": "Mail",
                "domain": {
                    "name": "Ether Mail",
                    "version": "1",
                    "chainId": "0x01",
                    "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC"
                },
                "message": {
                    "from": {
                        "name": "Cow",
                        "wallet": "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826"
                    },
                    "to": {
                        "name": "Bob",
                        "wallet": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"
                    },
                    "contents": "Hello, Bob!"
                }
            }
        """
        skip_if_testrpc(w3)
        signature = HexBytes(
            w3.eth.sign_typed_data(
                unlocked_account_dual_type, json.loads(validJSONMessage)
            )
        )
        assert len(signature) == 32 + 32 + 1

    def test_invalid_eth_sign_typed_data(
        self,
        w3: "Web3",
        unlocked_account_dual_type: ChecksumAddress,
        skip_if_testrpc: Callable[["Web3"], None],
    ) -> None:
        skip_if_testrpc(w3)
        invalid_typed_message = """
            {
                "types": {
                    "EIP712Domain": [
                        {"name": "name", "type": "string"},
                        {"name": "version", "type": "string"},
                        {"name": "chainId", "type": "uint256"},
                        {"name": "verifyingContract", "type": "address"}
                    ],
                    "Person": [
                        {"name": "name", "type": "string"},
                        {"name": "wallet", "type": "address"}
                    ],
                    "Mail": [
                        {"name": "from", "type": "Person"},
                        {"name": "to", "type": "Person[2]"},
                        {"name": "contents", "type": "string"}
                    ]
                },
                "primaryType": "Mail",
                "domain": {
                    "name": "Ether Mail",
                    "version": "1",
                    "chainId": "0x01",
                    "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC"
                },
                "message": {
                    "from": {
                        "name": "Cow",
                        "wallet": "0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826"
                    },
                    "to": [{
                        "name": "Bob",
                        "wallet": "0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"
                    }],
                    "contents": "Hello, Bob!"
                }
            }
        """
        with pytest.raises(
            ValueError,
            match=r".*Expected 2 items for array type Person\[2\], got 1 items.*",
        ):
            w3.eth.sign_typed_data(
                unlocked_account_dual_type, json.loads(invalid_typed_message)
            )

    def test_eth_sign_transaction_legacy(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": w3.eth.gas_price,
            "nonce": Nonce(0),
        }
        result = w3.eth.sign_transaction(txn_params)
        signatory_account = w3.eth.account.recover_transaction(result["raw"])
        assert unlocked_account == signatory_account
        assert result["tx"]["to"] == txn_params["to"]
        assert result["tx"]["value"] == txn_params["value"]
        assert result["tx"]["gas"] == txn_params["gas"]
        assert result["tx"]["gasPrice"] == txn_params["gasPrice"]
        assert result["tx"]["nonce"] == txn_params["nonce"]

    def test_eth_sign_transaction(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": w3.to_wei(2, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
            "nonce": Nonce(0),
        }
        result = w3.eth.sign_transaction(txn_params)
        signatory_account = w3.eth.account.recover_transaction(result["raw"])
        assert unlocked_account == signatory_account
        assert result["tx"]["to"] == txn_params["to"]
        assert result["tx"]["value"] == txn_params["value"]
        assert result["tx"]["gas"] == txn_params["gas"]
        assert result["tx"]["maxFeePerGas"] == txn_params["maxFeePerGas"]
        assert (
            result["tx"]["maxPriorityFeePerGas"] == txn_params["maxPriorityFeePerGas"]
        )
        assert result["tx"]["nonce"] == txn_params["nonce"]

    def test_eth_sign_transaction_hex_fees(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": hex(w3.to_wei(2, "gwei")),
            "maxPriorityFeePerGas": hex(w3.to_wei(1, "gwei")),
            "nonce": Nonce(0),
        }
        result = w3.eth.sign_transaction(txn_params)
        signatory_account = w3.eth.account.recover_transaction(result["raw"])
        assert unlocked_account == signatory_account
        assert result["tx"]["to"] == txn_params["to"]
        assert result["tx"]["value"] == txn_params["value"]
        assert result["tx"]["gas"] == txn_params["gas"]
        assert result["tx"]["maxFeePerGas"] == int(str(txn_params["maxFeePerGas"]), 16)
        assert result["tx"]["maxPriorityFeePerGas"] == int(
            str(txn_params["maxPriorityFeePerGas"]), 16
        )
        assert result["tx"]["nonce"] == txn_params["nonce"]

    def test_eth_sign_transaction_ens_names(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        with ens_addresses(w3, {"unlocked-account.eth": unlocked_account}):
            txn_params: TxParams = {
                "from": "unlocked-account.eth",
                "to": "unlocked-account.eth",
                "value": Wei(1),
                "gas": 21000,
                "maxFeePerGas": w3.to_wei(2, "gwei"),
                "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
                "nonce": Nonce(0),
            }
            result = w3.eth.sign_transaction(txn_params)
            signatory_account = w3.eth.account.recover_transaction(result["raw"])
            assert unlocked_account == signatory_account
            assert result["tx"]["to"] == unlocked_account
            assert result["tx"]["value"] == txn_params["value"]
            assert result["tx"]["gas"] == txn_params["gas"]
            assert result["tx"]["maxFeePerGas"] == txn_params["maxFeePerGas"]
            assert (
                result["tx"]["maxPriorityFeePerGas"]
                == txn_params["maxPriorityFeePerGas"]
            )
            assert result["tx"]["nonce"] == txn_params["nonce"]

    def test_eth_send_transaction_addr_checksum_required(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        non_checksum_addr = unlocked_account.lower()
        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": w3.to_wei(2, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
        }

        with pytest.raises(InvalidAddress):
            invalid_params = cast(
                TxParams, dict(txn_params, **{"from": non_checksum_addr})
            )
            w3.eth.send_transaction(invalid_params)

        with pytest.raises(InvalidAddress):
            invalid_params = cast(
                TxParams, dict(txn_params, **{"to": non_checksum_addr})
            )
            w3.eth.send_transaction(invalid_params)

    def test_eth_send_transaction_legacy(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": w3.to_wei(
                1, "gwei"
            ),  
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["gasPrice"] == txn_params["gasPrice"]

    def test_eth_send_transaction(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": w3.to_wei(3, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["maxFeePerGas"] == txn_params["maxFeePerGas"]
        assert txn["maxPriorityFeePerGas"] == txn_params["maxPriorityFeePerGas"]
        assert txn["gasPrice"] == txn_params["maxFeePerGas"]

    def test_eth_send_transaction_with_nonce(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        mine_pending_block(w3)  

        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            
            "maxFeePerGas": w3.to_wei(4.321, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
            "nonce": w3.eth.get_transaction_count(unlocked_account),
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["maxFeePerGas"] == txn_params["maxFeePerGas"]
        assert txn["maxPriorityFeePerGas"] == txn_params["maxPriorityFeePerGas"]
        assert txn["nonce"] == txn_params["nonce"]
        assert txn["gasPrice"] == txn_params["maxFeePerGas"]

    def test_eth_send_transaction_default_fees(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["maxPriorityFeePerGas"] == 1 * 10**9
        assert txn["maxFeePerGas"] >= 1 * 10**9
        assert txn["gasPrice"] == txn["maxFeePerGas"]

    def test_eth_send_transaction_hex_fees(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": hex(250 * 10**9),
            "maxPriorityFeePerGas": hex(2 * 10**9),
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000
        assert txn["maxFeePerGas"] == 250 * 10**9
        assert txn["maxPriorityFeePerGas"] == 2 * 10**9

    def test_eth_send_transaction_no_gas(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "maxFeePerGas": Wei(250 * 10**9),
            "maxPriorityFeePerGas": Wei(2 * 10**9),
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 121000  

    def test_eth_send_transaction_with_gas_price(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": Wei(1),
            "maxFeePerGas": Wei(250 * 10**9),
            "maxPriorityFeePerGas": Wei(2 * 10**9),
        }
        with pytest.raises(TransactionTypeMismatch):
            w3.eth.send_transaction(txn_params)

    def test_eth_send_transaction_no_priority_fee(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": Wei(250 * 10**9),
        }
        with pytest.raises(
            InvalidTransaction, match="maxPriorityFeePerGas must be defined"
        ):
            w3.eth.send_transaction(txn_params)

    def test_eth_send_transaction_no_max_fee(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        maxPriorityFeePerGas = w3.to_wei(2, "gwei")
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxPriorityFeePerGas": maxPriorityFeePerGas,
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        assert is_same_address(txn["from"], cast(ChecksumAddress, txn_params["from"]))
        assert is_same_address(txn["to"], cast(ChecksumAddress, txn_params["to"]))
        assert txn["value"] == 1
        assert txn["gas"] == 21000

        block = w3.eth.get_block("latest")
        assert txn["maxFeePerGas"] == maxPriorityFeePerGas + 2 * block["baseFeePerGas"]

    def test_eth_send_transaction_max_fee_less_than_tip(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": Wei(1 * 10**9),
            "maxPriorityFeePerGas": Wei(2 * 10**9),
        }
        with pytest.raises(
            InvalidTransaction, match="maxFeePerGas must be >= maxPriorityFeePerGas"
        ):
            w3.eth.send_transaction(txn_params)

    def test_validation_middleware_chain_id_mismatch(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        wrong_chain_id = 1234567890
        actual_chain_id = w3.eth.chain_id

        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": Wei(21000),
            "maxFeePerGas": w3.to_wei(2, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
            "chainId": wrong_chain_id,
        }
        with pytest.raises(
            ValidationError,
            match=f"The transaction declared chain ID {wrong_chain_id}, "
            f"but the connected node is on {actual_chain_id}",
        ):
            w3.eth.send_transaction(txn_params)

    @pytest.mark.parametrize(
        "max_fee", (1000000000, None), ids=["with_max_fee", "without_max_fee"]
    )
    def test_gas_price_from_strategy_bypassed_for_dynamic_fee_txn(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress, max_fee: Wei
    ) -> None:
        max_priority_fee = w3.to_wei(1, "gwei")
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxPriorityFeePerGas": max_priority_fee,
        }
        if max_fee is not None:
            txn_params = assoc(txn_params, "maxFeePerGas", max_fee)

        def gas_price_strategy(_w3: "Web3", _txn: TxParams) -> Wei:
            return w3.to_wei(2, "gwei")

        w3.eth.set_gas_price_strategy(gas_price_strategy)

        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        latest_block = w3.eth.get_block("latest")
        assert (
            txn["maxFeePerGas"] == max_fee
            if max_fee is not None
            else 2 * latest_block["baseFeePerGas"] + max_priority_fee
        )
        assert txn["maxPriorityFeePerGas"] == max_priority_fee
        assert txn["gasPrice"] == txn["maxFeePerGas"]

        w3.eth.set_gas_price_strategy(None)  

    def test_gas_price_from_strategy_bypassed_for_dynamic_fee_txn_no_tip(
        self,
        w3: "Web3",
        unlocked_account_dual_type: ChecksumAddress,
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": Wei(1000000000),
        }

        def gas_price_strategy(_w3: "Web3", _txn: TxParams) -> Wei:
            return w3.to_wei(2, "gwei")

        w3.eth.set_gas_price_strategy(gas_price_strategy)

        with pytest.raises(
            InvalidTransaction, match="maxPriorityFeePerGas must be defined"
        ):
            w3.eth.send_transaction(txn_params)

        w3.eth.set_gas_price_strategy(None)  

    def test_eth_replace_transaction_legacy(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": w3.to_wei(
                1, "gwei"
            ),  
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        txn_params["gasPrice"] = w3.to_wei(2, "gwei")
        replace_txn_hash = w3.eth.replace_transaction(txn_hash, txn_params)
        replace_txn = w3.eth.get_transaction(replace_txn_hash)

        assert is_same_address(
            replace_txn["from"], cast(ChecksumAddress, txn_params["from"])
        )
        assert is_same_address(
            replace_txn["to"], cast(ChecksumAddress, txn_params["to"])
        )
        assert replace_txn["value"] == 1
        assert replace_txn["gas"] == 21000
        assert replace_txn["gasPrice"] == txn_params["gasPrice"]

    def test_eth_replace_transaction(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        two_gwei_in_wei = w3.to_wei(2, "gwei")
        three_gwei_in_wei = w3.to_wei(3, "gwei")

        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": two_gwei_in_wei,
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        txn_params["maxFeePerGas"] = three_gwei_in_wei
        txn_params["maxPriorityFeePerGas"] = two_gwei_in_wei

        replace_txn_hash = w3.eth.replace_transaction(txn_hash, txn_params)
        replace_txn = w3.eth.get_transaction(replace_txn_hash)

        assert is_same_address(
            replace_txn["from"], cast(ChecksumAddress, txn_params["from"])
        )
        assert is_same_address(
            replace_txn["to"], cast(ChecksumAddress, txn_params["to"])
        )
        assert replace_txn["value"] == 1
        assert replace_txn["gas"] == 21000
        assert replace_txn["maxFeePerGas"] == three_gwei_in_wei
        assert replace_txn["maxPriorityFeePerGas"] == two_gwei_in_wei

    def test_eth_replace_transaction_underpriced(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": w3.to_wei(3, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        one_gwei_in_wei = w3.to_wei(1, "gwei")
        txn_params["maxFeePerGas"] = one_gwei_in_wei
        txn_params["maxPriorityFeePerGas"] = one_gwei_in_wei

        with pytest.raises(ValueError, match="replacement transaction underpriced"):
            w3.eth.replace_transaction(txn_hash, txn_params)

    def test_eth_replace_transaction_non_existing_transaction(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": w3.to_wei(3, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
        }
        with pytest.raises(TransactionNotFound):
            w3.eth.replace_transaction(
                HexStr(
                    "0x98e8cc09b311583c5079fa600f6c2a3bea8611af168c52e4b60b5b243a441997"
                ),
                txn_params,
            )

    def test_eth_replace_transaction_already_mined(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": w3.to_wei(2, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        try:
            w3.geth.miner.start()  
            w3.eth.wait_for_transaction_receipt(txn_hash, timeout=10)
        finally:
            w3.geth.miner.stop()  

        txn_params["maxFeePerGas"] = w3.to_wei(3, "gwei")
        txn_params["maxPriorityFeePerGas"] = w3.to_wei(2, "gwei")
        with pytest.raises(ValueError, match="Supplied transaction with hash"):
            w3.eth.replace_transaction(txn_hash, txn_params)

    def test_eth_replace_transaction_incorrect_nonce(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "maxFeePerGas": w3.to_wei(2, "gwei"),
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
        }
        txn_hash = w3.eth.send_transaction(txn_params)
        txn = w3.eth.get_transaction(txn_hash)

        txn_params["maxFeePerGas"] = w3.to_wei(3, "gwei")
        txn_params["maxPriorityFeePerGas"] = w3.to_wei(2, "gwei")
        txn_params["nonce"] = Nonce(txn["nonce"] + 1)
        with pytest.raises(ValueError):
            w3.eth.replace_transaction(txn_hash, txn_params)

    def test_eth_replace_transaction_gas_price_too_low(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account_dual_type,
            "to": unlocked_account_dual_type,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": w3.to_wei(2, "gwei"),
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        txn_params["gasPrice"] = w3.to_wei(1, "gwei")
        with pytest.raises(ValueError):
            w3.eth.replace_transaction(txn_hash, txn_params)

    def test_eth_replace_transaction_gas_price_defaulting_minimum(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        gas_price = w3.to_wei(1, "gwei")

        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": gas_price,
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        txn_params.pop("gasPrice")
        replace_txn_hash = w3.eth.replace_transaction(txn_hash, txn_params)
        replace_txn = w3.eth.get_transaction(replace_txn_hash)

        assert replace_txn["gasPrice"] == math.ceil(
            gas_price * 1.125
        )  

    def test_eth_replace_transaction_gas_price_defaulting_strategy_higher(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": w3.to_wei(1, "gwei"),
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        two_gwei_in_wei = w3.to_wei(2, "gwei")

        def higher_gas_price_strategy(w3: "Web3", txn: TxParams) -> Wei:
            return two_gwei_in_wei

        w3.eth.set_gas_price_strategy(higher_gas_price_strategy)

        txn_params.pop("gasPrice")
        replace_txn_hash = w3.eth.replace_transaction(txn_hash, txn_params)
        replace_txn = w3.eth.get_transaction(replace_txn_hash)
        assert (
            replace_txn["gasPrice"] == two_gwei_in_wei
        )  
        w3.eth.set_gas_price_strategy(None)  

    def test_eth_replace_transaction_gas_price_defaulting_strategy_lower(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        gas_price = w3.to_wei(2, "gwei")

        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": gas_price,
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        def lower_gas_price_strategy(w3: "Web3", txn: TxParams) -> Wei:
            return w3.to_wei(1, "gwei")

        w3.eth.set_gas_price_strategy(lower_gas_price_strategy)

        txn_params.pop("gasPrice")
        replace_txn_hash = w3.eth.replace_transaction(txn_hash, txn_params)
        replace_txn = w3.eth.get_transaction(replace_txn_hash)
        
        assert replace_txn["gasPrice"] == math.ceil(gas_price * 1.125)
        w3.eth.set_gas_price_strategy(None)  

    def test_eth_modify_transaction_legacy(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "gasPrice": w3.to_wei(
                1, "gwei"
            ),  
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        modified_txn_hash = w3.eth.modify_transaction(
            txn_hash, gasPrice=(cast(int, txn_params["gasPrice"]) * 2), value=2
        )
        modified_txn = w3.eth.get_transaction(modified_txn_hash)

        assert is_same_address(
            modified_txn["from"], cast(ChecksumAddress, txn_params["from"])
        )
        assert is_same_address(
            modified_txn["to"], cast(ChecksumAddress, txn_params["to"])
        )
        assert modified_txn["value"] == 2
        assert modified_txn["gas"] == 21000
        assert modified_txn["gasPrice"] == cast(int, txn_params["gasPrice"]) * 2

    def test_eth_modify_transaction(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        txn_params: TxParams = {
            "from": unlocked_account,
            "to": unlocked_account,
            "value": Wei(1),
            "gas": 21000,
            "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
            "maxFeePerGas": w3.to_wei(2, "gwei"),
        }
        txn_hash = w3.eth.send_transaction(txn_params)

        modified_txn_hash = w3.eth.modify_transaction(
            txn_hash,
            value=2,
            maxPriorityFeePerGas=(cast(Wei, txn_params["maxPriorityFeePerGas"]) * 2),
            maxFeePerGas=(cast(Wei, txn_params["maxFeePerGas"]) * 2),
        )
        modified_txn = w3.eth.get_transaction(modified_txn_hash)

        assert is_same_address(
            modified_txn["from"], cast(ChecksumAddress, txn_params["from"])
        )
        assert is_same_address(
            modified_txn["to"], cast(ChecksumAddress, txn_params["to"])
        )
        assert modified_txn["value"] == 2
        assert modified_txn["gas"] == 21000
        assert (
            modified_txn["maxPriorityFeePerGas"]
            == cast(Wei, txn_params["maxPriorityFeePerGas"]) * 2
        )
        assert modified_txn["maxFeePerGas"] == cast(Wei, txn_params["maxFeePerGas"]) * 2

    def test_eth_send_raw_transaction(
        self, w3: "Web3", unlocked_account: ChecksumAddress
    ) -> None:
        signed_tx = w3.eth.account.sign_transaction(
            {
                "to": "0x0000000000000000000000000000000000000000",
                "value": 0,
                "nonce": w3.eth.get_transaction_count(unlocked_account),
                "gas": 21000,
                "maxFeePerGas": 1000000000,
                "maxPriorityFeePerGas": 1000000000,
                "chainId": 131277322940537,
            },
            
            "0x392f63a79b1ff8774845f3fa69de4a13800a59e7083f5187f1558f0797ad0f01",
        )
        txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        assert txn_hash == signed_tx.hash

    def test_eth_call(self, w3: "Web3", math_contract: "Contract") -> None:
        coinbase = w3.eth.coinbase
        txn_params = math_contract._prepare_transaction(
            fn_name="add",
            fn_args=(7, 11),
            transaction={"from": coinbase, "to": math_contract.address},
        )
        call_result = w3.eth.call(txn_params)
        assert is_string(call_result)
        (result,) = w3.codec.decode(["uint256"], call_result)
        assert result == 18

    def test_eth_call_with_override(
        self, w3: "Web3", revert_contract: "Contract"
    ) -> None:
        coinbase = w3.eth.coinbase
        txn_params = revert_contract._prepare_transaction(
            fn_name="normalFunction",
            transaction={"from": coinbase, "to": revert_contract.address},
        )
        call_result = w3.eth.call(txn_params)
        (result,) = w3.codec.decode(["bool"], call_result)
        assert result is True

        
        override_code = HexStr(
            "0x6080604052348015600f57600080fd5b5060043610603c5760003560e01c8063185c38a4146041578063c06a97cb146049578063d67e4b84146051575b600080fd5b60476071565b005b604f60df565b005b605760e4565b604051808215151515815260200191505060405180910390f35b6040517f08c379a000000000000000000000000000000000000000000000000000000000815260040180806020018281038252601b8152602001807f46756e6374696f6e20686173206265656e2072657665727465642e000000000081525060200191505060405180910390fd5b600080fd5b60008090509056fea2646970667358221220bb71e9e9a2e271cd0fbe833524a3ea67df95f25ea13aef5b0a761fa52b538f1064736f6c63430006010033"  
        )
        call_result = w3.eth.call(
            txn_params, "latest", {revert_contract.address: {"code": override_code}}
        )
        (result,) = w3.codec.decode(["bool"], call_result)
        assert result is False

    def test_eth_call_with_0_result(
        self, w3: "Web3", math_contract: "Contract"
    ) -> None:
        coinbase = w3.eth.coinbase
        txn_params = math_contract._prepare_transaction(
            fn_name="add",
            fn_args=(0, 0),
            transaction={"from": coinbase, "to": math_contract.address},
        )
        call_result = w3.eth.call(txn_params)
        assert is_string(call_result)
        (result,) = w3.codec.decode(["uint256"], call_result)
        assert result == 0

    def test_eth_call_revert_with_msg(
        self,
        w3: "Web3",
        revert_contract: "Contract",
        unlocked_account: ChecksumAddress,
    ) -> None:
        with pytest.raises(
            ContractLogicError, match="execution reverted: Function has been reverted"
        ):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            w3.eth.call(txn_params)

    def test_eth_call_revert_without_msg(
        self,
        w3: "Web3",
        revert_contract: "Contract",
        unlocked_account: ChecksumAddress,
    ) -> None:
        with pytest.raises(ContractLogicError, match="execution reverted"):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithoutMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            w3.eth.call(txn_params)

    def test_eth_call_offchain_lookup(
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            offchain_lookup_contract.address
        ).lower()
        mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_json_data=WEB3PY_AS_HEXBYTES,
        )
        response = offchain_lookup_contract.functions.testOffchainLookup(
            OFFCHAIN_LOOKUP_TEST_DATA
        ).call()
        assert w3.codec.decode(["string"], response)[0] == "web3py"

    def test_eth_call_offchain_lookup_raises_when_ccip_read_is_disabled(
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
    ) -> None:
        
        with pytest.raises(OffchainLookup):
            offchain_lookup_contract.functions.testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            ).call(ccip_read_enabled=False)

        
        with pytest.raises(OffchainLookup):
            offchain_lookup_contract.caller(ccip_read_enabled=False).testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            )

        
        w3.provider.global_ccip_read_enabled = False

        with pytest.raises(OffchainLookup):
            offchain_lookup_contract.functions.testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            ).call()

        w3.provider.global_ccip_read_enabled = True  

    def test_eth_call_offchain_lookup_call_flag_overrides_provider_flag(
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            offchain_lookup_contract.address
        ).lower()
        mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_json_data=WEB3PY_AS_HEXBYTES,
        )

        w3.provider.global_ccip_read_enabled = False

        response = offchain_lookup_contract.functions.testOffchainLookup(
            OFFCHAIN_LOOKUP_TEST_DATA
        ).call(ccip_read_enabled=True)
        assert w3.codec.decode(["string"], response)[0] == "web3py"

        w3.provider.global_ccip_read_enabled = True  

    @pytest.mark.parametrize("max_redirects", range(-1, 4))
    def test_eth_call_offchain_lookup_raises_if_max_redirects_is_less_than_4(
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
        max_redirects: int,
    ) -> None:
        default_max_redirects = w3.provider.ccip_read_max_redirects

        w3.provider.ccip_read_max_redirects = max_redirects
        with pytest.raises(ValueError, match="at least 4"):
            offchain_lookup_contract.functions.testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            ).call()

        w3.provider.ccip_read_max_redirects = default_max_redirects  

    def test_eth_call_offchain_lookup_raises_for_improperly_formatted_rest_request_response(  
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            offchain_lookup_contract.address
        ).lower()
        mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_json_data=WEB3PY_AS_HEXBYTES,
            json_data_field="not_data",
        )
        with pytest.raises(ValidationError, match="missing 'data' field"):
            offchain_lookup_contract.functions.testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            ).call()

    @pytest.mark.parametrize("status_code_non_4xx_error", [100, 300, 500, 600])
    def test_eth_call_offchain_lookup_tries_next_url_for_non_4xx_error_status_and_tests_POST(  
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
        status_code_non_4xx_error: int,
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            offchain_lookup_contract.address
        ).lower()

        
        
        
        
        
        mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_status_code=status_code_non_4xx_error,
            mocked_json_data=WEB3PY_AS_HEXBYTES,
        )
        mock_offchain_lookup_request_response(
            monkeypatch,
            http_method="POST",
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}.json",  
            mocked_status_code=200,
            mocked_json_data=WEB3PY_AS_HEXBYTES,
            sender=normalized_contract_address,
            calldata=OFFCHAIN_LOOKUP_TEST_DATA,
        )
        response = offchain_lookup_contract.functions.testOffchainLookup(
            OFFCHAIN_LOOKUP_TEST_DATA
        ).call()
        assert w3.codec.decode(["string"], response)[0] == "web3py"

    def test_eth_call_offchain_lookup_calls_raise_for_status_for_4xx_status_code(
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            offchain_lookup_contract.address
        ).lower()
        mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/{OFFCHAIN_LOOKUP_TEST_DATA}.json",  
            mocked_status_code=randint(400, 499),
            mocked_json_data=WEB3PY_AS_HEXBYTES,
        )
        with pytest.raises(Exception, match="called raise_for_status\\(\\)"):
            offchain_lookup_contract.functions.testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            ).call()

    def test_eth_call_offchain_lookup_raises_when_all_supplied_urls_fail(
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
    ) -> None:
        
        with pytest.raises(
            MultipleFailedRequests, match="Offchain lookup failed for supplied urls"
        ):
            offchain_lookup_contract.functions.testOffchainLookup(
                OFFCHAIN_LOOKUP_TEST_DATA
            ).call()

    def test_eth_call_continuous_offchain_lookup_raises_with_too_many_requests(
        self,
        w3: "Web3",
        offchain_lookup_contract: "Contract",
        unlocked_account: ChecksumAddress,
        monkeypatch: "MonkeyPatch",
    ) -> None:
        normalized_contract_address = to_hex_if_bytes(
            offchain_lookup_contract.address
        ).lower()
        mock_offchain_lookup_request_response(
            monkeypatch,
            mocked_request_url=f"https://web3.py/gateway/{normalized_contract_address}/0x.json",  
        )
        with pytest.raises(TooManyRequests, match="Too many CCIP read redirects"):
            offchain_lookup_contract.caller().continuousOffchainLookup()

    def test_eth_estimate_gas_revert_with_msg(
        self,
        w3: "Web3",
        revert_contract: "Contract",
        unlocked_account: ChecksumAddress,
    ) -> None:
        with pytest.raises(
            ContractLogicError, match="execution reverted: Function has been reverted"
        ):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            w3.eth.estimate_gas(txn_params)

    def test_eth_estimate_gas_revert_without_msg(
        self,
        w3: "Web3",
        revert_contract: "Contract",
        unlocked_account: ChecksumAddress,
    ) -> None:
        with pytest.raises(ContractLogicError, match="execution reverted"):
            txn_params = revert_contract._prepare_transaction(
                fn_name="revertWithoutMessage",
                transaction={
                    "from": unlocked_account,
                    "to": revert_contract.address,
                },
            )
            w3.eth.estimate_gas(txn_params)

    def test_eth_estimate_gas(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        gas_estimate = w3.eth.estimate_gas(
            {
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
            }
        )
        assert is_integer(gas_estimate)
        assert gas_estimate > 0

    def test_eth_estimate_gas_with_block(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        gas_estimate = w3.eth.estimate_gas(
            {
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
            },
            "latest",
        )
        assert is_integer(gas_estimate)
        assert gas_estimate > 0

    def test_eth_getBlockByHash(self, w3: "Web3", empty_block: BlockData) -> None:
        block = w3.eth.get_block(empty_block["hash"])
        assert block["hash"] == empty_block["hash"]
        assert block["receiptsRoot"] == empty_block["receiptsRoot"]
        assert block["logsBloom"] == empty_block["logsBloom"]

    def test_eth_getBlockByHash_not_found(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        with pytest.raises(BlockNotFound):
            w3.eth.get_block(UNKNOWN_HASH)

    def test_eth_getBlockByHash_pending(self, w3: "Web3") -> None:
        block = w3.eth.get_block("pending")
        assert block["hash"] is None

    def test_eth_getBlockByNumber_with_integer(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        block = w3.eth.get_block(empty_block["number"])
        assert block["number"] == empty_block["number"]

    def test_eth_getBlockByNumber_latest(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        current_block_number = w3.eth.block_number
        block = w3.eth.get_block("latest")
        assert block["number"] == current_block_number

    def test_eth_getBlockByNumber_not_found(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        with pytest.raises(BlockNotFound):
            w3.eth.get_block(BlockNumber(12345))

    def test_eth_getBlockByNumber_pending(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        current_block_number = w3.eth.block_number
        block = w3.eth.get_block("pending")
        assert block["number"] == current_block_number + 1

    def test_eth_getBlockByNumber_earliest(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        genesis_block = w3.eth.get_block(BlockNumber(0))
        block = w3.eth.get_block("earliest")
        assert block["number"] == 0
        assert block["hash"] == genesis_block["hash"]

    @pytest.mark.xfail(reason="Integration test suite not yet set up for PoS")
    def test_eth_getBlockByNumber_safe(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        block = w3.eth.get_block("safe")
        assert block is not None
        assert isinstance(block["number"], int)

    @pytest.mark.xfail(reason="Integration test suite not yet set up for PoS")
    def test_eth_getBlockByNumber_finalized(
        self, w3: "Web3", empty_block: BlockData
    ) -> None:
        block = w3.eth.get_block("finalized")
        assert block is not None
        assert isinstance(block["number"], int)

    def test_eth_getBlockByNumber_full_transactions(
        self, w3: "Web3", block_with_txn: BlockData
    ) -> None:
        block = w3.eth.get_block(block_with_txn["number"], True)
        transaction = block["transactions"][0]
        assert transaction["hash"] == block_with_txn["transactions"][0]  

    def test_eth_getTransactionByHash(self, w3: "Web3", mined_txn_hash: HexStr) -> None:
        transaction = w3.eth.get_transaction(mined_txn_hash)
        assert is_dict(transaction)
        assert transaction["hash"] == HexBytes(mined_txn_hash)

    def test_eth_getTransactionByHash_contract_creation(
        self, w3: "Web3", math_contract_deploy_txn_hash: HexStr
    ) -> None:
        transaction = w3.eth.get_transaction(math_contract_deploy_txn_hash)
        assert is_dict(transaction)
        assert transaction["to"] is None, f"to field is {transaction['to']!r}"

    def test_eth_getTransactionByBlockHashAndIndex(
        self, w3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        transaction = w3.eth.get_transaction_by_block(block_with_txn["hash"], 0)
        assert is_dict(transaction)
        assert transaction["hash"] == HexBytes(mined_txn_hash)

    def test_eth_getTransactionByBlockNumberAndIndex(
        self, w3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        transaction = w3.eth.get_transaction_by_block(block_with_txn["number"], 0)
        assert is_dict(transaction)
        assert transaction["hash"] == HexBytes(mined_txn_hash)

    def test_eth_get_transaction_receipt_mined(
        self, w3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        receipt = w3.eth.get_transaction_receipt(mined_txn_hash)
        assert is_dict(receipt)
        assert receipt["blockNumber"] == block_with_txn["number"]
        assert receipt["blockHash"] == block_with_txn["hash"]
        assert receipt["transactionIndex"] == 0
        assert receipt["transactionHash"] == HexBytes(mined_txn_hash)
        assert is_checksum_address(receipt["to"])
        assert receipt["from"] is not None
        assert is_checksum_address(receipt["from"])

        effective_gas_price = receipt["effectiveGasPrice"]
        assert isinstance(effective_gas_price, int)
        assert effective_gas_price > 0

    def test_eth_get_transaction_receipt_unmined(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_hash = w3.eth.send_transaction(
            {
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
                "gas": 21000,
                "maxFeePerGas": w3.to_wei(3, "gwei"),
                "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
            }
        )
        with pytest.raises(TransactionNotFound):
            w3.eth.get_transaction_receipt(txn_hash)

    def test_eth_get_transaction_receipt_with_log_entry(
        self,
        w3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract: "Contract",
        txn_hash_with_log: HexStr,
    ) -> None:
        receipt = w3.eth.get_transaction_receipt(txn_hash_with_log)
        assert is_dict(receipt)
        assert receipt["blockNumber"] == block_with_txn_with_log["number"]
        assert receipt["blockHash"] == block_with_txn_with_log["hash"]
        assert receipt["transactionIndex"] == 0
        assert receipt["transactionHash"] == HexBytes(txn_hash_with_log)

        assert len(receipt["logs"]) == 1
        log_entry = receipt["logs"][0]

        assert log_entry["blockNumber"] == block_with_txn_with_log["number"]
        assert log_entry["blockHash"] == block_with_txn_with_log["hash"]
        assert log_entry["logIndex"] == 0
        assert is_same_address(log_entry["address"], emitter_contract.address)
        assert log_entry["transactionIndex"] == 0
        assert log_entry["transactionHash"] == HexBytes(txn_hash_with_log)

    def test_eth_wait_for_transaction_receipt_mined(
        self, w3: "Web3", block_with_txn: BlockData, mined_txn_hash: HexStr
    ) -> None:
        receipt = w3.eth.wait_for_transaction_receipt(mined_txn_hash)
        assert is_dict(receipt)
        assert receipt["blockNumber"] == block_with_txn["number"]
        assert receipt["blockHash"] == block_with_txn["hash"]
        assert receipt["transactionIndex"] == 0
        assert receipt["transactionHash"] == HexBytes(mined_txn_hash)
        assert is_checksum_address(receipt["to"])
        assert receipt["from"] is not None
        assert is_checksum_address(receipt["from"])

        effective_gas_price = receipt["effectiveGasPrice"]
        assert isinstance(effective_gas_price, int)
        assert effective_gas_price > 0

    def test_eth_wait_for_transaction_receipt_unmined(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:
        txn_hash = w3.eth.send_transaction(
            {
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
                "gas": 21000,
                "maxFeePerGas": w3.to_wei(3, "gwei"),
                "maxPriorityFeePerGas": w3.to_wei(1, "gwei"),
            }
        )

        timeout = 2
        with pytest.raises(TimeExhausted) as exc_info:
            w3.eth.wait_for_transaction_receipt(txn_hash, timeout=timeout)

        assert (_ in str(exc_info) for _ in [repr(txn_hash), timeout])

    def test_eth_wait_for_transaction_receipt_with_log_entry(
        self,
        w3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract: "Contract",
        txn_hash_with_log: HexStr,
    ) -> None:
        receipt = w3.eth.wait_for_transaction_receipt(txn_hash_with_log)
        assert is_dict(receipt)
        assert receipt["blockNumber"] == block_with_txn_with_log["number"]
        assert receipt["blockHash"] == block_with_txn_with_log["hash"]
        assert receipt["transactionIndex"] == 0
        assert receipt["transactionHash"] == HexBytes(txn_hash_with_log)

        assert len(receipt["logs"]) == 1
        log_entry = receipt["logs"][0]

        assert log_entry["blockNumber"] == block_with_txn_with_log["number"]
        assert log_entry["blockHash"] == block_with_txn_with_log["hash"]
        assert log_entry["logIndex"] == 0
        assert is_same_address(log_entry["address"], emitter_contract.address)
        assert log_entry["transactionIndex"] == 0
        assert log_entry["transactionHash"] == HexBytes(txn_hash_with_log)

    def test_eth_getUncleByBlockHashAndIndex(self, w3: "Web3") -> None:
        
        pass

    def test_eth_getUncleByBlockNumberAndIndex(self, w3: "Web3") -> None:
        
        pass

    def test_eth_new_filter(self, w3: "Web3") -> None:
        filter = w3.eth.filter({})

        changes = w3.eth.get_filter_changes(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        logs = w3.eth.get_filter_logs(filter.filter_id)
        assert is_list_like(logs)
        assert not logs

        result = w3.eth.uninstall_filter(filter.filter_id)
        assert result is True

    def test_eth_new_block_filter(self, w3: "Web3") -> None:
        filter = w3.eth.filter("latest")
        assert is_string(filter.filter_id)

        changes = w3.eth.get_filter_changes(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        result = w3.eth.uninstall_filter(filter.filter_id)
        assert result is True

    def test_eth_new_pending_transaction_filter(self, w3: "Web3") -> None:
        filter = w3.eth.filter("pending")
        assert is_string(filter.filter_id)

        changes = w3.eth.get_filter_changes(filter.filter_id)
        assert is_list_like(changes)
        assert not changes

        result = w3.eth.uninstall_filter(filter.filter_id)
        assert result is True

    def test_eth_get_logs_without_logs(
        self, w3: "Web3", block_with_txn_with_log: BlockData
    ) -> None:
        

        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "toBlock": BlockNumber(block_with_txn_with_log["number"] - 1),
        }
        result = w3.eth.get_logs(filter_params)
        assert len(result) == 0

        
        filter_params = {
            "fromBlock": block_with_txn_with_log["number"],
            "toBlock": BlockNumber(block_with_txn_with_log["number"] - 1),
        }
        result = w3.eth.get_logs(filter_params)
        assert len(result) == 0

        

        
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": UNKNOWN_ADDRESS,
        }
        result = w3.eth.get_logs(filter_params)
        assert len(result) == 0

        

        
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": [UNKNOWN_ADDRESS, UNKNOWN_ADDRESS],
        }
        result = w3.eth.get_logs(filter_params)
        assert len(result) == 0

    def test_eth_get_logs_with_logs(
        self,
        w3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract_address: ChecksumAddress,
        txn_hash_with_log: HexStr,
    ) -> None:

        

        
        filter_params: FilterParams = {
            "fromBlock": block_with_txn_with_log["number"],
            "toBlock": block_with_txn_with_log["number"],
        }
        result = w3.eth.get_logs(filter_params)
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

        
        filter_params = {
            "fromBlock": BlockNumber(0),
        }
        result = w3.eth.get_logs(filter_params)
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

        

        
        filter_params = {
            "fromBlock": BlockNumber(0),
            "address": emitter_contract_address,
        }

    def test_eth_get_logs_with_logs_topic_args(
        self,
        w3: "Web3",
        block_with_txn_with_log: BlockData,
        emitter_contract_address: ChecksumAddress,
        txn_hash_with_log: HexStr,
    ) -> None:

        

        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "topics": [
                None,
                HexStr(
                    "0x000000000000000000000000000000000000000000000000000000000000d431"
                ),
            ],
        }

        result = w3.eth.get_logs(filter_params)
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

        
        filter_params = {
            "fromBlock": BlockNumber(0),
            "topics": [
                HexStr(
                    "0x057bc32826fbe161da1c110afcdcae7c109a8b69149f727fc37a603c60ef94ca"
                ),
                None,
            ],
        }
        result = w3.eth.get_logs(filter_params)
        assert_contains_log(
            result, block_with_txn_with_log, emitter_contract_address, txn_hash_with_log
        )

    def test_eth_get_logs_with_logs_none_topic_args(self, w3: "Web3") -> None:
        
        filter_params: FilterParams = {
            "fromBlock": BlockNumber(0),
            "topics": [None, None, None],
        }

        result = w3.eth.get_logs(filter_params)
        assert len(result) == 0

    def test_eth_call_old_contract_state(
        self, w3: "Web3", math_contract: "Contract", unlocked_account: ChecksumAddress
    ) -> None:
        start_block = w3.eth.get_block("latest")
        block_num = start_block["number"]
        block_hash = start_block["hash"]

        math_contract.functions.increment().transact({"from": unlocked_account})

        
        
        
        
        
        
        
        block_hash_call_result = math_contract.functions.counter().call(
            block_identifier=block_hash
        )
        block_num_call_result = math_contract.functions.counter().call(
            block_identifier=block_num
        )
        latest_call_result = math_contract.functions.counter().call(
            block_identifier="latest"
        )
        default_call_result = math_contract.functions.counter().call()
        pending_call_result = math_contract.functions.counter().call(
            block_identifier="pending"
        )

        assert block_hash_call_result == 0
        assert block_num_call_result == 0
        assert latest_call_result == 0
        assert default_call_result == 0

        if pending_call_result != 1:
            raise AssertionError(
                f"pending call result was {pending_call_result} instead of 1"
            )

    def test_eth_uninstall_filter(self, w3: "Web3") -> None:
        filter = w3.eth.filter({})
        assert is_string(filter.filter_id)

        success = w3.eth.uninstall_filter(filter.filter_id)
        assert success is True

        failure = w3.eth.uninstall_filter(filter.filter_id)
        assert failure is False

    def test_eth_submit_hashrate(self, w3: "Web3") -> None:
        
        node_id = HexStr(
            "59daa26581d0acd1fce254fb7e85952f4c09d0915afd33d3886cd914bc7d283c"
        )
        result = w3.eth.submit_hashrate(5000, node_id)
        assert result is True

    def test_eth_submit_work(self, w3: "Web3") -> None:
        nonce = 1
        pow_hash = HexStr(
            "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        )
        mix_digest = HexStr(
            "0xD1FE5700000000000000000000000000D1FE5700000000000000000000000000"
        )
        result = w3.eth.submit_work(nonce, pow_hash, mix_digest)
        assert result is False

    def test_eth_get_raw_transaction(self, w3: "Web3", mined_txn_hash: HexStr) -> None:
        raw_transaction = w3.eth.get_raw_transaction(mined_txn_hash)
        assert is_bytes(raw_transaction)

    def test_eth_get_raw_transaction_raises_error(self, w3: "Web3") -> None:
        with pytest.raises(
            TransactionNotFound, match=f"Transaction with hash: '{UNKNOWN_HASH}'"
        ):
            w3.eth.get_raw_transaction(UNKNOWN_HASH)

    def test_eth_get_raw_transaction_by_block(
        self,
        w3: "Web3",
        unlocked_account_dual_type: ChecksumAddress,
        block_with_txn: BlockData,
    ) -> None:
        
        
        w3.eth.send_transaction(
            {
                "from": unlocked_account_dual_type,
                "to": unlocked_account_dual_type,
                "value": Wei(1),
            }
        )
        last_pending_txn_index = len(w3.eth.get_block("pending")["transactions"]) - 1
        raw_transaction = w3.eth.get_raw_transaction_by_block(
            "pending", last_pending_txn_index
        )
        assert is_bytes(raw_transaction)

        
        block_with_txn_number = block_with_txn["number"]
        assert is_integer(block_with_txn_number)
        raw_transaction = w3.eth.get_raw_transaction_by_block(block_with_txn_number, 0)
        assert is_bytes(raw_transaction)

        
        block_with_txn_hash = block_with_txn["hash"]
        assert is_bytes(block_with_txn_hash)
        raw_transaction = w3.eth.get_raw_transaction_by_block(block_with_txn_hash, 0)
        assert is_bytes(raw_transaction)

    @pytest.mark.parametrize("unknown_block_num_or_hash", (1234567899999, UNKNOWN_HASH))
    def test_eth_get_raw_transaction_by_block_raises_error(
        self, w3: "Web3", unknown_block_num_or_hash: Union[int, HexBytes]
    ) -> None:
        with pytest.raises(
            TransactionNotFound,
            match=(
                f"Transaction index: 0 on block id: "
                f"{to_hex_if_integer(unknown_block_num_or_hash)!r} not found."
            ),
        ):
            w3.eth.get_raw_transaction_by_block(unknown_block_num_or_hash, 0)

    def test_eth_get_raw_transaction_by_block_raises_error_block_identifier(
        self, w3: "Web3"
    ) -> None:
        unknown_identifier = "unknown"
        with pytest.raises(
            ValueError,
            match=(
                "Value did not match any of the recognized block identifiers: "
                f"{unknown_identifier}"
            ),
        ):
            w3.eth.get_raw_transaction_by_block(unknown_identifier, 0)  

    def test_default_account(
        self, w3: "Web3", unlocked_account_dual_type: ChecksumAddress
    ) -> None:

        
        default_account = w3.eth.default_account
        assert default_account is empty

        
        w3.eth.default_account = unlocked_account_dual_type
        default_account = w3.eth.default_account
        assert default_account == unlocked_account_dual_type

        
        w3.eth.default_account = empty

    def test_default_block(
        self,
        w3: "Web3",
    ) -> None:

        
        default_block = w3.eth.default_block
        assert default_block == "latest"

        
        w3.eth.default_block = BlockNumber(12345)
        default_block = w3.eth.default_block
        assert default_block == BlockNumber(12345)

        
        w3.eth.default_block = "latest"
