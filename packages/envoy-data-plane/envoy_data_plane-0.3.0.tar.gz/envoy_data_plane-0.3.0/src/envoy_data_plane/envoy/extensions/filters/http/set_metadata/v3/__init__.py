# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/http/set_metadata/v3/set_metadata.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class Config(betterproto.Message):
    # The metadata namespace.
    metadata_namespace: str = betterproto.string_field(1)
    # The value to update the namespace with. See :ref:`the filter documentation
    # <config_http_filters_set_metadata>` for more information on how this value
    # is merged with potentially existing ones.
    value: "betterproto_lib_google_protobuf.Struct" = betterproto.message_field(2)


import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
