# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_monitoring_details.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$transaction_monitoring_details.proto\x12\x1etransaction_monitoring_details\"\xe4\x01\n\x0bRequestData\x12\x41\n\x0cproduct_type\x18\x01 \x01(\x0e\x32+.transaction_monitoring_details.ProductType\x12Z\n\x10request_metadata\x18\x02 \x03(\x0b\x32@.transaction_monitoring_details.RequestData.RequestMetadataEntry\x1a\x36\n\x14RequestMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xc5\x01\n\x0cResponseData\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x03\x12\x0f\n\x07message\x18\x02 \x01(\t\x12]\n\x11response_metadata\x18\x03 \x03(\x0b\x32\x42.transaction_monitoring_details.ResponseData.ResponseMetadataEntry\x1a\x37\n\x15ResponseMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01*\x1c\n\x0bProductType\x12\r\n\tUSD_CARDS\x10\x00\x32\x93\x01\n\x1cTransactionMonitoringService\x12s\n\x14\x43heckTransactionRisk\x12+.transaction_monitoring_details.RequestData\x1a,.transaction_monitoring_details.ResponseData\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_monitoring_details_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REQUESTDATA_REQUESTMETADATAENTRY']._options = None
  _globals['_REQUESTDATA_REQUESTMETADATAENTRY']._serialized_options = b'8\001'
  _globals['_RESPONSEDATA_RESPONSEMETADATAENTRY']._options = None
  _globals['_RESPONSEDATA_RESPONSEMETADATAENTRY']._serialized_options = b'8\001'
  _globals['_PRODUCTTYPE']._serialized_start=503
  _globals['_PRODUCTTYPE']._serialized_end=531
  _globals['_REQUESTDATA']._serialized_start=73
  _globals['_REQUESTDATA']._serialized_end=301
  _globals['_REQUESTDATA_REQUESTMETADATAENTRY']._serialized_start=247
  _globals['_REQUESTDATA_REQUESTMETADATAENTRY']._serialized_end=301
  _globals['_RESPONSEDATA']._serialized_start=304
  _globals['_RESPONSEDATA']._serialized_end=501
  _globals['_RESPONSEDATA_RESPONSEMETADATAENTRY']._serialized_start=446
  _globals['_RESPONSEDATA_RESPONSEMETADATAENTRY']._serialized_end=501
  _globals['_TRANSACTIONMONITORINGSERVICE']._serialized_start=534
  _globals['_TRANSACTIONMONITORINGSERVICE']._serialized_end=681
# @@protoc_insertion_point(module_scope)