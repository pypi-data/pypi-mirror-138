# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/framework/kernel_def.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fudataqa.tensorflow.core.framework import attr_value_pb2 as tensorflow_dot_core_dot_framework_dot_attr__value__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/framework/kernel_def.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=b'\n\030org.tensorflow.frameworkB\017KernelDefProtosP\001ZQgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/kernel_def_go_proto\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n*tensorflow/core/framework/kernel_def.proto\x12\ntensorflow\x1a*tensorflow/core/framework/attr_value.proto\"\xef\x01\n\tKernelDef\x12\n\n\x02op\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x02 \x01(\t\x12\x38\n\nconstraint\x18\x03 \x03(\x0b\x32$.tensorflow.KernelDef.AttrConstraint\x12\x17\n\x0fhost_memory_arg\x18\x04 \x03(\t\x12\r\n\x05label\x18\x05 \x01(\t\x12\x10\n\x08priority\x18\x06 \x01(\x05\x1aM\n\x0e\x41ttrConstraint\x12\x0c\n\x04name\x18\x01 \x01(\t\x12-\n\x0e\x61llowed_values\x18\x02 \x01(\x0b\x32\x15.tensorflow.AttrValue\"3\n\nKernelList\x12%\n\x06kernel\x18\x01 \x03(\x0b\x32\x15.tensorflow.KernelDefB\x83\x01\n\x18org.tensorflow.frameworkB\x0fKernelDefProtosP\x01ZQgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/kernel_def_go_proto\xf8\x01\x01\x62\x06proto3'
  ,
  dependencies=[tensorflow_dot_core_dot_framework_dot_attr__value__pb2.DESCRIPTOR,])




_KERNELDEF_ATTRCONSTRAINT = _descriptor.Descriptor(
  name='AttrConstraint',
  full_name='tensorflow.KernelDef.AttrConstraint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.KernelDef.AttrConstraint.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='allowed_values', full_name='tensorflow.KernelDef.AttrConstraint.allowed_values', index=1,
      number=2, type=11, cpp_type=10, label=1,
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
  serialized_start=265,
  serialized_end=342,
)

_KERNELDEF = _descriptor.Descriptor(
  name='KernelDef',
  full_name='tensorflow.KernelDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='op', full_name='tensorflow.KernelDef.op', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device_type', full_name='tensorflow.KernelDef.device_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='constraint', full_name='tensorflow.KernelDef.constraint', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='host_memory_arg', full_name='tensorflow.KernelDef.host_memory_arg', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='label', full_name='tensorflow.KernelDef.label', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='priority', full_name='tensorflow.KernelDef.priority', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_KERNELDEF_ATTRCONSTRAINT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=103,
  serialized_end=342,
)


_KERNELLIST = _descriptor.Descriptor(
  name='KernelList',
  full_name='tensorflow.KernelList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='kernel', full_name='tensorflow.KernelList.kernel', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=344,
  serialized_end=395,
)

_KERNELDEF_ATTRCONSTRAINT.fields_by_name['allowed_values'].message_type = tensorflow_dot_core_dot_framework_dot_attr__value__pb2._ATTRVALUE
_KERNELDEF_ATTRCONSTRAINT.containing_type = _KERNELDEF
_KERNELDEF.fields_by_name['constraint'].message_type = _KERNELDEF_ATTRCONSTRAINT
_KERNELLIST.fields_by_name['kernel'].message_type = _KERNELDEF
DESCRIPTOR.message_types_by_name['KernelDef'] = _KERNELDEF
DESCRIPTOR.message_types_by_name['KernelList'] = _KERNELLIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

KernelDef = _reflection.GeneratedProtocolMessageType('KernelDef', (_message.Message,), {

  'AttrConstraint' : _reflection.GeneratedProtocolMessageType('AttrConstraint', (_message.Message,), {
    'DESCRIPTOR' : _KERNELDEF_ATTRCONSTRAINT,
    '__module__' : 'tensorflow.core.framework.kernel_def_pb2'
    # @@protoc_insertion_point(class_scope:tensorflow.KernelDef.AttrConstraint)
    })
  ,
  'DESCRIPTOR' : _KERNELDEF,
  '__module__' : 'tensorflow.core.framework.kernel_def_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.KernelDef)
  })
_sym_db.RegisterMessage(KernelDef)
_sym_db.RegisterMessage(KernelDef.AttrConstraint)

KernelList = _reflection.GeneratedProtocolMessageType('KernelList', (_message.Message,), {
  'DESCRIPTOR' : _KERNELLIST,
  '__module__' : 'tensorflow.core.framework.kernel_def_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.KernelList)
  })
_sym_db.RegisterMessage(KernelList)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
