# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/annotations/deprecation.proto, envoy/annotations/resource.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class ResourceAnnotation(betterproto.Message):
    # Annotation for xDS services that indicates the fully-qualified Protobuf
    # type for the resource type.
    type: str = betterproto.string_field(1)
