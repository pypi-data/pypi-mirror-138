# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/network/local_ratelimit/v3/local_rate_limit.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class LocalRateLimit(betterproto.Message):
    # The prefix to use when emitting :ref:`statistics
    # <config_network_filters_local_rate_limit_stats>`.
    stat_prefix: str = betterproto.string_field(1)
    # The token bucket configuration to use for rate limiting connections that
    # are processed by the filter's filter chain. Each incoming connection
    # processed by the filter consumes a single token. If the token is available,
    # the connection will be allowed. If no tokens are available, the connection
    # will be immediately closed. .. note::   In the current implementation each
    # filter and filter chain has an independent rate limit. .. note::   In the
    # current implementation the token bucket's :ref:`fill_interval
    # <envoy_v3_api_field_type.v3.TokenBucket.fill_interval>` must be >= 50ms to
    # avoid too aggressive   refills.
    token_bucket: "_____type_v3__.TokenBucket" = betterproto.message_field(2)
    # Runtime flag that controls whether the filter is enabled or not. If not
    # specified, defaults to enabled.
    runtime_enabled: "_____config_core_v3__.RuntimeFeatureFlag" = (
        betterproto.message_field(3)
    )


from ......config.core import v3 as _____config_core_v3__
from ......type import v3 as _____type_v3__
