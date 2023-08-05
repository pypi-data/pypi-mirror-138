# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: continual/rpc/graphql/options.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='continual/rpc/graphql/options.proto',
  package='continual.rpc.graphql',
  syntax='proto3',
  serialized_options=b'Z>github.com/continualiq/continual/continual/rpc/graphql;graphql',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n#continual/rpc/graphql/options.proto\x12\x15\x63ontinual.rpc.graphql\x1a google/protobuf/descriptor.proto*8\n\x13GraphQLFieldOptions\x12\t\n\x05INPUT\x10\x00\x12\n\n\x06OUTPUT\x10\x01\x12\n\n\x06IGNORE\x10\x02:[\n\x07options\x12\x1d.google.protobuf.FieldOptions\x18\xd7\x08 \x01(\x0e\x32*.continual.rpc.graphql.GraphQLFieldOptions:1\n\treference\x12\x1d.google.protobuf.FieldOptions\x18\xd8\x08 \x01(\t:.\n\x05\x65\x64ges\x12\x1e.google.protobuf.MethodOptions\x18\xd9\x08 \x01(\t:0\n\x07parents\x12\x1e.google.protobuf.MethodOptions\x18\xda\x08 \x01(\t:4\n\x0bpassthrough\x12\x1e.google.protobuf.MethodOptions\x18\xdb\x08 \x01(\t:2\n\tedge_only\x12\x1e.google.protobuf.MethodOptions\x18\xdc\x08 \x01(\x08:/\n\x06ignore\x12\x1e.google.protobuf.MethodOptions\x18\xdd\x08 \x01(\x08\x42@Z>github.com/continualiq/continual/continual/rpc/graphql;graphqlb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])

_GRAPHQLFIELDOPTIONS = _descriptor.EnumDescriptor(
  name='GraphQLFieldOptions',
  full_name='continual.rpc.graphql.GraphQLFieldOptions',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INPUT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OUTPUT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='IGNORE', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=96,
  serialized_end=152,
)
_sym_db.RegisterEnumDescriptor(_GRAPHQLFIELDOPTIONS)

GraphQLFieldOptions = enum_type_wrapper.EnumTypeWrapper(_GRAPHQLFIELDOPTIONS)
INPUT = 0
OUTPUT = 1
IGNORE = 2

OPTIONS_FIELD_NUMBER = 1111
options = _descriptor.FieldDescriptor(
  name='options', full_name='continual.rpc.graphql.options', index=0,
  number=1111, type=14, cpp_type=8, label=1,
  has_default_value=False, default_value=0,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)
REFERENCE_FIELD_NUMBER = 1112
reference = _descriptor.FieldDescriptor(
  name='reference', full_name='continual.rpc.graphql.reference', index=1,
  number=1112, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=b"".decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)
EDGES_FIELD_NUMBER = 1113
edges = _descriptor.FieldDescriptor(
  name='edges', full_name='continual.rpc.graphql.edges', index=2,
  number=1113, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=b"".decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)
PARENTS_FIELD_NUMBER = 1114
parents = _descriptor.FieldDescriptor(
  name='parents', full_name='continual.rpc.graphql.parents', index=3,
  number=1114, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=b"".decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)
PASSTHROUGH_FIELD_NUMBER = 1115
passthrough = _descriptor.FieldDescriptor(
  name='passthrough', full_name='continual.rpc.graphql.passthrough', index=4,
  number=1115, type=9, cpp_type=9, label=1,
  has_default_value=False, default_value=b"".decode('utf-8'),
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)
EDGE_ONLY_FIELD_NUMBER = 1116
edge_only = _descriptor.FieldDescriptor(
  name='edge_only', full_name='continual.rpc.graphql.edge_only', index=5,
  number=1116, type=8, cpp_type=7, label=1,
  has_default_value=False, default_value=False,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)
IGNORE_FIELD_NUMBER = 1117
ignore = _descriptor.FieldDescriptor(
  name='ignore', full_name='continual.rpc.graphql.ignore', index=6,
  number=1117, type=8, cpp_type=7, label=1,
  has_default_value=False, default_value=False,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)

DESCRIPTOR.enum_types_by_name['GraphQLFieldOptions'] = _GRAPHQLFIELDOPTIONS
DESCRIPTOR.extensions_by_name['options'] = options
DESCRIPTOR.extensions_by_name['reference'] = reference
DESCRIPTOR.extensions_by_name['edges'] = edges
DESCRIPTOR.extensions_by_name['parents'] = parents
DESCRIPTOR.extensions_by_name['passthrough'] = passthrough
DESCRIPTOR.extensions_by_name['edge_only'] = edge_only
DESCRIPTOR.extensions_by_name['ignore'] = ignore
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

options.enum_type = _GRAPHQLFIELDOPTIONS
google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(options)
google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(reference)
google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(edges)
google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(parents)
google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(passthrough)
google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(edge_only)
google_dot_protobuf_dot_descriptor__pb2.MethodOptions.RegisterExtension(ignore)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
