# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/filter/fault/v2/fault.proto
# plugin: python-betterproto
import warnings
from dataclasses import dataclass
from datetime import timedelta

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class FaultDelayFaultDelayType(betterproto.Enum):
    FIXED = 0


@dataclass(eq=False, repr=False)
class FaultDelay(betterproto.Message):
    """
    Delay specification is used to inject latency into the
    HTTP/gRPC/Mongo/Redis operation or delay proxying of TCP connections.
    [#next-free-field: 6]
    """

    # Unused and deprecated. Will be removed in the next release.
    type: "FaultDelayFaultDelayType" = betterproto.enum_field(1)
    # Add a fixed delay before forwarding the operation upstream. See
    # https://developers.google.com/protocol-buffers/docs/proto3#json for the
    # JSON/YAML Duration mapping. For HTTP/Mongo/Redis, the specified delay will
    # be injected before a new request/operation. For TCP connections, the
    # proxying of the connection upstream will be delayed for the specified
    # period. This is required if type is FIXED.
    fixed_delay: timedelta = betterproto.message_field(3, group="fault_delay_secifier")
    # Fault delays are controlled via an HTTP header (if applicable).
    header_delay: "FaultDelayHeaderDelay" = betterproto.message_field(
        5, group="fault_delay_secifier"
    )
    # The percentage of operations/connections/requests on which the delay will
    # be injected.
    percentage: "____type__.FractionalPercent" = betterproto.message_field(4)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.type:
            warnings.warn("FaultDelay.type is deprecated", DeprecationWarning)


@dataclass(eq=False, repr=False)
class FaultDelayHeaderDelay(betterproto.Message):
    """
    Fault delays are controlled via an HTTP header (if applicable). See the
    :ref:`HTTP fault filter <config_http_filters_fault_injection_http_header>`
    documentation for more information.
    """

    pass


@dataclass(eq=False, repr=False)
class FaultRateLimit(betterproto.Message):
    """Describes a rate limit to be applied."""

    # A fixed rate limit.
    fixed_limit: "FaultRateLimitFixedLimit" = betterproto.message_field(
        1, group="limit_type"
    )
    # Rate limits are controlled via an HTTP header (if applicable).
    header_limit: "FaultRateLimitHeaderLimit" = betterproto.message_field(
        3, group="limit_type"
    )
    # The percentage of operations/connections/requests on which the rate limit
    # will be injected.
    percentage: "____type__.FractionalPercent" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class FaultRateLimitFixedLimit(betterproto.Message):
    """Describes a fixed/constant rate limit."""

    # The limit supplied in KiB/s.
    limit_kbps: int = betterproto.uint64_field(1)


@dataclass(eq=False, repr=False)
class FaultRateLimitHeaderLimit(betterproto.Message):
    """
    Rate limits are controlled via an HTTP header (if applicable). See the
    :ref:`HTTP fault filter <config_http_filters_fault_injection_http_header>`
    documentation for more information.
    """

    pass


from ..... import type as ____type__
