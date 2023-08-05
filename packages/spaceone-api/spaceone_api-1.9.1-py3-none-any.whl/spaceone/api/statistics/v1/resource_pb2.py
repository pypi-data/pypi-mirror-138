# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/statistics/v1/resource.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/statistics/v1/resource.proto',
  package='spaceone.api.statistics.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)spaceone/api/statistics/v1/resource.proto\x12\x1aspaceone.api.statistics.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\x8f\x01\n\x12StatAggregateQuery\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x34\n\x05query\x18\x02 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12,\n\x0b\x65xtend_data\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x99\x02\n\x11StatAggregateJoin\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x34\n\x05query\x18\x02 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12,\n\x0b\x65xtend_data\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x44\n\x04type\x18\x04 \x01(\x0e\x32\x36.spaceone.api.statistics.v1.StatAggregateJoin.JoinType\x12\x0c\n\x04keys\x18\x05 \x03(\t\"5\n\x08JoinType\x12\x08\n\x04LEFT\x10\x00\x12\t\n\x05RIGHT\x10\x01\x12\t\n\x05OUTER\x10\x02\x12\t\n\x05INNER\x10\x03\"\x90\x01\n\x13StatAggregateConcat\x12\x15\n\rresource_type\x18\x01 \x01(\t\x12\x34\n\x05query\x18\x02 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12,\n\x0b\x65xtend_data\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\".\n\x11StatAggregateSort\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x65sc\x18\x02 \x01(\x08\"H\n\x14StatAggregateFormula\x12\x0e\n\x04\x65val\x18\x01 \x01(\tH\x00\x12\x0f\n\x05query\x18\x02 \x01(\tH\x00\x42\x0f\n\rformula_alias\"<\n\x13StatAggregateFillNA\x12%\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x17.google.protobuf.Struct\"\xad\x03\n\rStatAggregate\x12?\n\x05query\x18\x01 \x01(\x0b\x32..spaceone.api.statistics.v1.StatAggregateQueryH\x00\x12=\n\x04join\x18\x02 \x01(\x0b\x32-.spaceone.api.statistics.v1.StatAggregateJoinH\x00\x12\x41\n\x06\x63oncat\x18\x03 \x01(\x0b\x32/.spaceone.api.statistics.v1.StatAggregateConcatH\x00\x12=\n\x04sort\x18\x04 \x01(\x0b\x32-.spaceone.api.statistics.v1.StatAggregateSortH\x00\x12\x43\n\x07\x66ormula\x18\x05 \x01(\x0b\x32\x30.spaceone.api.statistics.v1.StatAggregateFormulaH\x00\x12\x42\n\x07\x66ill_na\x18\x06 \x01(\x0b\x32/.spaceone.api.statistics.v1.StatAggregateFillNAH\x00\x42\x11\n\x0f\x61ggregate_alias\"(\n\x08StatPage\x12\r\n\x05start\x18\x01 \x01(\r\x12\r\n\x05limit\x18\x02 \x01(\r\"\x9a\x01\n\x13ResourceStatRequest\x12<\n\taggregate\x18\x01 \x03(\x0b\x32).spaceone.api.statistics.v1.StatAggregate\x12\x32\n\x04page\x18\x02 \x01(\x0b\x32$.spaceone.api.statistics.v1.StatPage\x12\x11\n\tdomain_id\x18\x03 \x01(\t2\x83\x01\n\x08Resource\x12w\n\x04stat\x12/.spaceone.api.statistics.v1.ResourceStatRequest\x1a\x17.google.protobuf.Struct\"%\x82\xd3\xe4\x93\x02\x1f\"\x1d/statistics/v1/resources/statb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,spaceone_dot_api_dot_core_dot_v1_dot_query__pb2.DESCRIPTOR,])



_STATAGGREGATEJOIN_JOINTYPE = _descriptor.EnumDescriptor(
  name='JoinType',
  full_name='spaceone.api.statistics.v1.StatAggregateJoin.JoinType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LEFT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RIGHT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OUTER', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='INNER', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=542,
  serialized_end=595,
)
_sym_db.RegisterEnumDescriptor(_STATAGGREGATEJOIN_JOINTYPE)


_STATAGGREGATEQUERY = _descriptor.Descriptor(
  name='StatAggregateQuery',
  full_name='spaceone.api.statistics.v1.StatAggregateQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.statistics.v1.StatAggregateQuery.resource_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.statistics.v1.StatAggregateQuery.query', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extend_data', full_name='spaceone.api.statistics.v1.StatAggregateQuery.extend_data', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=168,
  serialized_end=311,
)


_STATAGGREGATEJOIN = _descriptor.Descriptor(
  name='StatAggregateJoin',
  full_name='spaceone.api.statistics.v1.StatAggregateJoin',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.statistics.v1.StatAggregateJoin.resource_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.statistics.v1.StatAggregateJoin.query', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extend_data', full_name='spaceone.api.statistics.v1.StatAggregateJoin.extend_data', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='spaceone.api.statistics.v1.StatAggregateJoin.type', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keys', full_name='spaceone.api.statistics.v1.StatAggregateJoin.keys', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STATAGGREGATEJOIN_JOINTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=314,
  serialized_end=595,
)


_STATAGGREGATECONCAT = _descriptor.Descriptor(
  name='StatAggregateConcat',
  full_name='spaceone.api.statistics.v1.StatAggregateConcat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_type', full_name='spaceone.api.statistics.v1.StatAggregateConcat.resource_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.statistics.v1.StatAggregateConcat.query', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='extend_data', full_name='spaceone.api.statistics.v1.StatAggregateConcat.extend_data', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=598,
  serialized_end=742,
)


_STATAGGREGATESORT = _descriptor.Descriptor(
  name='StatAggregateSort',
  full_name='spaceone.api.statistics.v1.StatAggregateSort',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='spaceone.api.statistics.v1.StatAggregateSort.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='desc', full_name='spaceone.api.statistics.v1.StatAggregateSort.desc', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=744,
  serialized_end=790,
)


_STATAGGREGATEFORMULA = _descriptor.Descriptor(
  name='StatAggregateFormula',
  full_name='spaceone.api.statistics.v1.StatAggregateFormula',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='eval', full_name='spaceone.api.statistics.v1.StatAggregateFormula.eval', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.statistics.v1.StatAggregateFormula.query', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='formula_alias', full_name='spaceone.api.statistics.v1.StatAggregateFormula.formula_alias',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=792,
  serialized_end=864,
)


_STATAGGREGATEFILLNA = _descriptor.Descriptor(
  name='StatAggregateFillNA',
  full_name='spaceone.api.statistics.v1.StatAggregateFillNA',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='spaceone.api.statistics.v1.StatAggregateFillNA.data', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=866,
  serialized_end=926,
)


_STATAGGREGATE = _descriptor.Descriptor(
  name='StatAggregate',
  full_name='spaceone.api.statistics.v1.StatAggregate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.statistics.v1.StatAggregate.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='join', full_name='spaceone.api.statistics.v1.StatAggregate.join', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='concat', full_name='spaceone.api.statistics.v1.StatAggregate.concat', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sort', full_name='spaceone.api.statistics.v1.StatAggregate.sort', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='formula', full_name='spaceone.api.statistics.v1.StatAggregate.formula', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fill_na', full_name='spaceone.api.statistics.v1.StatAggregate.fill_na', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='aggregate_alias', full_name='spaceone.api.statistics.v1.StatAggregate.aggregate_alias',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=929,
  serialized_end=1358,
)


_STATPAGE = _descriptor.Descriptor(
  name='StatPage',
  full_name='spaceone.api.statistics.v1.StatPage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='start', full_name='spaceone.api.statistics.v1.StatPage.start', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='limit', full_name='spaceone.api.statistics.v1.StatPage.limit', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1360,
  serialized_end=1400,
)


_RESOURCESTATREQUEST = _descriptor.Descriptor(
  name='ResourceStatRequest',
  full_name='spaceone.api.statistics.v1.ResourceStatRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='aggregate', full_name='spaceone.api.statistics.v1.ResourceStatRequest.aggregate', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='page', full_name='spaceone.api.statistics.v1.ResourceStatRequest.page', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.statistics.v1.ResourceStatRequest.domain_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1403,
  serialized_end=1557,
)

_STATAGGREGATEQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
_STATAGGREGATEQUERY.fields_by_name['extend_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_STATAGGREGATEJOIN.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
_STATAGGREGATEJOIN.fields_by_name['extend_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_STATAGGREGATEJOIN.fields_by_name['type'].enum_type = _STATAGGREGATEJOIN_JOINTYPE
_STATAGGREGATEJOIN_JOINTYPE.containing_type = _STATAGGREGATEJOIN
_STATAGGREGATECONCAT.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
_STATAGGREGATECONCAT.fields_by_name['extend_data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_STATAGGREGATEFORMULA.oneofs_by_name['formula_alias'].fields.append(
  _STATAGGREGATEFORMULA.fields_by_name['eval'])
_STATAGGREGATEFORMULA.fields_by_name['eval'].containing_oneof = _STATAGGREGATEFORMULA.oneofs_by_name['formula_alias']
_STATAGGREGATEFORMULA.oneofs_by_name['formula_alias'].fields.append(
  _STATAGGREGATEFORMULA.fields_by_name['query'])
_STATAGGREGATEFORMULA.fields_by_name['query'].containing_oneof = _STATAGGREGATEFORMULA.oneofs_by_name['formula_alias']
_STATAGGREGATEFILLNA.fields_by_name['data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_STATAGGREGATE.fields_by_name['query'].message_type = _STATAGGREGATEQUERY
_STATAGGREGATE.fields_by_name['join'].message_type = _STATAGGREGATEJOIN
_STATAGGREGATE.fields_by_name['concat'].message_type = _STATAGGREGATECONCAT
_STATAGGREGATE.fields_by_name['sort'].message_type = _STATAGGREGATESORT
_STATAGGREGATE.fields_by_name['formula'].message_type = _STATAGGREGATEFORMULA
_STATAGGREGATE.fields_by_name['fill_na'].message_type = _STATAGGREGATEFILLNA
_STATAGGREGATE.oneofs_by_name['aggregate_alias'].fields.append(
  _STATAGGREGATE.fields_by_name['query'])
_STATAGGREGATE.fields_by_name['query'].containing_oneof = _STATAGGREGATE.oneofs_by_name['aggregate_alias']
_STATAGGREGATE.oneofs_by_name['aggregate_alias'].fields.append(
  _STATAGGREGATE.fields_by_name['join'])
_STATAGGREGATE.fields_by_name['join'].containing_oneof = _STATAGGREGATE.oneofs_by_name['aggregate_alias']
_STATAGGREGATE.oneofs_by_name['aggregate_alias'].fields.append(
  _STATAGGREGATE.fields_by_name['concat'])
_STATAGGREGATE.fields_by_name['concat'].containing_oneof = _STATAGGREGATE.oneofs_by_name['aggregate_alias']
_STATAGGREGATE.oneofs_by_name['aggregate_alias'].fields.append(
  _STATAGGREGATE.fields_by_name['sort'])
_STATAGGREGATE.fields_by_name['sort'].containing_oneof = _STATAGGREGATE.oneofs_by_name['aggregate_alias']
_STATAGGREGATE.oneofs_by_name['aggregate_alias'].fields.append(
  _STATAGGREGATE.fields_by_name['formula'])
_STATAGGREGATE.fields_by_name['formula'].containing_oneof = _STATAGGREGATE.oneofs_by_name['aggregate_alias']
_STATAGGREGATE.oneofs_by_name['aggregate_alias'].fields.append(
  _STATAGGREGATE.fields_by_name['fill_na'])
_STATAGGREGATE.fields_by_name['fill_na'].containing_oneof = _STATAGGREGATE.oneofs_by_name['aggregate_alias']
_RESOURCESTATREQUEST.fields_by_name['aggregate'].message_type = _STATAGGREGATE
_RESOURCESTATREQUEST.fields_by_name['page'].message_type = _STATPAGE
DESCRIPTOR.message_types_by_name['StatAggregateQuery'] = _STATAGGREGATEQUERY
DESCRIPTOR.message_types_by_name['StatAggregateJoin'] = _STATAGGREGATEJOIN
DESCRIPTOR.message_types_by_name['StatAggregateConcat'] = _STATAGGREGATECONCAT
DESCRIPTOR.message_types_by_name['StatAggregateSort'] = _STATAGGREGATESORT
DESCRIPTOR.message_types_by_name['StatAggregateFormula'] = _STATAGGREGATEFORMULA
DESCRIPTOR.message_types_by_name['StatAggregateFillNA'] = _STATAGGREGATEFILLNA
DESCRIPTOR.message_types_by_name['StatAggregate'] = _STATAGGREGATE
DESCRIPTOR.message_types_by_name['StatPage'] = _STATPAGE
DESCRIPTOR.message_types_by_name['ResourceStatRequest'] = _RESOURCESTATREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StatAggregateQuery = _reflection.GeneratedProtocolMessageType('StatAggregateQuery', (_message.Message,), {
  'DESCRIPTOR' : _STATAGGREGATEQUERY,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.StatAggregateQuery)
  })
_sym_db.RegisterMessage(StatAggregateQuery)

StatAggregateJoin = _reflection.GeneratedProtocolMessageType('StatAggregateJoin', (_message.Message,), {
  'DESCRIPTOR' : _STATAGGREGATEJOIN,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.StatAggregateJoin)
  })
_sym_db.RegisterMessage(StatAggregateJoin)

StatAggregateConcat = _reflection.GeneratedProtocolMessageType('StatAggregateConcat', (_message.Message,), {
  'DESCRIPTOR' : _STATAGGREGATECONCAT,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.StatAggregateConcat)
  })
_sym_db.RegisterMessage(StatAggregateConcat)

StatAggregateSort = _reflection.GeneratedProtocolMessageType('StatAggregateSort', (_message.Message,), {
  'DESCRIPTOR' : _STATAGGREGATESORT,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.StatAggregateSort)
  })
_sym_db.RegisterMessage(StatAggregateSort)

StatAggregateFormula = _reflection.GeneratedProtocolMessageType('StatAggregateFormula', (_message.Message,), {
  'DESCRIPTOR' : _STATAGGREGATEFORMULA,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.StatAggregateFormula)
  })
_sym_db.RegisterMessage(StatAggregateFormula)

StatAggregateFillNA = _reflection.GeneratedProtocolMessageType('StatAggregateFillNA', (_message.Message,), {
  'DESCRIPTOR' : _STATAGGREGATEFILLNA,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.StatAggregateFillNA)
  })
_sym_db.RegisterMessage(StatAggregateFillNA)

StatAggregate = _reflection.GeneratedProtocolMessageType('StatAggregate', (_message.Message,), {
  'DESCRIPTOR' : _STATAGGREGATE,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.StatAggregate)
  })
_sym_db.RegisterMessage(StatAggregate)

StatPage = _reflection.GeneratedProtocolMessageType('StatPage', (_message.Message,), {
  'DESCRIPTOR' : _STATPAGE,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.StatPage)
  })
_sym_db.RegisterMessage(StatPage)

ResourceStatRequest = _reflection.GeneratedProtocolMessageType('ResourceStatRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCESTATREQUEST,
  '__module__' : 'spaceone.api.statistics.v1.resource_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.statistics.v1.ResourceStatRequest)
  })
_sym_db.RegisterMessage(ResourceStatRequest)



_RESOURCE = _descriptor.ServiceDescriptor(
  name='Resource',
  full_name='spaceone.api.statistics.v1.Resource',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1560,
  serialized_end=1691,
  methods=[
  _descriptor.MethodDescriptor(
    name='stat',
    full_name='spaceone.api.statistics.v1.Resource.stat',
    index=0,
    containing_service=None,
    input_type=_RESOURCESTATREQUEST,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=b'\202\323\344\223\002\037\"\035/statistics/v1/resources/stat',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_RESOURCE)

DESCRIPTOR.services_by_name['Resource'] = _RESOURCE

# @@protoc_insertion_point(module_scope)
