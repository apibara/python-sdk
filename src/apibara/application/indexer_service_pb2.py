# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: apibara/application/indexer_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n)apibara/application/indexer_service.proto\x12\x1c\x61pibara.application.v1alpha3\x1a\x1fgoogle/protobuf/timestamp.proto"1\n\x0b\x45ventFilter\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0c\x12\x11\n\tsignature\x18\x02 \x01(\t"\x1b\n\nTopicValue\x12\r\n\x05value\x18\x01 \x01(\x0c"\x1f\n\x0fStarkNetNetwork\x12\x0c\n\x04name\x18\x01 \x01(\t"\x1f\n\x0f\x45thereumNetwork\x12\x0c\n\x04name\x18\x02 \x01(\t"\x9a\x01\n\x07Network\x12\x41\n\x08starknet\x18\x01 \x01(\x0b\x32-.apibara.application.v1alpha3.StarkNetNetworkH\x00\x12\x41\n\x08\x65thereum\x18\x02 \x01(\x0b\x32-.apibara.application.v1alpha3.EthereumNetworkH\x00\x42\t\n\x07network"\xd7\x01\n\x07Indexer\x12\n\n\x02id\x18\x01 \x01(\t\x12\x36\n\x07network\x18\x02 \x01(\x0b\x32%.apibara.application.v1alpha3.Network\x12\x1d\n\x10indexed_to_block\x18\x03 \x01(\x04H\x00\x88\x01\x01\x12\x18\n\x10index_from_block\x18\x04 \x01(\x04\x12:\n\x07\x66ilters\x18\x05 \x03(\x0b\x32).apibara.application.v1alpha3.EventFilterB\x13\n\x11_indexed_to_block"\x8e\x01\n\x14\x43reateIndexerRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x0cnetwork_name\x18\x02 \x01(\t\x12\x18\n\x10index_from_block\x18\x03 \x01(\x04\x12:\n\x07\x66ilters\x18\x04 \x03(\x0b\x32).apibara.application.v1alpha3.EventFilter"O\n\x15\x43reateIndexerResponse\x12\x36\n\x07indexer\x18\x01 \x01(\x0b\x32%.apibara.application.v1alpha3.Indexer"\x1f\n\x11GetIndexerRequest\x12\n\n\x02id\x18\x01 \x01(\t"L\n\x12GetIndexerResponse\x12\x36\n\x07indexer\x18\x01 \x01(\x0b\x32%.apibara.application.v1alpha3.Indexer"\x14\n\x12ListIndexerRequest"N\n\x13ListIndexerResponse\x12\x37\n\x08indexers\x18\x01 \x03(\x0b\x32%.apibara.application.v1alpha3.Indexer""\n\x14\x44\x65leteIndexerRequest\x12\n\n\x02id\x18\x01 \x01(\t"O\n\x15\x44\x65leteIndexerResponse\x12\x36\n\x07indexer\x18\x01 \x01(\x0b\x32%.apibara.application.v1alpha3.Indexer"\x84\x01\n\x0b\x42lockHeader\x12\x0c\n\x04hash\x18\x01 \x01(\x0c\x12\x18\n\x0bparent_hash\x18\x02 \x01(\x0cH\x00\x88\x01\x01\x12\x0e\n\x06number\x18\x03 \x01(\x04\x12-\n\ttimestamp\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x0e\n\x0c_parent_hash"\xa5\x01\n\rStarkNetEvent\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0c\x12\x11\n\tlog_index\x18\x02 \x01(\x04\x12\x38\n\x06topics\x18\x03 \x03(\x0b\x32(.apibara.application.v1alpha3.TopicValue\x12\x36\n\x04\x64\x61ta\x18\x04 \x03(\x0b\x32(.apibara.application.v1alpha3.TopicValue"{\n\rEthereumEvent\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0c\x12\x11\n\tlog_index\x18\x02 \x01(\x04\x12\x38\n\x06topics\x18\x03 \x03(\x0b\x32(.apibara.application.v1alpha3.TopicValue\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c"\x92\x01\n\x05\x45vent\x12?\n\x08starknet\x18\x01 \x01(\x0b\x32+.apibara.application.v1alpha3.StarkNetEventH\x00\x12?\n\x08\x65thereum\x18\x02 \x01(\x0b\x32+.apibara.application.v1alpha3.EthereumEventH\x00\x42\x07\n\x05\x65vent"6\n\x07Version\x12\r\n\x05major\x18\x01 \x01(\x04\x12\r\n\x05minor\x18\x02 \x01(\x04\x12\r\n\x05patch\x18\x03 \x01(\x04"\x1c\n\x0e\x43onnectIndexer\x12\n\n\x02id\x18\x01 \x01(\t"\x82\x01\n\x10IndexerConnected\x12\x36\n\x07indexer\x18\x01 \x01(\x0b\x32%.apibara.application.v1alpha3.Indexer\x12\x36\n\x07version\x18\x02 \x01(\x0b\x32%.apibara.application.v1alpha3.Version"\x18\n\x08\x41\x63kBlock\x12\x0c\n\x04hash\x18\x01 \x01(\x0c"\x9a\x01\n\x15\x43onnectIndexerRequest\x12?\n\x07\x63onnect\x18\x01 \x01(\x0b\x32,.apibara.application.v1alpha3.ConnectIndexerH\x00\x12\x35\n\x03\x61\x63k\x18\x03 \x01(\x0b\x32&.apibara.application.v1alpha3.AckBlockH\x00\x42\t\n\x07message"G\n\x08NewBlock\x12;\n\x08new_head\x18\x01 \x01(\x0b\x32).apibara.application.v1alpha3.BlockHeader"D\n\x05Reorg\x12;\n\x08new_head\x18\x01 \x01(\x0b\x32).apibara.application.v1alpha3.BlockHeader"z\n\tNewEvents\x12\x38\n\x05\x62lock\x18\x01 \x01(\x0b\x32).apibara.application.v1alpha3.BlockHeader\x12\x33\n\x06\x65vents\x18\x02 \x03(\x0b\x32#.apibara.application.v1alpha3.Event"\x9a\x02\n\x16\x43onnectIndexerResponse\x12\x43\n\tconnected\x18\x01 \x01(\x0b\x32..apibara.application.v1alpha3.IndexerConnectedH\x00\x12;\n\tnew_block\x18\x02 \x01(\x0b\x32&.apibara.application.v1alpha3.NewBlockH\x00\x12\x34\n\x05reorg\x18\x03 \x01(\x0b\x32#.apibara.application.v1alpha3.ReorgH\x00\x12=\n\nnew_events\x18\x04 \x01(\x0b\x32\'.apibara.application.v1alpha3.NewEventsH\x00\x42\t\n\x07message2\xea\x04\n\x0eIndexerManager\x12x\n\rCreateIndexer\x12\x32.apibara.application.v1alpha3.CreateIndexerRequest\x1a\x33.apibara.application.v1alpha3.CreateIndexerResponse\x12o\n\nGetIndexer\x12/.apibara.application.v1alpha3.GetIndexerRequest\x1a\x30.apibara.application.v1alpha3.GetIndexerResponse\x12r\n\x0bListIndexer\x12\x30.apibara.application.v1alpha3.ListIndexerRequest\x1a\x31.apibara.application.v1alpha3.ListIndexerResponse\x12x\n\rDeleteIndexer\x12\x32.apibara.application.v1alpha3.DeleteIndexerRequest\x1a\x33.apibara.application.v1alpha3.DeleteIndexerResponse\x12\x7f\n\x0e\x43onnectIndexer\x12\x33.apibara.application.v1alpha3.ConnectIndexerRequest\x1a\x34.apibara.application.v1alpha3.ConnectIndexerResponse(\x01\x30\x01\x62\x06proto3'
)


_EVENTFILTER = DESCRIPTOR.message_types_by_name["EventFilter"]
_TOPICVALUE = DESCRIPTOR.message_types_by_name["TopicValue"]
_STARKNETNETWORK = DESCRIPTOR.message_types_by_name["StarkNetNetwork"]
_ETHEREUMNETWORK = DESCRIPTOR.message_types_by_name["EthereumNetwork"]
_NETWORK = DESCRIPTOR.message_types_by_name["Network"]
_INDEXER = DESCRIPTOR.message_types_by_name["Indexer"]
_CREATEINDEXERREQUEST = DESCRIPTOR.message_types_by_name["CreateIndexerRequest"]
_CREATEINDEXERRESPONSE = DESCRIPTOR.message_types_by_name["CreateIndexerResponse"]
_GETINDEXERREQUEST = DESCRIPTOR.message_types_by_name["GetIndexerRequest"]
_GETINDEXERRESPONSE = DESCRIPTOR.message_types_by_name["GetIndexerResponse"]
_LISTINDEXERREQUEST = DESCRIPTOR.message_types_by_name["ListIndexerRequest"]
_LISTINDEXERRESPONSE = DESCRIPTOR.message_types_by_name["ListIndexerResponse"]
_DELETEINDEXERREQUEST = DESCRIPTOR.message_types_by_name["DeleteIndexerRequest"]
_DELETEINDEXERRESPONSE = DESCRIPTOR.message_types_by_name["DeleteIndexerResponse"]
_BLOCKHEADER = DESCRIPTOR.message_types_by_name["BlockHeader"]
_STARKNETEVENT = DESCRIPTOR.message_types_by_name["StarkNetEvent"]
_ETHEREUMEVENT = DESCRIPTOR.message_types_by_name["EthereumEvent"]
_EVENT = DESCRIPTOR.message_types_by_name["Event"]
_VERSION = DESCRIPTOR.message_types_by_name["Version"]
_CONNECTINDEXER = DESCRIPTOR.message_types_by_name["ConnectIndexer"]
_INDEXERCONNECTED = DESCRIPTOR.message_types_by_name["IndexerConnected"]
_ACKBLOCK = DESCRIPTOR.message_types_by_name["AckBlock"]
_CONNECTINDEXERREQUEST = DESCRIPTOR.message_types_by_name["ConnectIndexerRequest"]
_NEWBLOCK = DESCRIPTOR.message_types_by_name["NewBlock"]
_REORG = DESCRIPTOR.message_types_by_name["Reorg"]
_NEWEVENTS = DESCRIPTOR.message_types_by_name["NewEvents"]
_CONNECTINDEXERRESPONSE = DESCRIPTOR.message_types_by_name["ConnectIndexerResponse"]
EventFilter = _reflection.GeneratedProtocolMessageType(
    "EventFilter",
    (_message.Message,),
    {
        "DESCRIPTOR": _EVENTFILTER,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.EventFilter)
    },
)
_sym_db.RegisterMessage(EventFilter)

TopicValue = _reflection.GeneratedProtocolMessageType(
    "TopicValue",
    (_message.Message,),
    {
        "DESCRIPTOR": _TOPICVALUE,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.TopicValue)
    },
)
_sym_db.RegisterMessage(TopicValue)

StarkNetNetwork = _reflection.GeneratedProtocolMessageType(
    "StarkNetNetwork",
    (_message.Message,),
    {
        "DESCRIPTOR": _STARKNETNETWORK,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.StarkNetNetwork)
    },
)
_sym_db.RegisterMessage(StarkNetNetwork)

EthereumNetwork = _reflection.GeneratedProtocolMessageType(
    "EthereumNetwork",
    (_message.Message,),
    {
        "DESCRIPTOR": _ETHEREUMNETWORK,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.EthereumNetwork)
    },
)
_sym_db.RegisterMessage(EthereumNetwork)

Network = _reflection.GeneratedProtocolMessageType(
    "Network",
    (_message.Message,),
    {
        "DESCRIPTOR": _NETWORK,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.Network)
    },
)
_sym_db.RegisterMessage(Network)

Indexer = _reflection.GeneratedProtocolMessageType(
    "Indexer",
    (_message.Message,),
    {
        "DESCRIPTOR": _INDEXER,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.Indexer)
    },
)
_sym_db.RegisterMessage(Indexer)

CreateIndexerRequest = _reflection.GeneratedProtocolMessageType(
    "CreateIndexerRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _CREATEINDEXERREQUEST,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.CreateIndexerRequest)
    },
)
_sym_db.RegisterMessage(CreateIndexerRequest)

CreateIndexerResponse = _reflection.GeneratedProtocolMessageType(
    "CreateIndexerResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _CREATEINDEXERRESPONSE,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.CreateIndexerResponse)
    },
)
_sym_db.RegisterMessage(CreateIndexerResponse)

GetIndexerRequest = _reflection.GeneratedProtocolMessageType(
    "GetIndexerRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETINDEXERREQUEST,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.GetIndexerRequest)
    },
)
_sym_db.RegisterMessage(GetIndexerRequest)

GetIndexerResponse = _reflection.GeneratedProtocolMessageType(
    "GetIndexerResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETINDEXERRESPONSE,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.GetIndexerResponse)
    },
)
_sym_db.RegisterMessage(GetIndexerResponse)

ListIndexerRequest = _reflection.GeneratedProtocolMessageType(
    "ListIndexerRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _LISTINDEXERREQUEST,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.ListIndexerRequest)
    },
)
_sym_db.RegisterMessage(ListIndexerRequest)

ListIndexerResponse = _reflection.GeneratedProtocolMessageType(
    "ListIndexerResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _LISTINDEXERRESPONSE,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.ListIndexerResponse)
    },
)
_sym_db.RegisterMessage(ListIndexerResponse)

DeleteIndexerRequest = _reflection.GeneratedProtocolMessageType(
    "DeleteIndexerRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _DELETEINDEXERREQUEST,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.DeleteIndexerRequest)
    },
)
_sym_db.RegisterMessage(DeleteIndexerRequest)

DeleteIndexerResponse = _reflection.GeneratedProtocolMessageType(
    "DeleteIndexerResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _DELETEINDEXERRESPONSE,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.DeleteIndexerResponse)
    },
)
_sym_db.RegisterMessage(DeleteIndexerResponse)

BlockHeader = _reflection.GeneratedProtocolMessageType(
    "BlockHeader",
    (_message.Message,),
    {
        "DESCRIPTOR": _BLOCKHEADER,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.BlockHeader)
    },
)
_sym_db.RegisterMessage(BlockHeader)

StarkNetEvent = _reflection.GeneratedProtocolMessageType(
    "StarkNetEvent",
    (_message.Message,),
    {
        "DESCRIPTOR": _STARKNETEVENT,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.StarkNetEvent)
    },
)
_sym_db.RegisterMessage(StarkNetEvent)

EthereumEvent = _reflection.GeneratedProtocolMessageType(
    "EthereumEvent",
    (_message.Message,),
    {
        "DESCRIPTOR": _ETHEREUMEVENT,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.EthereumEvent)
    },
)
_sym_db.RegisterMessage(EthereumEvent)

Event = _reflection.GeneratedProtocolMessageType(
    "Event",
    (_message.Message,),
    {
        "DESCRIPTOR": _EVENT,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.Event)
    },
)
_sym_db.RegisterMessage(Event)

Version = _reflection.GeneratedProtocolMessageType(
    "Version",
    (_message.Message,),
    {
        "DESCRIPTOR": _VERSION,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.Version)
    },
)
_sym_db.RegisterMessage(Version)

ConnectIndexer = _reflection.GeneratedProtocolMessageType(
    "ConnectIndexer",
    (_message.Message,),
    {
        "DESCRIPTOR": _CONNECTINDEXER,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.ConnectIndexer)
    },
)
_sym_db.RegisterMessage(ConnectIndexer)

IndexerConnected = _reflection.GeneratedProtocolMessageType(
    "IndexerConnected",
    (_message.Message,),
    {
        "DESCRIPTOR": _INDEXERCONNECTED,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.IndexerConnected)
    },
)
_sym_db.RegisterMessage(IndexerConnected)

AckBlock = _reflection.GeneratedProtocolMessageType(
    "AckBlock",
    (_message.Message,),
    {
        "DESCRIPTOR": _ACKBLOCK,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.AckBlock)
    },
)
_sym_db.RegisterMessage(AckBlock)

ConnectIndexerRequest = _reflection.GeneratedProtocolMessageType(
    "ConnectIndexerRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _CONNECTINDEXERREQUEST,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.ConnectIndexerRequest)
    },
)
_sym_db.RegisterMessage(ConnectIndexerRequest)

NewBlock = _reflection.GeneratedProtocolMessageType(
    "NewBlock",
    (_message.Message,),
    {
        "DESCRIPTOR": _NEWBLOCK,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.NewBlock)
    },
)
_sym_db.RegisterMessage(NewBlock)

Reorg = _reflection.GeneratedProtocolMessageType(
    "Reorg",
    (_message.Message,),
    {
        "DESCRIPTOR": _REORG,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.Reorg)
    },
)
_sym_db.RegisterMessage(Reorg)

NewEvents = _reflection.GeneratedProtocolMessageType(
    "NewEvents",
    (_message.Message,),
    {
        "DESCRIPTOR": _NEWEVENTS,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.NewEvents)
    },
)
_sym_db.RegisterMessage(NewEvents)

ConnectIndexerResponse = _reflection.GeneratedProtocolMessageType(
    "ConnectIndexerResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _CONNECTINDEXERRESPONSE,
        "__module__": "apibara.application.indexer_service_pb2"
        # @@protoc_insertion_point(class_scope:apibara.application.v1alpha3.ConnectIndexerResponse)
    },
)
_sym_db.RegisterMessage(ConnectIndexerResponse)

_INDEXERMANAGER = DESCRIPTOR.services_by_name["IndexerManager"]
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _EVENTFILTER._serialized_start = 108
    _EVENTFILTER._serialized_end = 157
    _TOPICVALUE._serialized_start = 159
    _TOPICVALUE._serialized_end = 186
    _STARKNETNETWORK._serialized_start = 188
    _STARKNETNETWORK._serialized_end = 219
    _ETHEREUMNETWORK._serialized_start = 221
    _ETHEREUMNETWORK._serialized_end = 252
    _NETWORK._serialized_start = 255
    _NETWORK._serialized_end = 409
    _INDEXER._serialized_start = 412
    _INDEXER._serialized_end = 627
    _CREATEINDEXERREQUEST._serialized_start = 630
    _CREATEINDEXERREQUEST._serialized_end = 772
    _CREATEINDEXERRESPONSE._serialized_start = 774
    _CREATEINDEXERRESPONSE._serialized_end = 853
    _GETINDEXERREQUEST._serialized_start = 855
    _GETINDEXERREQUEST._serialized_end = 886
    _GETINDEXERRESPONSE._serialized_start = 888
    _GETINDEXERRESPONSE._serialized_end = 964
    _LISTINDEXERREQUEST._serialized_start = 966
    _LISTINDEXERREQUEST._serialized_end = 986
    _LISTINDEXERRESPONSE._serialized_start = 988
    _LISTINDEXERRESPONSE._serialized_end = 1066
    _DELETEINDEXERREQUEST._serialized_start = 1068
    _DELETEINDEXERREQUEST._serialized_end = 1102
    _DELETEINDEXERRESPONSE._serialized_start = 1104
    _DELETEINDEXERRESPONSE._serialized_end = 1183
    _BLOCKHEADER._serialized_start = 1186
    _BLOCKHEADER._serialized_end = 1318
    _STARKNETEVENT._serialized_start = 1321
    _STARKNETEVENT._serialized_end = 1486
    _ETHEREUMEVENT._serialized_start = 1488
    _ETHEREUMEVENT._serialized_end = 1611
    _EVENT._serialized_start = 1614
    _EVENT._serialized_end = 1760
    _VERSION._serialized_start = 1762
    _VERSION._serialized_end = 1816
    _CONNECTINDEXER._serialized_start = 1818
    _CONNECTINDEXER._serialized_end = 1846
    _INDEXERCONNECTED._serialized_start = 1849
    _INDEXERCONNECTED._serialized_end = 1979
    _ACKBLOCK._serialized_start = 1981
    _ACKBLOCK._serialized_end = 2005
    _CONNECTINDEXERREQUEST._serialized_start = 2008
    _CONNECTINDEXERREQUEST._serialized_end = 2162
    _NEWBLOCK._serialized_start = 2164
    _NEWBLOCK._serialized_end = 2235
    _REORG._serialized_start = 2237
    _REORG._serialized_end = 2305
    _NEWEVENTS._serialized_start = 2307
    _NEWEVENTS._serialized_end = 2429
    _CONNECTINDEXERRESPONSE._serialized_start = 2432
    _CONNECTINDEXERRESPONSE._serialized_end = 2714
    _INDEXERMANAGER._serialized_start = 2717
    _INDEXERMANAGER._serialized_end = 3335
# @@protoc_insertion_point(module_scope)
