# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: notification.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'notification.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12notification.proto\x12\x0cnotification\"K\n\x17SendNotificationRequest\x12\x11\n\tusuarioId\x18\x01 \x01(\t\x12\x0f\n\x07mensaje\x18\x02 \x01(\t\x12\x0c\n\x04tipo\x18\x03 \x01(\t\"p\n\x0cNotification\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tusuarioId\x18\x02 \x01(\t\x12\x0f\n\x07mensaje\x18\x03 \x01(\t\x12\x0c\n\x04tipo\x18\x04 \x01(\t\x12\x12\n\nfechaEnvio\x18\x05 \x01(\t\x12\x0e\n\x06\x65stado\x18\x06 \x01(\t2l\n\x13NotificationService\x12U\n\x10SendNotification\x12%.notification.SendNotificationRequest\x1a\x1a.notification.Notificationb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'notification_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SENDNOTIFICATIONREQUEST']._serialized_start=36
  _globals['_SENDNOTIFICATIONREQUEST']._serialized_end=111
  _globals['_NOTIFICATION']._serialized_start=113
  _globals['_NOTIFICATION']._serialized_end=225
  _globals['_NOTIFICATIONSERVICE']._serialized_start=227
  _globals['_NOTIFICATIONSERVICE']._serialized_end=335
# @@protoc_insertion_point(module_scope)
