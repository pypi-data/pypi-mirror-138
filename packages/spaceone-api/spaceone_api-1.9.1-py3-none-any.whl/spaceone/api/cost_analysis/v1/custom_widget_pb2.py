# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/cost_analysis/v1/custom_widget.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='spaceone/api/cost_analysis/v1/custom_widget.proto',
  package='spaceone.api.cost_analysis.v1',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n1spaceone/api/cost_analysis/v1/custom_widget.proto\x12\x1dspaceone.api.cost_analysis.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"\x8d\x01\n\x19\x43reateCustomWidgetRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"\xa7\x01\n\x19UpdateCustomWidgetRequest\x12\x18\n\x10\x63ustom_widget_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"B\n\x13\x43ustomWidgetRequest\x12\x18\n\x10\x63ustom_widget_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\"S\n\x16GetCustomWidgetRequest\x12\x18\n\x10\x63ustom_widget_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\x8b\x01\n\x11\x43ustomWidgetQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x18\n\x10\x63ustom_widget_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07user_id\x18\x04 \x01(\t\x12\x11\n\tdomain_id\x18\x0b \x01(\t\"\xd7\x01\n\x10\x43ustomWidgetInfo\x12\x18\n\x10\x63ustom_widget_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12(\n\x07options\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x12%\n\x04tags\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0f\n\x07user_id\x18\x0b \x01(\t\x12\x11\n\tdomain_id\x18\x0c \x01(\t\x12\x12\n\ncreated_at\x18\x15 \x01(\t\x12\x12\n\nupdated_at\x18\x16 \x01(\t\"j\n\x11\x43ustomWidgetsInfo\x12@\n\x07results\x18\x01 \x03(\x0b\x32/.spaceone.api.cost_analysis.v1.CustomWidgetInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"`\n\x15\x43ustomWidgetStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xe8\x07\n\x0c\x43ustomWidget\x12\x9d\x01\n\x06\x63reate\x12\x38.spaceone.api.cost_analysis.v1.CreateCustomWidgetRequest\x1a/.spaceone.api.cost_analysis.v1.CustomWidgetInfo\"(\x82\xd3\xe4\x93\x02\"\" /cost-analysis/v1/custom-widgets\x12\xaf\x01\n\x06update\x12\x38.spaceone.api.cost_analysis.v1.UpdateCustomWidgetRequest\x1a/.spaceone.api.cost_analysis.v1.CustomWidgetInfo\":\x82\xd3\xe4\x93\x02\x34\x1a\x32/cost-analysis/v1/custom-widget/{custom_widget_id}\x12\x90\x01\n\x06\x64\x65lete\x12\x32.spaceone.api.cost_analysis.v1.CustomWidgetRequest\x1a\x16.google.protobuf.Empty\":\x82\xd3\xe4\x93\x02\x34*2/cost-analysis/v1/custom-widget/{custom_widget_id}\x12\xa9\x01\n\x03get\x12\x35.spaceone.api.cost_analysis.v1.GetCustomWidgetRequest\x1a/.spaceone.api.cost_analysis.v1.CustomWidgetInfo\":\x82\xd3\xe4\x93\x02\x34\x12\x32/cost-analysis/v1/custom-widget/{custom_widget_id}\x12\xbf\x01\n\x04list\x12\x30.spaceone.api.cost_analysis.v1.CustomWidgetQuery\x1a\x30.spaceone.api.cost_analysis.v1.CustomWidgetsInfo\"S\x82\xd3\xe4\x93\x02M\x12 /cost-analysis/v1/custom-widgetsZ)\"\'/cost-analysis/v1/custom-widgets/search\x12\x84\x01\n\x04stat\x12\x34.spaceone.api.cost_analysis.v1.CustomWidgetStatQuery\x1a\x17.google.protobuf.Struct\"-\x82\xd3\xe4\x93\x02\'\"%/cost-analysis/v1/custom-widgets/statb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,spaceone_dot_api_dot_core_dot_v1_dot_query__pb2.DESCRIPTOR,])




_CREATECUSTOMWIDGETREQUEST = _descriptor.Descriptor(
  name='CreateCustomWidgetRequest',
  full_name='spaceone.api.cost_analysis.v1.CreateCustomWidgetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.cost_analysis.v1.CreateCustomWidgetRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.cost_analysis.v1.CreateCustomWidgetRequest.options', index=1,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='spaceone.api.cost_analysis.v1.CreateCustomWidgetRequest.tags', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.cost_analysis.v1.CreateCustomWidgetRequest.domain_id', index=3,
      number=11, type=9, cpp_type=9, label=1,
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
  serialized_start=208,
  serialized_end=349,
)


_UPDATECUSTOMWIDGETREQUEST = _descriptor.Descriptor(
  name='UpdateCustomWidgetRequest',
  full_name='spaceone.api.cost_analysis.v1.UpdateCustomWidgetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='custom_widget_id', full_name='spaceone.api.cost_analysis.v1.UpdateCustomWidgetRequest.custom_widget_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.cost_analysis.v1.UpdateCustomWidgetRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.cost_analysis.v1.UpdateCustomWidgetRequest.options', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='spaceone.api.cost_analysis.v1.UpdateCustomWidgetRequest.tags', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.cost_analysis.v1.UpdateCustomWidgetRequest.domain_id', index=4,
      number=11, type=9, cpp_type=9, label=1,
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
  serialized_start=352,
  serialized_end=519,
)


_CUSTOMWIDGETREQUEST = _descriptor.Descriptor(
  name='CustomWidgetRequest',
  full_name='spaceone.api.cost_analysis.v1.CustomWidgetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='custom_widget_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetRequest.custom_widget_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetRequest.domain_id', index=1,
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
  ],
  serialized_start=521,
  serialized_end=587,
)


_GETCUSTOMWIDGETREQUEST = _descriptor.Descriptor(
  name='GetCustomWidgetRequest',
  full_name='spaceone.api.cost_analysis.v1.GetCustomWidgetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='custom_widget_id', full_name='spaceone.api.cost_analysis.v1.GetCustomWidgetRequest.custom_widget_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.cost_analysis.v1.GetCustomWidgetRequest.domain_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='only', full_name='spaceone.api.cost_analysis.v1.GetCustomWidgetRequest.only', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=589,
  serialized_end=672,
)


_CUSTOMWIDGETQUERY = _descriptor.Descriptor(
  name='CustomWidgetQuery',
  full_name='spaceone.api.cost_analysis.v1.CustomWidgetQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.cost_analysis.v1.CustomWidgetQuery.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='custom_widget_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetQuery.custom_widget_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.cost_analysis.v1.CustomWidgetQuery.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetQuery.user_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetQuery.domain_id', index=4,
      number=11, type=9, cpp_type=9, label=1,
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
  serialized_start=675,
  serialized_end=814,
)


_CUSTOMWIDGETINFO = _descriptor.Descriptor(
  name='CustomWidgetInfo',
  full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='custom_widget_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo.custom_widget_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='options', full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo.options', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo.tags', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo.user_id', index=4,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo.domain_id', index=5,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo.created_at', index=6,
      number=21, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='updated_at', full_name='spaceone.api.cost_analysis.v1.CustomWidgetInfo.updated_at', index=7,
      number=22, type=9, cpp_type=9, label=1,
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
  serialized_start=817,
  serialized_end=1032,
)


_CUSTOMWIDGETSINFO = _descriptor.Descriptor(
  name='CustomWidgetsInfo',
  full_name='spaceone.api.cost_analysis.v1.CustomWidgetsInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='results', full_name='spaceone.api.cost_analysis.v1.CustomWidgetsInfo.results', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_count', full_name='spaceone.api.cost_analysis.v1.CustomWidgetsInfo.total_count', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=1034,
  serialized_end=1140,
)


_CUSTOMWIDGETSTATQUERY = _descriptor.Descriptor(
  name='CustomWidgetStatQuery',
  full_name='spaceone.api.cost_analysis.v1.CustomWidgetStatQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='spaceone.api.cost_analysis.v1.CustomWidgetStatQuery.query', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domain_id', full_name='spaceone.api.cost_analysis.v1.CustomWidgetStatQuery.domain_id', index=1,
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
  ],
  serialized_start=1142,
  serialized_end=1238,
)

_CREATECUSTOMWIDGETREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_CREATECUSTOMWIDGETREQUEST.fields_by_name['tags'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_UPDATECUSTOMWIDGETREQUEST.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_UPDATECUSTOMWIDGETREQUEST.fields_by_name['tags'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_CUSTOMWIDGETQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._QUERY
_CUSTOMWIDGETINFO.fields_by_name['options'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_CUSTOMWIDGETINFO.fields_by_name['tags'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_CUSTOMWIDGETSINFO.fields_by_name['results'].message_type = _CUSTOMWIDGETINFO
_CUSTOMWIDGETSTATQUERY.fields_by_name['query'].message_type = spaceone_dot_api_dot_core_dot_v1_dot_query__pb2._STATISTICSQUERY
DESCRIPTOR.message_types_by_name['CreateCustomWidgetRequest'] = _CREATECUSTOMWIDGETREQUEST
DESCRIPTOR.message_types_by_name['UpdateCustomWidgetRequest'] = _UPDATECUSTOMWIDGETREQUEST
DESCRIPTOR.message_types_by_name['CustomWidgetRequest'] = _CUSTOMWIDGETREQUEST
DESCRIPTOR.message_types_by_name['GetCustomWidgetRequest'] = _GETCUSTOMWIDGETREQUEST
DESCRIPTOR.message_types_by_name['CustomWidgetQuery'] = _CUSTOMWIDGETQUERY
DESCRIPTOR.message_types_by_name['CustomWidgetInfo'] = _CUSTOMWIDGETINFO
DESCRIPTOR.message_types_by_name['CustomWidgetsInfo'] = _CUSTOMWIDGETSINFO
DESCRIPTOR.message_types_by_name['CustomWidgetStatQuery'] = _CUSTOMWIDGETSTATQUERY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateCustomWidgetRequest = _reflection.GeneratedProtocolMessageType('CreateCustomWidgetRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATECUSTOMWIDGETREQUEST,
  '__module__' : 'spaceone.api.cost_analysis.v1.custom_widget_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CreateCustomWidgetRequest)
  })
_sym_db.RegisterMessage(CreateCustomWidgetRequest)

UpdateCustomWidgetRequest = _reflection.GeneratedProtocolMessageType('UpdateCustomWidgetRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATECUSTOMWIDGETREQUEST,
  '__module__' : 'spaceone.api.cost_analysis.v1.custom_widget_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.UpdateCustomWidgetRequest)
  })
_sym_db.RegisterMessage(UpdateCustomWidgetRequest)

CustomWidgetRequest = _reflection.GeneratedProtocolMessageType('CustomWidgetRequest', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMWIDGETREQUEST,
  '__module__' : 'spaceone.api.cost_analysis.v1.custom_widget_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CustomWidgetRequest)
  })
_sym_db.RegisterMessage(CustomWidgetRequest)

GetCustomWidgetRequest = _reflection.GeneratedProtocolMessageType('GetCustomWidgetRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCUSTOMWIDGETREQUEST,
  '__module__' : 'spaceone.api.cost_analysis.v1.custom_widget_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.GetCustomWidgetRequest)
  })
_sym_db.RegisterMessage(GetCustomWidgetRequest)

CustomWidgetQuery = _reflection.GeneratedProtocolMessageType('CustomWidgetQuery', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMWIDGETQUERY,
  '__module__' : 'spaceone.api.cost_analysis.v1.custom_widget_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CustomWidgetQuery)
  })
_sym_db.RegisterMessage(CustomWidgetQuery)

CustomWidgetInfo = _reflection.GeneratedProtocolMessageType('CustomWidgetInfo', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMWIDGETINFO,
  '__module__' : 'spaceone.api.cost_analysis.v1.custom_widget_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CustomWidgetInfo)
  })
_sym_db.RegisterMessage(CustomWidgetInfo)

CustomWidgetsInfo = _reflection.GeneratedProtocolMessageType('CustomWidgetsInfo', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMWIDGETSINFO,
  '__module__' : 'spaceone.api.cost_analysis.v1.custom_widget_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CustomWidgetsInfo)
  })
_sym_db.RegisterMessage(CustomWidgetsInfo)

CustomWidgetStatQuery = _reflection.GeneratedProtocolMessageType('CustomWidgetStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMWIDGETSTATQUERY,
  '__module__' : 'spaceone.api.cost_analysis.v1.custom_widget_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.cost_analysis.v1.CustomWidgetStatQuery)
  })
_sym_db.RegisterMessage(CustomWidgetStatQuery)



_CUSTOMWIDGET = _descriptor.ServiceDescriptor(
  name='CustomWidget',
  full_name='spaceone.api.cost_analysis.v1.CustomWidget',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1241,
  serialized_end=2241,
  methods=[
  _descriptor.MethodDescriptor(
    name='create',
    full_name='spaceone.api.cost_analysis.v1.CustomWidget.create',
    index=0,
    containing_service=None,
    input_type=_CREATECUSTOMWIDGETREQUEST,
    output_type=_CUSTOMWIDGETINFO,
    serialized_options=b'\202\323\344\223\002\"\" /cost-analysis/v1/custom-widgets',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='update',
    full_name='spaceone.api.cost_analysis.v1.CustomWidget.update',
    index=1,
    containing_service=None,
    input_type=_UPDATECUSTOMWIDGETREQUEST,
    output_type=_CUSTOMWIDGETINFO,
    serialized_options=b'\202\323\344\223\0024\0322/cost-analysis/v1/custom-widget/{custom_widget_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='delete',
    full_name='spaceone.api.cost_analysis.v1.CustomWidget.delete',
    index=2,
    containing_service=None,
    input_type=_CUSTOMWIDGETREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=b'\202\323\344\223\0024*2/cost-analysis/v1/custom-widget/{custom_widget_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get',
    full_name='spaceone.api.cost_analysis.v1.CustomWidget.get',
    index=3,
    containing_service=None,
    input_type=_GETCUSTOMWIDGETREQUEST,
    output_type=_CUSTOMWIDGETINFO,
    serialized_options=b'\202\323\344\223\0024\0222/cost-analysis/v1/custom-widget/{custom_widget_id}',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='list',
    full_name='spaceone.api.cost_analysis.v1.CustomWidget.list',
    index=4,
    containing_service=None,
    input_type=_CUSTOMWIDGETQUERY,
    output_type=_CUSTOMWIDGETSINFO,
    serialized_options=b'\202\323\344\223\002M\022 /cost-analysis/v1/custom-widgetsZ)\"\'/cost-analysis/v1/custom-widgets/search',
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='stat',
    full_name='spaceone.api.cost_analysis.v1.CustomWidget.stat',
    index=5,
    containing_service=None,
    input_type=_CUSTOMWIDGETSTATQUERY,
    output_type=google_dot_protobuf_dot_struct__pb2._STRUCT,
    serialized_options=b'\202\323\344\223\002\'\"%/cost-analysis/v1/custom-widgets/stat',
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CUSTOMWIDGET)

DESCRIPTOR.services_by_name['CustomWidget'] = _CUSTOMWIDGET

# @@protoc_insertion_point(module_scope)
