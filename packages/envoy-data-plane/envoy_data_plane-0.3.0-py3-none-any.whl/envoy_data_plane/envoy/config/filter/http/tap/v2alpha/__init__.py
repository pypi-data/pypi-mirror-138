# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/filter/http/tap/v2alpha/tap.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class Tap(betterproto.Message):
    """Top level configuration for the tap filter."""

    # Common configuration for the HTTP tap filter.
    common_config: "____common_tap_v2_alpha__.CommonExtensionConfig" = (
        betterproto.message_field(1)
    )


from .....common.tap import v2alpha as ____common_tap_v2_alpha__
