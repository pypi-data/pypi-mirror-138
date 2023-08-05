# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Trd_UpdateOrderFill.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Common_pb2 as Common__pb2
import Trd_Common_pb2 as Trd__Common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='Trd_UpdateOrderFill.proto',
  package='Trd_UpdateOrderFill',
  syntax='proto2',
  serialized_pb=_b('\n\x19Trd_UpdateOrderFill.proto\x12\x13Trd_UpdateOrderFill\x1a\x0c\x43ommon.proto\x1a\x10Trd_Common.proto\"V\n\x03S2C\x12%\n\x06header\x18\x01 \x02(\x0b\x32\x15.Trd_Common.TrdHeader\x12(\n\torderFill\x18\x02 \x02(\x0b\x32\x15.Trd_Common.OrderFill\"i\n\x08Response\x12\x15\n\x07retType\x18\x01 \x02(\x05:\x04-400\x12\x0e\n\x06retMsg\x18\x02 \x01(\t\x12\x0f\n\x07\x65rrCode\x18\x03 \x01(\x05\x12%\n\x03s2c\x18\x04 \x01(\x0b\x32\x18.Trd_UpdateOrderFill.S2CBI\n\x13\x63om.futu.openapi.pbZ2github.com/futuopen/ftapi4go/pb/trdupdateorderfill')
  ,
  dependencies=[Common__pb2.DESCRIPTOR,Trd__Common__pb2.DESCRIPTOR,])




_S2C = _descriptor.Descriptor(
  name='S2C',
  full_name='Trd_UpdateOrderFill.S2C',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='Trd_UpdateOrderFill.S2C.header', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='orderFill', full_name='Trd_UpdateOrderFill.S2C.orderFill', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=82,
  serialized_end=168,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='Trd_UpdateOrderFill.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='retType', full_name='Trd_UpdateOrderFill.Response.retType', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=True, default_value=-400,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='retMsg', full_name='Trd_UpdateOrderFill.Response.retMsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errCode', full_name='Trd_UpdateOrderFill.Response.errCode', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='s2c', full_name='Trd_UpdateOrderFill.Response.s2c', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=170,
  serialized_end=275,
)

_S2C.fields_by_name['header'].message_type = Trd__Common__pb2._TRDHEADER
_S2C.fields_by_name['orderFill'].message_type = Trd__Common__pb2._ORDERFILL
_RESPONSE.fields_by_name['s2c'].message_type = _S2C
DESCRIPTOR.message_types_by_name['S2C'] = _S2C
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

S2C = _reflection.GeneratedProtocolMessageType('S2C', (_message.Message,), dict(
  DESCRIPTOR = _S2C,
  __module__ = 'Trd_UpdateOrderFill_pb2'
  # @@protoc_insertion_point(class_scope:Trd_UpdateOrderFill.S2C)
  ))
_sym_db.RegisterMessage(S2C)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'Trd_UpdateOrderFill_pb2'
  # @@protoc_insertion_point(class_scope:Trd_UpdateOrderFill.Response)
  ))
_sym_db.RegisterMessage(Response)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\023com.futu.openapi.pbZ2github.com/futuopen/ftapi4go/pb/trdupdateorderfill'))
# @@protoc_insertion_point(module_scope)
