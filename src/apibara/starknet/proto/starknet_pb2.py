# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: starknet.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import \
    timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b"\n\x0estarknet.proto\x12\x19\x61pibara.starknet.v1alpha2\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0btypes.proto\"\x93\x03\n\x05\x42lock\x12\x36\n\x06status\x18\x01 \x01(\x0e\x32&.apibara.starknet.v1alpha2.BlockStatus\x12\x36\n\x06header\x18\x02 \x01(\x0b\x32&.apibara.starknet.v1alpha2.BlockHeader\x12G\n\x0ctransactions\x18\x03 \x03(\x0b\x32\x31.apibara.starknet.v1alpha2.TransactionWithReceipt\x12<\n\x0cstate_update\x18\x04 \x01(\x0b\x32&.apibara.starknet.v1alpha2.StateUpdate\x12?\n\x06\x65vents\x18\x05 \x03(\x0b\x32/.apibara.starknet.v1alpha2.EventWithTransaction\x12R\n\x11l2_to_l1_messages\x18\x06 \x03(\x0b\x32\x37.apibara.starknet.v1alpha2.L2ToL1MessageWithTransaction\"\xd2\x02\n\x0b\x42lockHeader\x12;\n\nblock_hash\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x42\n\x11parent_block_hash\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x14\n\x0c\x62lock_number\x18\x03 \x01(\x04\x12\x42\n\x11sequencer_address\x18\x04 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x39\n\x08new_root\x18\x05 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12-\n\ttimestamp\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x95\x01\n\x16TransactionWithReceipt\x12;\n\x0btransaction\x18\x01 \x01(\x0b\x32&.apibara.starknet.v1alpha2.Transaction\x12>\n\x07receipt\x18\x02 \x01(\x0b\x32-.apibara.starknet.v1alpha2.TransactionReceipt\"\xf8\x03\n\x0bTransaction\x12\x38\n\x04meta\x18\x01 \x01(\x0b\x32*.apibara.starknet.v1alpha2.TransactionMeta\x12\x43\n\tinvoke_v0\x18\x02 \x01(\x0b\x32..apibara.starknet.v1alpha2.InvokeTransactionV0H\x00\x12\x43\n\tinvoke_v1\x18\x03 \x01(\x0b\x32..apibara.starknet.v1alpha2.InvokeTransactionV1H\x00\x12>\n\x06\x64\x65ploy\x18\x04 \x01(\x0b\x32,.apibara.starknet.v1alpha2.DeployTransactionH\x00\x12@\n\x07\x64\x65\x63lare\x18\x05 \x01(\x0b\x32-.apibara.starknet.v1alpha2.DeclareTransactionH\x00\x12\x45\n\nl1_handler\x18\x06 \x01(\x0b\x32/.apibara.starknet.v1alpha2.L1HandlerTransactionH\x00\x12M\n\x0e\x64\x65ploy_account\x18\x07 \x01(\x0b\x32\x33.apibara.starknet.v1alpha2.DeployAccountTransactionH\x00\x42\r\n\x0btransaction\"\x87\x02\n\x0fTransactionMeta\x12\x35\n\x04hash\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x38\n\x07max_fee\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12:\n\tsignature\x18\x03 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x36\n\x05nonce\x18\x04 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x0f\n\x07version\x18\x05 \x01(\x04\"\xda\x01\n\x13InvokeTransactionV0\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x45\n\x14\x65ntry_point_selector\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x39\n\x08\x63\x61lldata\x18\x03 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x91\x01\n\x13InvokeTransactionV1\x12?\n\x0esender_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x39\n\x08\x63\x61lldata\x18\x02 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xdf\x01\n\x11\x44\x65ployTransaction\x12\x45\n\x14\x63onstructor_calldata\x18\x02 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x46\n\x15\x63ontract_address_salt\x18\x03 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12;\n\nclass_hash\x18\x04 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x92\x01\n\x12\x44\x65\x63lareTransaction\x12;\n\nclass_hash\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12?\n\x0esender_address\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xdb\x01\n\x14L1HandlerTransaction\x12\x41\n\x10\x63ontract_address\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x45\n\x14\x65ntry_point_selector\x18\x03 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x39\n\x08\x63\x61lldata\x18\x04 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xe6\x01\n\x18\x44\x65ployAccountTransaction\x12\x45\n\x14\x63onstructor_calldata\x18\x02 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x46\n\x15\x63ontract_address_salt\x18\x03 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12;\n\nclass_hash\x18\x04 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xa6\x02\n\x12TransactionReceipt\x12\x41\n\x10transaction_hash\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x19\n\x11transaction_index\x18\x02 \x01(\x04\x12;\n\nactual_fee\x18\x03 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x43\n\x11l2_to_l1_messages\x18\x04 \x03(\x0b\x32(.apibara.starknet.v1alpha2.L2ToL1Message\x12\x30\n\x06\x65vents\x18\x05 \x03(\x0b\x32 .apibara.starknet.v1alpha2.Event\"\xd6\x01\n\x1cL2ToL1MessageWithTransaction\x12;\n\x0btransaction\x18\x01 \x01(\x0b\x32&.apibara.starknet.v1alpha2.Transaction\x12>\n\x07receipt\x18\x02 \x01(\x0b\x32-.apibara.starknet.v1alpha2.TransactionReceipt\x12\x39\n\x07message\x18\x03 \x01(\x0b\x32(.apibara.starknet.v1alpha2.L2ToL1Message\"\x86\x01\n\rL2ToL1Message\x12;\n\nto_address\x18\x03 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x38\n\x07payload\x18\x04 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xc4\x01\n\x14\x45ventWithTransaction\x12;\n\x0btransaction\x18\x01 \x01(\x0b\x32&.apibara.starknet.v1alpha2.Transaction\x12>\n\x07receipt\x18\x02 \x01(\x0b\x32-.apibara.starknet.v1alpha2.TransactionReceipt\x12/\n\x05\x65vent\x18\x03 \x01(\x0b\x32 .apibara.starknet.v1alpha2.Event\"\xb4\x01\n\x05\x45vent\x12=\n\x0c\x66rom_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x35\n\x04keys\x18\x02 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x35\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xbd\x01\n\x0bStateUpdate\x12\x39\n\x08new_root\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x39\n\x08old_root\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x38\n\nstate_diff\x18\x03 \x01(\x0b\x32$.apibara.starknet.v1alpha2.StateDiff\"\x94\x02\n\tStateDiff\x12=\n\rstorage_diffs\x18\x01 \x03(\x0b\x32&.apibara.starknet.v1alpha2.StorageDiff\x12G\n\x12\x64\x65\x63lared_contracts\x18\x02 \x03(\x0b\x32+.apibara.starknet.v1alpha2.DeclaredContract\x12G\n\x12\x64\x65ployed_contracts\x18\x03 \x03(\x0b\x32+.apibara.starknet.v1alpha2.DeployedContract\x12\x36\n\x06nonces\x18\x04 \x03(\x0b\x32&.apibara.starknet.v1alpha2.NonceUpdate\"\x92\x01\n\x0bStorageDiff\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12@\n\x0fstorage_entries\x18\x02 \x03(\x0b\x32'.apibara.starknet.v1alpha2.StorageEntry\"|\n\x0cStorageEntry\x12\x34\n\x03key\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"O\n\x10\x44\x65\x63laredContract\x12;\n\nclass_hash\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x92\x01\n\x10\x44\x65ployedContract\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12;\n\nclass_hash\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x88\x01\n\x0bNonceUpdate\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x36\n\x05nonce\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement*\xa2\x01\n\x0b\x42lockStatus\x12\x1c\n\x18\x42LOCK_STATUS_UNSPECIFIED\x10\x00\x12\x18\n\x14\x42LOCK_STATUS_PENDING\x10\x01\x12\x1f\n\x1b\x42LOCK_STATUS_ACCEPTED_ON_L2\x10\x02\x12\x1f\n\x1b\x42LOCK_STATUS_ACCEPTED_ON_L1\x10\x03\x12\x19\n\x15\x42LOCK_STATUS_REJECTED\x10\x04\x62\x06proto3"
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "starknet_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _BLOCKSTATUS._serialized_start = 5111
    _BLOCKSTATUS._serialized_end = 5273
    _BLOCK._serialized_start = 92
    _BLOCK._serialized_end = 495
    _BLOCKHEADER._serialized_start = 498
    _BLOCKHEADER._serialized_end = 836
    _TRANSACTIONWITHRECEIPT._serialized_start = 839
    _TRANSACTIONWITHRECEIPT._serialized_end = 988
    _TRANSACTION._serialized_start = 991
    _TRANSACTION._serialized_end = 1495
    _TRANSACTIONMETA._serialized_start = 1498
    _TRANSACTIONMETA._serialized_end = 1761
    _INVOKETRANSACTIONV0._serialized_start = 1764
    _INVOKETRANSACTIONV0._serialized_end = 1982
    _INVOKETRANSACTIONV1._serialized_start = 1985
    _INVOKETRANSACTIONV1._serialized_end = 2130
    _DEPLOYTRANSACTION._serialized_start = 2133
    _DEPLOYTRANSACTION._serialized_end = 2356
    _DECLARETRANSACTION._serialized_start = 2359
    _DECLARETRANSACTION._serialized_end = 2505
    _L1HANDLERTRANSACTION._serialized_start = 2508
    _L1HANDLERTRANSACTION._serialized_end = 2727
    _DEPLOYACCOUNTTRANSACTION._serialized_start = 2730
    _DEPLOYACCOUNTTRANSACTION._serialized_end = 2960
    _TRANSACTIONRECEIPT._serialized_start = 2963
    _TRANSACTIONRECEIPT._serialized_end = 3257
    _L2TOL1MESSAGEWITHTRANSACTION._serialized_start = 3260
    _L2TOL1MESSAGEWITHTRANSACTION._serialized_end = 3474
    _L2TOL1MESSAGE._serialized_start = 3477
    _L2TOL1MESSAGE._serialized_end = 3611
    _EVENTWITHTRANSACTION._serialized_start = 3614
    _EVENTWITHTRANSACTION._serialized_end = 3810
    _EVENT._serialized_start = 3813
    _EVENT._serialized_end = 3993
    _STATEUPDATE._serialized_start = 3996
    _STATEUPDATE._serialized_end = 4185
    _STATEDIFF._serialized_start = 4188
    _STATEDIFF._serialized_end = 4464
    _STORAGEDIFF._serialized_start = 4467
    _STORAGEDIFF._serialized_end = 4613
    _STORAGEENTRY._serialized_start = 4615
    _STORAGEENTRY._serialized_end = 4739
    _DECLAREDCONTRACT._serialized_start = 4741
    _DECLAREDCONTRACT._serialized_end = 4820
    _DEPLOYEDCONTRACT._serialized_start = 4823
    _DEPLOYEDCONTRACT._serialized_end = 4969
    _NONCEUPDATE._serialized_start = 4972
    _NONCEUPDATE._serialized_end = 5108
# @@protoc_insertion_point(module_scope)