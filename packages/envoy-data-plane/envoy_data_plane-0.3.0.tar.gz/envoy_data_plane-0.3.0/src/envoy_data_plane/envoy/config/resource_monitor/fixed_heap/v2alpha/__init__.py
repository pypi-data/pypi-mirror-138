# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/resource_monitor/fixed_heap/v2alpha/fixed_heap.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class FixedHeapConfig(betterproto.Message):
    """
    The fixed heap resource monitor reports the Envoy process memory pressure,
    computed as a fraction of currently reserved heap memory divided by a
    statically configured maximum specified in the FixedHeapConfig.
    """

    max_heap_size_bytes: int = betterproto.uint64_field(1)
