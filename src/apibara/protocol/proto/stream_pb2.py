# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stream.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0cstream.proto\x12\x15\x61pibara.node.v1alpha2"\xf2\x01\n\x11StreamDataRequest\x12\x16\n\tstream_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x17\n\nbatch_size\x18\x02 \x01(\x04H\x01\x88\x01\x01\x12\x36\n\x0fstarting_cursor\x18\x03 \x01(\x0b\x32\x1d.apibara.node.v1alpha2.Cursor\x12:\n\x08\x66inality\x18\x04 \x01(\x0e\x32#.apibara.node.v1alpha2.DataFinalityH\x02\x88\x01\x01\x12\x0e\n\x06\x66ilter\x18\x05 \x01(\x0c\x42\x0c\n\n_stream_idB\r\n\x0b_batch_sizeB\x0b\n\t_finality"\xcf\x01\n\x12StreamDataResponse\x12\x11\n\tstream_id\x18\x01 \x01(\x04\x12\x37\n\ninvalidate\x18\x02 \x01(\x0b\x32!.apibara.node.v1alpha2.InvalidateH\x00\x12+\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x1b.apibara.node.v1alpha2.DataH\x00\x12\x35\n\theartbeat\x18\x04 \x01(\x0b\x32 .apibara.node.v1alpha2.HeartbeatH\x00\x42\t\n\x07message"/\n\x06\x43ursor\x12\x11\n\torder_key\x18\x01 \x01(\x04\x12\x12\n\nunique_key\x18\x02 \x01(\x0c";\n\nInvalidate\x12-\n\x06\x63ursor\x18\x01 \x01(\x0b\x32\x1d.apibara.node.v1alpha2.Cursor"\xad\x01\n\x04\x44\x61ta\x12\x31\n\nend_cursor\x18\x01 \x01(\x0b\x32\x1d.apibara.node.v1alpha2.Cursor\x12\x35\n\x08\x66inality\x18\x02 \x01(\x0e\x32#.apibara.node.v1alpha2.DataFinality\x12\x0c\n\x04\x64\x61ta\x18\x03 \x03(\x0c\x12-\n\x06\x63ursor\x18\x04 \x01(\x0b\x32\x1d.apibara.node.v1alpha2.Cursor"\x0b\n\tHeartbeat*u\n\x0c\x44\x61taFinality\x12\x17\n\x13\x44\x41TA_STATUS_UNKNOWN\x10\x00\x12\x17\n\x13\x44\x41TA_STATUS_PENDING\x10\x01\x12\x18\n\x14\x44\x41TA_STATUS_ACCEPTED\x10\x02\x12\x19\n\x15\x44\x41TA_STATUS_FINALIZED\x10\x03\x32o\n\x06Stream\x12\x65\n\nStreamData\x12(.apibara.node.v1alpha2.StreamDataRequest\x1a).apibara.node.v1alpha2.StreamDataResponse(\x01\x30\x01\x62\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "stream_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _DATAFINALITY._serialized_start = 793
    _DATAFINALITY._serialized_end = 910
    _STREAMDATAREQUEST._serialized_start = 40
    _STREAMDATAREQUEST._serialized_end = 282
    _STREAMDATARESPONSE._serialized_start = 285
    _STREAMDATARESPONSE._serialized_end = 492
    _CURSOR._serialized_start = 494
    _CURSOR._serialized_end = 541
    _INVALIDATE._serialized_start = 543
    _INVALIDATE._serialized_end = 602
    _DATA._serialized_start = 605
    _DATA._serialized_end = 778
    _HEARTBEAT._serialized_start = 780
    _HEARTBEAT._serialized_end = 791
    _STREAM._serialized_start = 912
    _STREAM._serialized_end = 1023
# @@protoc_insertion_point(module_scope)
