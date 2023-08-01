# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: filter.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b"\n\x0c\x66ilter.proto\x12\x19\x61pibara.starknet.v1alpha2\x1a\x0btypes.proto\"\xc3\x02\n\x06\x46ilter\x12\x37\n\x06header\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.HeaderFilter\x12\x42\n\x0ctransactions\x18\x02 \x03(\x0b\x32,.apibara.starknet.v1alpha2.TransactionFilter\x12\x42\n\x0cstate_update\x18\x03 \x01(\x0b\x32,.apibara.starknet.v1alpha2.StateUpdateFilter\x12\x36\n\x06\x65vents\x18\x04 \x03(\x0b\x32&.apibara.starknet.v1alpha2.EventFilter\x12@\n\x08messages\x18\x05 \x03(\x0b\x32..apibara.starknet.v1alpha2.L2ToL1MessageFilter\"\x1c\n\x0cHeaderFilter\x12\x0c\n\x04weak\x18\x01 \x01(\x08\"\xe3\x03\n\x11TransactionFilter\x12I\n\tinvoke_v0\x18\x01 \x01(\x0b\x32\x34.apibara.starknet.v1alpha2.InvokeTransactionV0FilterH\x00\x12I\n\tinvoke_v1\x18\x02 \x01(\x0b\x32\x34.apibara.starknet.v1alpha2.InvokeTransactionV1FilterH\x00\x12\x44\n\x06\x64\x65ploy\x18\x03 \x01(\x0b\x32\x32.apibara.starknet.v1alpha2.DeployTransactionFilterH\x00\x12\x46\n\x07\x64\x65\x63lare\x18\x04 \x01(\x0b\x32\x33.apibara.starknet.v1alpha2.DeclareTransactionFilterH\x00\x12K\n\nl1_handler\x18\x05 \x01(\x0b\x32\x35.apibara.starknet.v1alpha2.L1HandlerTransactionFilterH\x00\x12S\n\x0e\x64\x65ploy_account\x18\x06 \x01(\x0b\x32\x39.apibara.starknet.v1alpha2.DeployAccountTransactionFilterH\x00\x42\x08\n\x06\x66ilter\"\xe0\x01\n\x19InvokeTransactionV0Filter\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x45\n\x14\x65ntry_point_selector\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x39\n\x08\x63\x61lldata\x18\x03 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x97\x01\n\x19InvokeTransactionV1Filter\x12?\n\x0esender_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x39\n\x08\x63\x61lldata\x18\x03 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xe5\x01\n\x17\x44\x65ployTransactionFilter\x12\x46\n\x15\x63ontract_address_salt\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12;\n\nclass_hash\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x45\n\x14\x63onstructor_calldata\x18\x04 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x98\x01\n\x18\x44\x65\x63lareTransactionFilter\x12;\n\nclass_hash\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12?\n\x0esender_address\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xe1\x01\n\x1aL1HandlerTransactionFilter\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x45\n\x14\x65ntry_point_selector\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x39\n\x08\x63\x61lldata\x18\x03 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xec\x01\n\x1e\x44\x65ployAccountTransactionFilter\x12\x46\n\x15\x63ontract_address_salt\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12;\n\nclass_hash\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x45\n\x14\x63onstructor_calldata\x18\x04 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x8c\x01\n\x13L2ToL1MessageFilter\x12;\n\nto_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x38\n\x07payload\x18\x02 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xba\x01\n\x0b\x45ventFilter\x12=\n\x0c\x66rom_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x35\n\x04keys\x18\x02 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x35\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\xc8\x03\n\x11StateUpdateFilter\x12\x43\n\rstorage_diffs\x18\x01 \x03(\x0b\x32,.apibara.starknet.v1alpha2.StorageDiffFilter\x12M\n\x12\x64\x65\x63lared_contracts\x18\x02 \x03(\x0b\x32\x31.apibara.starknet.v1alpha2.DeclaredContractFilter\x12M\n\x12\x64\x65ployed_contracts\x18\x03 \x03(\x0b\x32\x31.apibara.starknet.v1alpha2.DeployedContractFilter\x12<\n\x06nonces\x18\x04 \x03(\x0b\x32,.apibara.starknet.v1alpha2.NonceUpdateFilter\x12H\n\x10\x64\x65\x63lared_classes\x18\x05 \x03(\x0b\x32..apibara.starknet.v1alpha2.DeclaredClassFilter\x12H\n\x10replaced_classes\x18\x06 \x03(\x0b\x32..apibara.starknet.v1alpha2.ReplacedClassFilter\"V\n\x11StorageDiffFilter\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"U\n\x16\x44\x65\x63laredContractFilter\x12;\n\nclass_hash\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x98\x01\n\x13\x44\x65\x63laredClassFilter\x12;\n\nclass_hash\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x44\n\x13\x63ompiled_class_hash\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x95\x01\n\x13ReplacedClassFilter\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12;\n\nclass_hash\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x98\x01\n\x16\x44\x65ployedContractFilter\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12;\n\nclass_hash\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\"\x8e\x01\n\x11NonceUpdateFilter\x12\x41\n\x10\x63ontract_address\x18\x01 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElement\x12\x36\n\x05nonce\x18\x02 \x01(\x0b\x32'.apibara.starknet.v1alpha2.FieldElementb\x06proto3"
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "filter_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_FILTER"]._serialized_start = 57
    _globals["_FILTER"]._serialized_end = 380
    _globals["_HEADERFILTER"]._serialized_start = 382
    _globals["_HEADERFILTER"]._serialized_end = 410
    _globals["_TRANSACTIONFILTER"]._serialized_start = 413
    _globals["_TRANSACTIONFILTER"]._serialized_end = 896
    _globals["_INVOKETRANSACTIONV0FILTER"]._serialized_start = 899
    _globals["_INVOKETRANSACTIONV0FILTER"]._serialized_end = 1123
    _globals["_INVOKETRANSACTIONV1FILTER"]._serialized_start = 1126
    _globals["_INVOKETRANSACTIONV1FILTER"]._serialized_end = 1277
    _globals["_DEPLOYTRANSACTIONFILTER"]._serialized_start = 1280
    _globals["_DEPLOYTRANSACTIONFILTER"]._serialized_end = 1509
    _globals["_DECLARETRANSACTIONFILTER"]._serialized_start = 1512
    _globals["_DECLARETRANSACTIONFILTER"]._serialized_end = 1664
    _globals["_L1HANDLERTRANSACTIONFILTER"]._serialized_start = 1667
    _globals["_L1HANDLERTRANSACTIONFILTER"]._serialized_end = 1892
    _globals["_DEPLOYACCOUNTTRANSACTIONFILTER"]._serialized_start = 1895
    _globals["_DEPLOYACCOUNTTRANSACTIONFILTER"]._serialized_end = 2131
    _globals["_L2TOL1MESSAGEFILTER"]._serialized_start = 2134
    _globals["_L2TOL1MESSAGEFILTER"]._serialized_end = 2274
    _globals["_EVENTFILTER"]._serialized_start = 2277
    _globals["_EVENTFILTER"]._serialized_end = 2463
    _globals["_STATEUPDATEFILTER"]._serialized_start = 2466
    _globals["_STATEUPDATEFILTER"]._serialized_end = 2922
    _globals["_STORAGEDIFFFILTER"]._serialized_start = 2924
    _globals["_STORAGEDIFFFILTER"]._serialized_end = 3010
    _globals["_DECLAREDCONTRACTFILTER"]._serialized_start = 3012
    _globals["_DECLAREDCONTRACTFILTER"]._serialized_end = 3097
    _globals["_DECLAREDCLASSFILTER"]._serialized_start = 3100
    _globals["_DECLAREDCLASSFILTER"]._serialized_end = 3252
    _globals["_REPLACEDCLASSFILTER"]._serialized_start = 3255
    _globals["_REPLACEDCLASSFILTER"]._serialized_end = 3404
    _globals["_DEPLOYEDCONTRACTFILTER"]._serialized_start = 3407
    _globals["_DEPLOYEDCONTRACTFILTER"]._serialized_end = 3559
    _globals["_NONCEUPDATEFILTER"]._serialized_start = 3562
    _globals["_NONCEUPDATEFILTER"]._serialized_end = 3704
# @@protoc_insertion_point(module_scope)
