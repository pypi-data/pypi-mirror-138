# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: strmprivacy/api/schemas/v1/schemas_v1.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from strmprivacy.api.entities.v1 import entities_v1_pb2 as strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='strmprivacy/api/schemas/v1/schemas_v1.proto',
  package='strmprivacy.api.schemas.v1',
  syntax='proto3',
  serialized_options=b'\n\035io.strmprivacy.api.schemas.v1P\001ZCgithub.com/strmprivacy/api-definitions-go/v2/api/schemas/v1;schemas',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+strmprivacy/api/schemas/v1/schemas_v1.proto\x12\x1astrmprivacy.api.schemas.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a google/protobuf/field_mask.proto\x1a-strmprivacy/api/entities/v1/entities_v1.proto\"\xe4\x02\n\x12ListSchemasRequest\x12\x17\n\nbilling_id\x18\x01 \x01(\tB\x03\xe0\x41\x01\x12\x13\n\x06\x66ilter\x18\x02 \x01(\tB\x03\xe0\x41\x01\x12\x13\n\x06handle\x18\x03 \x01(\tB\x03\xe0\x41\x01\x12\x11\n\x04name\x18\x04 \x01(\tB\x03\xe0\x41\x01\x12M\n\x0epublic_private\x18\x05 \x01(\x0e\x32\x30.strmprivacy.api.entities.v1.FilterPublicPrivateB\x03\xe0\x41\x01\x12\x41\n\x0bschema_type\x18\x06 \x01(\x0e\x32\'.strmprivacy.api.entities.v1.SchemaTypeB\x03\xe0\x41\x01\x12\x37\n\x06labels\x18\x07 \x03(\x0b\x32\".strmprivacy.api.entities.v1.LabelB\x03\xe0\x41\x01\x12\x14\n\x07\x64omains\x18\x08 \x03(\tB\x03\xe0\x41\x01\x12\x17\n\nindustries\x18\t \x03(\tB\x03\xe0\x41\x01\"K\n\x13ListSchemasResponse\x12\x34\n\x07schemas\x18\x01 \x03(\x0b\x32#.strmprivacy.api.entities.v1.Schema\"\x9e\x01\n\x10GetSchemaRequest\x12\x12\n\nbilling_id\x18\x01 \x01(\t\x12\x33\n\x03ref\x18\x02 \x01(\x0b\x32&.strmprivacy.api.entities.v1.SchemaRef\x12\x41\n\x0b\x63luster_ref\x18\x03 \x01(\x0b\x32,.strmprivacy.api.entities.v1.KafkaClusterRef\"u\n\x11GetSchemaResponse\x12\x33\n\x06schema\x18\x01 \x01(\x0b\x32#.strmprivacy.api.entities.v1.Schema\x12\x14\n\x0c\x63onfluent_id\x18\x02 \x01(\x05\x12\x15\n\x08\x63hecksum\x18\x03 \x01(\tB\x03\xe0\x41\x02\"^\n\x13\x43reateSchemaRequest\x12\x12\n\nbilling_id\x18\x01 \x01(\t\x12\x33\n\x06schema\x18\x02 \x01(\x0b\x32#.strmprivacy.api.entities.v1.Schema\"b\n\x14\x43reateSchemaResponse\x12\x33\n\x06schema\x18\x01 \x01(\x0b\x32#.strmprivacy.api.entities.v1.Schema\x12\x15\n\x08\x63hecksum\x18\x02 \x01(\tB\x03\xe0\x41\x03\"\xb5\x01\n\x13UpdateSchemaRequest\x12\x17\n\nbilling_id\x18\x01 \x01(\tB\x03\xe0\x41\x02\x12\x38\n\x06schema\x18\x02 \x01(\x0b\x32#.strmprivacy.api.entities.v1.SchemaB\x03\xe0\x41\x02\x12\x15\n\x08\x63hecksum\x18\x03 \x01(\tB\x03\xe0\x41\x02\x12\x34\n\x0bupdate_mask\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskB\x03\xe0\x41\x02\"b\n\x14UpdateSchemaResponse\x12\x33\n\x06schema\x18\x01 \x01(\x0b\x32#.strmprivacy.api.entities.v1.Schema\x12\x15\n\x08\x63hecksum\x18\x02 \x01(\tB\x03\xe0\x41\x03\"q\n\x14GetSchemaCodeRequest\x12\x12\n\nbilling_id\x18\x01 \x01(\t\x12\x33\n\x03ref\x18\x02 \x01(\x0b\x32&.strmprivacy.api.entities.v1.SchemaRef\x12\x10\n\x08language\x18\x03 \x01(\t\"J\n\x15GetSchemaCodeResponse\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x11\n\tdata_size\x18\x02 \x01(\x03\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x32\xc6\x04\n\x0eSchemasService\x12n\n\x0bListSchemas\x12..strmprivacy.api.schemas.v1.ListSchemasRequest\x1a/.strmprivacy.api.schemas.v1.ListSchemasResponse\x12h\n\tGetSchema\x12,.strmprivacy.api.schemas.v1.GetSchemaRequest\x1a-.strmprivacy.api.schemas.v1.GetSchemaResponse\x12q\n\x0c\x43reateSchema\x12/.strmprivacy.api.schemas.v1.CreateSchemaRequest\x1a\x30.strmprivacy.api.schemas.v1.CreateSchemaResponse\x12q\n\x0cUpdateSchema\x12/.strmprivacy.api.schemas.v1.UpdateSchemaRequest\x1a\x30.strmprivacy.api.schemas.v1.UpdateSchemaResponse\x12t\n\rGetSchemaCode\x12\x30.strmprivacy.api.schemas.v1.GetSchemaCodeRequest\x1a\x31.strmprivacy.api.schemas.v1.GetSchemaCodeResponseBf\n\x1dio.strmprivacy.api.schemas.v1P\x01ZCgithub.com/strmprivacy/api-definitions-go/v2/api/schemas/v1;schemasb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_protobuf_dot_field__mask__pb2.DESCRIPTOR,strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2.DESCRIPTOR,])




_LISTSCHEMASREQUEST = _descriptor.Descriptor(
  name='ListSchemasRequest',
  full_name='strmprivacy.api.schemas.v1.ListSchemasRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filter', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.filter', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='handle', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.handle', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='public_private', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.public_private', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schema_type', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.schema_type', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='labels', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.labels', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='domains', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.domains', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='industries', full_name='strmprivacy.api.schemas.v1.ListSchemasRequest.industries', index=8,
      number=9, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=190,
  serialized_end=546,
)


_LISTSCHEMASRESPONSE = _descriptor.Descriptor(
  name='ListSchemasResponse',
  full_name='strmprivacy.api.schemas.v1.ListSchemasResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='schemas', full_name='strmprivacy.api.schemas.v1.ListSchemasResponse.schemas', index=0,
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
  serialized_start=548,
  serialized_end=623,
)


_GETSCHEMAREQUEST = _descriptor.Descriptor(
  name='GetSchemaRequest',
  full_name='strmprivacy.api.schemas.v1.GetSchemaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='strmprivacy.api.schemas.v1.GetSchemaRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ref', full_name='strmprivacy.api.schemas.v1.GetSchemaRequest.ref', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cluster_ref', full_name='strmprivacy.api.schemas.v1.GetSchemaRequest.cluster_ref', index=2,
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
  serialized_start=626,
  serialized_end=784,
)


_GETSCHEMARESPONSE = _descriptor.Descriptor(
  name='GetSchemaResponse',
  full_name='strmprivacy.api.schemas.v1.GetSchemaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='schema', full_name='strmprivacy.api.schemas.v1.GetSchemaResponse.schema', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='confluent_id', full_name='strmprivacy.api.schemas.v1.GetSchemaResponse.confluent_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='checksum', full_name='strmprivacy.api.schemas.v1.GetSchemaResponse.checksum', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=786,
  serialized_end=903,
)


_CREATESCHEMAREQUEST = _descriptor.Descriptor(
  name='CreateSchemaRequest',
  full_name='strmprivacy.api.schemas.v1.CreateSchemaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='strmprivacy.api.schemas.v1.CreateSchemaRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schema', full_name='strmprivacy.api.schemas.v1.CreateSchemaRequest.schema', index=1,
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
  serialized_start=905,
  serialized_end=999,
)


_CREATESCHEMARESPONSE = _descriptor.Descriptor(
  name='CreateSchemaResponse',
  full_name='strmprivacy.api.schemas.v1.CreateSchemaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='schema', full_name='strmprivacy.api.schemas.v1.CreateSchemaResponse.schema', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='checksum', full_name='strmprivacy.api.schemas.v1.CreateSchemaResponse.checksum', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1001,
  serialized_end=1099,
)


_UPDATESCHEMAREQUEST = _descriptor.Descriptor(
  name='UpdateSchemaRequest',
  full_name='strmprivacy.api.schemas.v1.UpdateSchemaRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='strmprivacy.api.schemas.v1.UpdateSchemaRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='schema', full_name='strmprivacy.api.schemas.v1.UpdateSchemaRequest.schema', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='checksum', full_name='strmprivacy.api.schemas.v1.UpdateSchemaRequest.checksum', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\002', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='update_mask', full_name='strmprivacy.api.schemas.v1.UpdateSchemaRequest.update_mask', index=3,
      number=4, type=11, cpp_type=10, label=1,
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
  serialized_start=1102,
  serialized_end=1283,
)


_UPDATESCHEMARESPONSE = _descriptor.Descriptor(
  name='UpdateSchemaResponse',
  full_name='strmprivacy.api.schemas.v1.UpdateSchemaResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='schema', full_name='strmprivacy.api.schemas.v1.UpdateSchemaResponse.schema', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='checksum', full_name='strmprivacy.api.schemas.v1.UpdateSchemaResponse.checksum', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\340A\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1285,
  serialized_end=1383,
)


_GETSCHEMACODEREQUEST = _descriptor.Descriptor(
  name='GetSchemaCodeRequest',
  full_name='strmprivacy.api.schemas.v1.GetSchemaCodeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billing_id', full_name='strmprivacy.api.schemas.v1.GetSchemaCodeRequest.billing_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ref', full_name='strmprivacy.api.schemas.v1.GetSchemaCodeRequest.ref', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='language', full_name='strmprivacy.api.schemas.v1.GetSchemaCodeRequest.language', index=2,
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
  serialized_start=1385,
  serialized_end=1498,
)


_GETSCHEMACODERESPONSE = _descriptor.Descriptor(
  name='GetSchemaCodeResponse',
  full_name='strmprivacy.api.schemas.v1.GetSchemaCodeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='strmprivacy.api.schemas.v1.GetSchemaCodeResponse.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data_size', full_name='strmprivacy.api.schemas.v1.GetSchemaCodeResponse.data_size', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='strmprivacy.api.schemas.v1.GetSchemaCodeResponse.data', index=2,
      number=3, type=12, cpp_type=9, label=1,
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
  serialized_start=1500,
  serialized_end=1574,
)

_LISTSCHEMASREQUEST.fields_by_name['public_private'].enum_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._FILTERPUBLICPRIVATE
_LISTSCHEMASREQUEST.fields_by_name['schema_type'].enum_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMATYPE
_LISTSCHEMASREQUEST.fields_by_name['labels'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._LABEL
_LISTSCHEMASRESPONSE.fields_by_name['schemas'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMA
_GETSCHEMAREQUEST.fields_by_name['ref'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMAREF
_GETSCHEMAREQUEST.fields_by_name['cluster_ref'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._KAFKACLUSTERREF
_GETSCHEMARESPONSE.fields_by_name['schema'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMA
_CREATESCHEMAREQUEST.fields_by_name['schema'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMA
_CREATESCHEMARESPONSE.fields_by_name['schema'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMA
_UPDATESCHEMAREQUEST.fields_by_name['schema'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMA
_UPDATESCHEMAREQUEST.fields_by_name['update_mask'].message_type = google_dot_protobuf_dot_field__mask__pb2._FIELDMASK
_UPDATESCHEMARESPONSE.fields_by_name['schema'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMA
_GETSCHEMACODEREQUEST.fields_by_name['ref'].message_type = strmprivacy_dot_api_dot_entities_dot_v1_dot_entities__v1__pb2._SCHEMAREF
DESCRIPTOR.message_types_by_name['ListSchemasRequest'] = _LISTSCHEMASREQUEST
DESCRIPTOR.message_types_by_name['ListSchemasResponse'] = _LISTSCHEMASRESPONSE
DESCRIPTOR.message_types_by_name['GetSchemaRequest'] = _GETSCHEMAREQUEST
DESCRIPTOR.message_types_by_name['GetSchemaResponse'] = _GETSCHEMARESPONSE
DESCRIPTOR.message_types_by_name['CreateSchemaRequest'] = _CREATESCHEMAREQUEST
DESCRIPTOR.message_types_by_name['CreateSchemaResponse'] = _CREATESCHEMARESPONSE
DESCRIPTOR.message_types_by_name['UpdateSchemaRequest'] = _UPDATESCHEMAREQUEST
DESCRIPTOR.message_types_by_name['UpdateSchemaResponse'] = _UPDATESCHEMARESPONSE
DESCRIPTOR.message_types_by_name['GetSchemaCodeRequest'] = _GETSCHEMACODEREQUEST
DESCRIPTOR.message_types_by_name['GetSchemaCodeResponse'] = _GETSCHEMACODERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListSchemasRequest = _reflection.GeneratedProtocolMessageType('ListSchemasRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTSCHEMASREQUEST,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.ListSchemasRequest)
  })
_sym_db.RegisterMessage(ListSchemasRequest)

ListSchemasResponse = _reflection.GeneratedProtocolMessageType('ListSchemasResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSCHEMASRESPONSE,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.ListSchemasResponse)
  })
_sym_db.RegisterMessage(ListSchemasResponse)

GetSchemaRequest = _reflection.GeneratedProtocolMessageType('GetSchemaRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSCHEMAREQUEST,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.GetSchemaRequest)
  })
_sym_db.RegisterMessage(GetSchemaRequest)

GetSchemaResponse = _reflection.GeneratedProtocolMessageType('GetSchemaResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSCHEMARESPONSE,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.GetSchemaResponse)
  })
_sym_db.RegisterMessage(GetSchemaResponse)

CreateSchemaRequest = _reflection.GeneratedProtocolMessageType('CreateSchemaRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATESCHEMAREQUEST,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.CreateSchemaRequest)
  })
_sym_db.RegisterMessage(CreateSchemaRequest)

CreateSchemaResponse = _reflection.GeneratedProtocolMessageType('CreateSchemaResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATESCHEMARESPONSE,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.CreateSchemaResponse)
  })
_sym_db.RegisterMessage(CreateSchemaResponse)

UpdateSchemaRequest = _reflection.GeneratedProtocolMessageType('UpdateSchemaRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATESCHEMAREQUEST,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.UpdateSchemaRequest)
  })
_sym_db.RegisterMessage(UpdateSchemaRequest)

UpdateSchemaResponse = _reflection.GeneratedProtocolMessageType('UpdateSchemaResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATESCHEMARESPONSE,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.UpdateSchemaResponse)
  })
_sym_db.RegisterMessage(UpdateSchemaResponse)

GetSchemaCodeRequest = _reflection.GeneratedProtocolMessageType('GetSchemaCodeRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSCHEMACODEREQUEST,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.GetSchemaCodeRequest)
  })
_sym_db.RegisterMessage(GetSchemaCodeRequest)

GetSchemaCodeResponse = _reflection.GeneratedProtocolMessageType('GetSchemaCodeResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSCHEMACODERESPONSE,
  '__module__' : 'strmprivacy.api.schemas.v1.schemas_v1_pb2'
  # @@protoc_insertion_point(class_scope:strmprivacy.api.schemas.v1.GetSchemaCodeResponse)
  })
_sym_db.RegisterMessage(GetSchemaCodeResponse)


DESCRIPTOR._options = None
_LISTSCHEMASREQUEST.fields_by_name['billing_id']._options = None
_LISTSCHEMASREQUEST.fields_by_name['filter']._options = None
_LISTSCHEMASREQUEST.fields_by_name['handle']._options = None
_LISTSCHEMASREQUEST.fields_by_name['name']._options = None
_LISTSCHEMASREQUEST.fields_by_name['public_private']._options = None
_LISTSCHEMASREQUEST.fields_by_name['schema_type']._options = None
_LISTSCHEMASREQUEST.fields_by_name['labels']._options = None
_LISTSCHEMASREQUEST.fields_by_name['domains']._options = None
_LISTSCHEMASREQUEST.fields_by_name['industries']._options = None
_GETSCHEMARESPONSE.fields_by_name['checksum']._options = None
_CREATESCHEMARESPONSE.fields_by_name['checksum']._options = None
_UPDATESCHEMAREQUEST.fields_by_name['billing_id']._options = None
_UPDATESCHEMAREQUEST.fields_by_name['schema']._options = None
_UPDATESCHEMAREQUEST.fields_by_name['checksum']._options = None
_UPDATESCHEMAREQUEST.fields_by_name['update_mask']._options = None
_UPDATESCHEMARESPONSE.fields_by_name['checksum']._options = None

_SCHEMASSERVICE = _descriptor.ServiceDescriptor(
  name='SchemasService',
  full_name='strmprivacy.api.schemas.v1.SchemasService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1577,
  serialized_end=2159,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListSchemas',
    full_name='strmprivacy.api.schemas.v1.SchemasService.ListSchemas',
    index=0,
    containing_service=None,
    input_type=_LISTSCHEMASREQUEST,
    output_type=_LISTSCHEMASRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetSchema',
    full_name='strmprivacy.api.schemas.v1.SchemasService.GetSchema',
    index=1,
    containing_service=None,
    input_type=_GETSCHEMAREQUEST,
    output_type=_GETSCHEMARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateSchema',
    full_name='strmprivacy.api.schemas.v1.SchemasService.CreateSchema',
    index=2,
    containing_service=None,
    input_type=_CREATESCHEMAREQUEST,
    output_type=_CREATESCHEMARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateSchema',
    full_name='strmprivacy.api.schemas.v1.SchemasService.UpdateSchema',
    index=3,
    containing_service=None,
    input_type=_UPDATESCHEMAREQUEST,
    output_type=_UPDATESCHEMARESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetSchemaCode',
    full_name='strmprivacy.api.schemas.v1.SchemasService.GetSchemaCode',
    index=4,
    containing_service=None,
    input_type=_GETSCHEMACODEREQUEST,
    output_type=_GETSCHEMACODERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SCHEMASSERVICE)

DESCRIPTOR.services_by_name['SchemasService'] = _SCHEMASSERVICE

# @@protoc_insertion_point(module_scope)
