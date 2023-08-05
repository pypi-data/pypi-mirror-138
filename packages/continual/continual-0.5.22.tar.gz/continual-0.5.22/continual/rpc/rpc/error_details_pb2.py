# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: continual/rpc/rpc/error_details.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='continual/rpc/rpc/error_details.proto',
  package='continual.rpc.rpc',
  syntax='proto3',
  serialized_options=b'Z6github.com/continualiq/continual/continual/rpc/rpc;rpc',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%continual/rpc/rpc/error_details.proto\x12\x11\x63ontinual.rpc.rpc\"}\n\x0c\x45rrorDetails\x12=\n\x07\x64\x65tails\x18\x01 \x03(\x0b\x32,.continual.rpc.rpc.ErrorDetails.DetailsEntry\x1a.\n\x0c\x44\x65tailsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x38Z6github.com/continualiq/continual/continual/rpc/rpc;rpcb\x06proto3'
)




_ERRORDETAILS_DETAILSENTRY = _descriptor.Descriptor(
  name='DetailsEntry',
  full_name='continual.rpc.rpc.ErrorDetails.DetailsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='continual.rpc.rpc.ErrorDetails.DetailsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='continual.rpc.rpc.ErrorDetails.DetailsEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=139,
  serialized_end=185,
)

_ERRORDETAILS = _descriptor.Descriptor(
  name='ErrorDetails',
  full_name='continual.rpc.rpc.ErrorDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='details', full_name='continual.rpc.rpc.ErrorDetails.details', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_ERRORDETAILS_DETAILSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=185,
)

_ERRORDETAILS_DETAILSENTRY.containing_type = _ERRORDETAILS
_ERRORDETAILS.fields_by_name['details'].message_type = _ERRORDETAILS_DETAILSENTRY
DESCRIPTOR.message_types_by_name['ErrorDetails'] = _ERRORDETAILS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ErrorDetails = _reflection.GeneratedProtocolMessageType('ErrorDetails', (_message.Message,), {

  'DetailsEntry' : _reflection.GeneratedProtocolMessageType('DetailsEntry', (_message.Message,), {
    'DESCRIPTOR' : _ERRORDETAILS_DETAILSENTRY,
    '__module__' : 'continual.rpc.rpc.error_details_pb2'
    # @@protoc_insertion_point(class_scope:continual.rpc.rpc.ErrorDetails.DetailsEntry)
    })
  ,
  'DESCRIPTOR' : _ERRORDETAILS,
  '__module__' : 'continual.rpc.rpc.error_details_pb2'
  # @@protoc_insertion_point(class_scope:continual.rpc.rpc.ErrorDetails)
  })
_sym_db.RegisterMessage(ErrorDetails)
_sym_db.RegisterMessage(ErrorDetails.DetailsEntry)


DESCRIPTOR._options = None
_ERRORDETAILS_DETAILSENTRY._options = None
# @@protoc_insertion_point(module_scope)
