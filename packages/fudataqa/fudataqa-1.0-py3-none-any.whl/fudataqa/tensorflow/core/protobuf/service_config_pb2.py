# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/service_config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/protobuf/service_config.proto',
  package='tensorflow.data.experimental',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-tensorflow/core/protobuf/service_config.proto\x12\x1ctensorflow.data.experimental\"\x9e\x01\n\x10\x44ispatcherConfig\x12\x0c\n\x04port\x18\x01 \x01(\x03\x12\x10\n\x08protocol\x18\x02 \x01(\t\x12\x10\n\x08work_dir\x18\x03 \x01(\t\x12\x1b\n\x13\x66\x61ult_tolerant_mode\x18\x04 \x01(\x08\x12 \n\x18job_gc_check_interval_ms\x18\x05 \x01(\x03\x12\x19\n\x11job_gc_timeout_ms\x18\x06 \x01(\x03\"\xa0\x01\n\x0cWorkerConfig\x12\x0c\n\x04port\x18\x01 \x01(\x03\x12\x10\n\x08protocol\x18\x02 \x01(\t\x12\x1a\n\x12\x64ispatcher_address\x18\x03 \x01(\t\x12\x16\n\x0eworker_address\x18\x04 \x01(\t\x12\x1d\n\x15heartbeat_interval_ms\x18\x05 \x01(\x03\x12\x1d\n\x15\x64ispatcher_timeout_ms\x18\x06 \x01(\x03\x62\x06proto3'
)




_DISPATCHERCONFIG = _descriptor.Descriptor(
  name='DispatcherConfig',
  full_name='tensorflow.data.experimental.DispatcherConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='port', full_name='tensorflow.data.experimental.DispatcherConfig.port', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='protocol', full_name='tensorflow.data.experimental.DispatcherConfig.protocol', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='work_dir', full_name='tensorflow.data.experimental.DispatcherConfig.work_dir', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fault_tolerant_mode', full_name='tensorflow.data.experimental.DispatcherConfig.fault_tolerant_mode', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='job_gc_check_interval_ms', full_name='tensorflow.data.experimental.DispatcherConfig.job_gc_check_interval_ms', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='job_gc_timeout_ms', full_name='tensorflow.data.experimental.DispatcherConfig.job_gc_timeout_ms', index=5,
      number=6, type=3, cpp_type=2, label=1,
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
  serialized_start=80,
  serialized_end=238,
)


_WORKERCONFIG = _descriptor.Descriptor(
  name='WorkerConfig',
  full_name='tensorflow.data.experimental.WorkerConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='port', full_name='tensorflow.data.experimental.WorkerConfig.port', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='protocol', full_name='tensorflow.data.experimental.WorkerConfig.protocol', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dispatcher_address', full_name='tensorflow.data.experimental.WorkerConfig.dispatcher_address', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='worker_address', full_name='tensorflow.data.experimental.WorkerConfig.worker_address', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='heartbeat_interval_ms', full_name='tensorflow.data.experimental.WorkerConfig.heartbeat_interval_ms', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dispatcher_timeout_ms', full_name='tensorflow.data.experimental.WorkerConfig.dispatcher_timeout_ms', index=5,
      number=6, type=3, cpp_type=2, label=1,
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
  serialized_start=241,
  serialized_end=401,
)

DESCRIPTOR.message_types_by_name['DispatcherConfig'] = _DISPATCHERCONFIG
DESCRIPTOR.message_types_by_name['WorkerConfig'] = _WORKERCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DispatcherConfig = _reflection.GeneratedProtocolMessageType('DispatcherConfig', (_message.Message,), {
  'DESCRIPTOR' : _DISPATCHERCONFIG,
  '__module__' : 'tensorflow.core.protobuf.service_config_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.data.experimental.DispatcherConfig)
  })
_sym_db.RegisterMessage(DispatcherConfig)

WorkerConfig = _reflection.GeneratedProtocolMessageType('WorkerConfig', (_message.Message,), {
  'DESCRIPTOR' : _WORKERCONFIG,
  '__module__' : 'tensorflow.core.protobuf.service_config_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.data.experimental.WorkerConfig)
  })
_sym_db.RegisterMessage(WorkerConfig)


# @@protoc_insertion_point(module_scope)
