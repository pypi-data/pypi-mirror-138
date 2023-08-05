# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: strmprivacy/api/consent_levels/v1/consent_levels_v1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from strmprivacy.api.entities.v1 import entities_v1_pb2 as strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='strmprivacy/api/consent_levels/v1/consent_levels_v1.proto',
  package='strmprivacy.api.consent_levels.v1',
  syntax='proto3',
  serialized_options=b'\n$io.strmprivacy.api.consent_levels.v1P\001ZQgithub.com/strmprivacy/api-definitions-go/v2/api/consent_levels/v1;consent_levels',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n9strmprivacy/api/consent_levels/v1/consent_levels_v1.proto\x12!strmprivacy.api.consent_levels.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a-strmprivacy/api/entities/v1/entities_v1.proto\"5\n\x1fListConsentLevelMappingsRequest\x12\x12\n\nbilling_id\x18\x01 \x01(\t\"t\n ListConsentLevelMappingsResponse\x12P\n\x16\x63onsent_level_mappings\x18\x01 \x03(\x0b\x32\x30.strmprivacy.api.entities.v1.ConsentLevelMapping\"i\n DeleteConsentLevelMappingRequest\x12\x45\n\x03ref\x18\x01 \x01(\x0b\x32\x33.strmprivacy.api.entities.v1.ConsentLevelMappingRefB\x03\xe0\x41\x02\"#\n!DeleteConsentLevelMappingResponse\"s\n CreateConsentLevelMappingRequest\x12O\n\x15\x63onsent_level_mapping\x18\x01 \x01(\x0b\x32\x30.strmprivacy.api.entities.v1.ConsentLevelMapping\"t\n!CreateConsentLevelMappingResponse\x12O\n\x15\x63onsent_level_mapping\x18\x01 \x01(\x0b\x32\x30.strmprivacy.api.entities.v1.ConsentLevelMapping\"f\n\x1dGetConsentLevelMappingRequest\x12\x45\n\x03ref\x18\x01 \x01(\x0b\x32\x33.strmprivacy.api.entities.v1.ConsentLevelMappingRefB\x03\xe0\x41\x02\"q\n\x1eGetConsentLevelMappingResponse\x12O\n\x15\x63onsent_level_mapping\x18\x01 \x01(\x0b\x32\x30.strmprivacy.api.entities.v1.ConsentLevelMapping2\xb5\x05\n\x1b\x43onsentLevelMappingsService\x12\xa3\x01\n\x18ListConsentLevelMappings\x12\x42.strmprivacy.api.consent_levels.v1.ListConsentLevelMappingsRequest\x1a\x43.strmprivacy.api.consent_levels.v1.ListConsentLevelMappingsResponse\x12\x9d\x01\n\x16GetConsentLevelMapping\x12@.strmprivacy.api.consent_levels.v1.GetConsentLevelMappingRequest\x1a\x41.strmprivacy.api.consent_levels.v1.GetConsentLevelMappingResponse\x12\xa6\x01\n\x19\x44\x65leteConsentLevelMapping\x12\x43.strmprivacy.api.consent_levels.v1.DeleteConsentLevelMappingRequest\x1a\x44.strmprivacy.api.consent_levels.v1.DeleteConsentLevelMappingResponse\x12\xa6\x01\n\x19\x43reateConsentLevelMapping\x12\x43.strmprivacy.api.consent_levels.v1.CreateConsentLevelMappingRequest\x1a\x44.strmprivacy.api.consent_levels.v1.CreateConsentLevelMappingResponseB{\n$io.strmprivacy.api.consent_levels.v1P\x01ZQgithub.com/strmprivacy/api-definitions-go/v2/api/consent_levels/v1;consent_levelsb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2.DESCRIPTOR,])




_LISTCONSENTLEVELMAPPINGSREQUEST = _descriptor.Descriptor(
  name='ListConsentLevelMappingsRequest',
  full_name='strmprivacy.api.consent_levels.v1.ListConsentLevelMappingsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='strmprivacy.api.consent_levels.v1.ListConsentLevelMappingsRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=176,
  serialized_end=229,
)


_LISTCONSENTLEVELMAPPINGSRESPONSE = _descriptor.Descriptor(
  name='ListConsentLevelMappingsResponse',
  full_name='strmprivacy.api.consent_levels.v1.ListConsentLevelMappingsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='consent_level_mappings', full_name='strmprivacy.api.consent_levels.v1.ListConsentLevelMappingsResponse.consent_level_mappings', index=0,
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
  serialized_start=231,
  serialized_end=347,
)


_DELETECONSENTLEVELMAPPINGREQUEST = _descriptor.Descriptor(
  name='DeleteConsentLevelMappingRequest',
  full_name='strmprivacy.api.consent_levels.v1.DeleteConsentLevelMappingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ref', full_name='strmprivacy.api.consent_levels.v1.DeleteConsentLevelMappingRequest.ref', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=349,
  serialized_end=454,
)


_DELETECONSENTLEVELMAPPINGRESPONSE = _descriptor.Descriptor(
  name='DeleteConsentLevelMappingResponse',
  full_name='strmprivacy.api.consent_levels.v1.DeleteConsentLevelMappingResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=456,
  serialized_end=491,
)


_CREATECONSENTLEVELMAPPINGREQUEST = _descriptor.Descriptor(
  name='CreateConsentLevelMappingRequest',
  full_name='strmprivacy.api.consent_levels.v1.CreateConsentLevelMappingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='consent_level_mapping', full_name='strmprivacy.api.consent_levels.v1.CreateConsentLevelMappingRequest.consent_level_mapping', index=0,
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
  serialized_start=493,
  serialized_end=608,
)


_CREATECONSENTLEVELMAPPINGRESPONSE = _descriptor.Descriptor(
  name='CreateConsentLevelMappingResponse',
  full_name='strmprivacy.api.consent_levels.v1.CreateConsentLevelMappingResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='consent_level_mapping', full_name='strmprivacy.api.consent_levels.v1.CreateConsentLevelMappingResponse.consent_level_mapping', index=0,
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
  serialized_start=610,
  serialized_end=726,
)


_GETCONSENTLEVELMAPPINGREQUEST = _descriptor.Descriptor(
  name='GetConsentLevelMappingRequest',
  full_name='strmprivacy.api.consent_levels.v1.GetConsentLevelMappingRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ref', full_name='strmprivacy.api.consent_levels.v1.GetConsentLevelMappingRequest.ref', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=728,
  serialized_end=830,
)


_GETCONSENTLEVELMAPPINGRESPONSE = _descriptor.Descriptor(
  name='GetConsentLevelMappingResponse',
  full_name='strmprivacy.api.consent_levels.v1.GetConsentLevelMappingResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='consent_level_mapping', full_name='strmprivacy.api.consent_levels.v1.GetConsentLevelMappingResponse.consent_level_mapping', index=0,
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
  serialized_start=832,
  serialized_end=945,
)

_LISTCONSENTLEVELMAPPINGSRESPONSE.fields_by_name['consent_level_mappings'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._CONSENTLEVELMAPPING
_DELETECONSENTLEVELMAPPINGREQUEST.fields_by_name['ref'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._CONSENTLEVELMAPPINGREF
_CREATECONSENTLEVELMAPPINGREQUEST.fields_by_name['consent_level_mapping'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._CONSENTLEVELMAPPING
_CREATECONSENTLEVELMAPPINGRESPONSE.fields_by_name['consent_level_mapping'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._CONSENTLEVELMAPPING
_GETCONSENTLEVELMAPPINGREQUEST.fields_by_name['ref'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._CONSENTLEVELMAPPINGREF
_GETCONSENTLEVELMAPPINGRESPONSE.fields_by_name['consent_level_mapping'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._CONSENTLEVELMAPPING
DESCRIPTOR.message_types_by_name['ListConsentLevelMappingsRequest'] = _LISTCONSENTLEVELMAPPINGSREQUEST
DESCRIPTOR.message_types_by_name['ListConsentLevelMappingsResponse'] = _LISTCONSENTLEVELMAPPINGSRESPONSE
DESCRIPTOR.message_types_by_name['DeleteConsentLevelMappingRequest'] = _DELETECONSENTLEVELMAPPINGREQUEST
DESCRIPTOR.message_types_by_name['DeleteConsentLevelMappingResponse'] = _DELETECONSENTLEVELMAPPINGRESPONSE
DESCRIPTOR.message_types_by_name['CreateConsentLevelMappingRequest'] = _CREATECONSENTLEVELMAPPINGREQUEST
DESCRIPTOR.message_types_by_name['CreateConsentLevelMappingResponse'] = _CREATECONSENTLEVELMAPPINGRESPONSE
DESCRIPTOR.message_types_by_name['GetConsentLevelMappingRequest'] = _GETCONSENTLEVELMAPPINGREQUEST
DESCRIPTOR.message_types_by_name['GetConsentLevelMappingResponse'] = _GETCONSENTLEVELMAPPINGRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListConsentLevelMappingsRequest = _reflection.GeneratedProtocolMessageType('ListConsentLevelMappingsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTCONSENTLEVELMAPPINGSREQUEST,
  '__module__' : 'strmprivacy.api.consent_levels.v1.consent_levels_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.consent_levels.v1.ListConsentLevelMappingsRequest)
  })
_sym_db.RegisterMessage(ListConsentLevelMappingsRequest)

ListConsentLevelMappingsResponse = _reflection.GeneratedProtocolMessageType('ListConsentLevelMappingsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTCONSENTLEVELMAPPINGSRESPONSE,
  '__module__' : 'strmprivacy.api.consent_levels.v1.consent_levels_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.consent_levels.v1.ListConsentLevelMappingsResponse)
  })
_sym_db.RegisterMessage(ListConsentLevelMappingsResponse)

DeleteConsentLevelMappingRequest = _reflection.GeneratedProtocolMessageType('DeleteConsentLevelMappingRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETECONSENTLEVELMAPPINGREQUEST,
  '__module__' : 'strmprivacy.api.consent_levels.v1.consent_levels_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.consent_levels.v1.DeleteConsentLevelMappingRequest)
  })
_sym_db.RegisterMessage(DeleteConsentLevelMappingRequest)

DeleteConsentLevelMappingResponse = _reflection.GeneratedProtocolMessageType('DeleteConsentLevelMappingResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETECONSENTLEVELMAPPINGRESPONSE,
  '__module__' : 'strmprivacy.api.consent_levels.v1.consent_levels_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.consent_levels.v1.DeleteConsentLevelMappingResponse)
  })
_sym_db.RegisterMessage(DeleteConsentLevelMappingResponse)

CreateConsentLevelMappingRequest = _reflection.GeneratedProtocolMessageType('CreateConsentLevelMappingRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATECONSENTLEVELMAPPINGREQUEST,
  '__module__' : 'strmprivacy.api.consent_levels.v1.consent_levels_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.consent_levels.v1.CreateConsentLevelMappingRequest)
  })
_sym_db.RegisterMessage(CreateConsentLevelMappingRequest)

CreateConsentLevelMappingResponse = _reflection.GeneratedProtocolMessageType('CreateConsentLevelMappingResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATECONSENTLEVELMAPPINGRESPONSE,
  '__module__' : 'strmprivacy.api.consent_levels.v1.consent_levels_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.consent_levels.v1.CreateConsentLevelMappingResponse)
  })
_sym_db.RegisterMessage(CreateConsentLevelMappingResponse)

GetConsentLevelMappingRequest = _reflection.GeneratedProtocolMessageType('GetConsentLevelMappingRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETCONSENTLEVELMAPPINGREQUEST,
  '__module__' : 'strmprivacy.api.consent_levels.v1.consent_levels_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.consent_levels.v1.GetConsentLevelMappingRequest)
  })
_sym_db.RegisterMessage(GetConsentLevelMappingRequest)

GetConsentLevelMappingResponse = _reflection.GeneratedProtocolMessageType('GetConsentLevelMappingResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETCONSENTLEVELMAPPINGRESPONSE,
  '__module__' : 'strmprivacy.api.consent_levels.v1.consent_levels_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.consent_levels.v1.GetConsentLevelMappingResponse)
  })
_sym_db.RegisterMessage(GetConsentLevelMappingResponse)


DESCRIPTOR._options = None
_DELETECONSENTLEVELMAPPINGREQUEST.fields_by_name['ref']._options = None
_GETCONSENTLEVELMAPPINGREQUEST.fields_by_name['ref']._options = None

_CONSENTLEVELMAPPINGSSERVICE = _descriptor.ServiceDescriptor(
  name='ConsentLevelMappingsService',
  full_name='strmprivacy.api.consent_levels.v1.ConsentLevelMappingsService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=948,
  serialized_end=1641,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListConsentLevelMappings',
    full_name='strmprivacy.api.consent_levels.v1.ConsentLevelMappingsService.ListConsentLevelMappings',
    index=0,
    containing_service=None,
    input_type=_LISTCONSENTLEVELMAPPINGSREQUEST,
    output_type=_LISTCONSENTLEVELMAPPINGSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetConsentLevelMapping',
    full_name='strmprivacy.api.consent_levels.v1.ConsentLevelMappingsService.GetConsentLevelMapping',
    index=1,
    containing_service=None,
    input_type=_GETCONSENTLEVELMAPPINGREQUEST,
    output_type=_GETCONSENTLEVELMAPPINGRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteConsentLevelMapping',
    full_name='strmprivacy.api.consent_levels.v1.ConsentLevelMappingsService.DeleteConsentLevelMapping',
    index=2,
    containing_service=None,
    input_type=_DELETECONSENTLEVELMAPPINGREQUEST,
    output_type=_DELETECONSENTLEVELMAPPINGRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateConsentLevelMapping',
    full_name='strmprivacy.api.consent_levels.v1.ConsentLevelMappingsService.CreateConsentLevelMapping',
    index=3,
    containing_service=None,
    input_type=_CREATECONSENTLEVELMAPPINGREQUEST,
    output_type=_CREATECONSENTLEVELMAPPINGRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CONSENTLEVELMAPPINGSSERVICE)

DESCRIPTOR.services_by_name['ConsentLevelMappingsService'] = _CONSENTLEVELMAPPINGSSERVICE

# @@protoc_insertion_point(module_scope)
