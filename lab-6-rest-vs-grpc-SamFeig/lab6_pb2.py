# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lab6.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='lab6.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\nlab6.proto\"\x1e\n\x06\x61\x64\x64Msg\x12\t\n\x01\x61\x18\x01 \x01(\x05\x12\t\n\x01\x62\x18\x02 \x01(\x05\"\x17\n\x08imageMsg\x12\x0b\n\x03img\x18\x01 \x01(\x0c\x32 \n\x03\x61\x64\x64\x12\x19\n\x03\x61\x64\x64\x12\x07.addMsg\x1a\x07.addMsg\"\x00\x32&\n\x05image\x12\x1d\n\x05image\x12\t.imageMsg\x1a\x07.addMsg\"\x00\x62\x06proto3'
)




_ADDMSG = _descriptor.Descriptor(
  name='addMsg',
  full_name='addMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='a', full_name='addMsg.a', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='b', full_name='addMsg.b', index=1,
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
  serialized_start=14,
  serialized_end=44,
)


_IMAGEMSG = _descriptor.Descriptor(
  name='imageMsg',
  full_name='imageMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='img', full_name='imageMsg.img', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=46,
  serialized_end=69,
)

DESCRIPTOR.message_types_by_name['addMsg'] = _ADDMSG
DESCRIPTOR.message_types_by_name['imageMsg'] = _IMAGEMSG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

addMsg = _reflection.GeneratedProtocolMessageType('addMsg', (_message.Message,), {
  'DESCRIPTOR' : _ADDMSG,
  '__module__' : 'lab6_pb2'
  # @@protoc_insertion_point(class_scope:addMsg)
  })
_sym_db.RegisterMessage(addMsg)

imageMsg = _reflection.GeneratedProtocolMessageType('imageMsg', (_message.Message,), {
  'DESCRIPTOR' : _IMAGEMSG,
  '__module__' : 'lab6_pb2'
  # @@protoc_insertion_point(class_scope:imageMsg)
  })
_sym_db.RegisterMessage(imageMsg)



_ADD = _descriptor.ServiceDescriptor(
  name='add',
  full_name='add',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=71,
  serialized_end=103,
  methods=[
  _descriptor.MethodDescriptor(
    name='add',
    full_name='add.add',
    index=0,
    containing_service=None,
    input_type=_ADDMSG,
    output_type=_ADDMSG,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ADD)

DESCRIPTOR.services_by_name['add'] = _ADD


_IMAGE = _descriptor.ServiceDescriptor(
  name='image',
  full_name='image',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=105,
  serialized_end=143,
  methods=[
  _descriptor.MethodDescriptor(
    name='image',
    full_name='image.image',
    index=0,
    containing_service=None,
    input_type=_IMAGEMSG,
    output_type=_ADDMSG,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_IMAGE)

DESCRIPTOR.services_by_name['image'] = _IMAGE

# @@protoc_insertion_point(module_scope)
