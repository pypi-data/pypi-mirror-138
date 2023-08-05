# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/http/alternate_protocols_cache/v3/alternate_protocols_cache.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class FilterConfig(betterproto.Message):
    """
    Configuration for the alternate protocols cache HTTP filter. [#extension:
    envoy.filters.http.alternate_protocols_cache]
    """

    # If set, causes the use of the alternate protocols cache, which is
    # responsible for parsing and caching HTTP Alt-Svc headers. This enables the
    # use of HTTP/3 for upstream servers that advertise supporting it.
    # TODO(RyanTheOptimist): Make this field required when HTTP/3 is enabled via
    # auto_http.
    alternate_protocols_cache_options: "_____config_core_v3__.AlternateProtocolsCacheOptions" = betterproto.message_field(
        1
    )


from ......config.core import v3 as _____config_core_v3__
