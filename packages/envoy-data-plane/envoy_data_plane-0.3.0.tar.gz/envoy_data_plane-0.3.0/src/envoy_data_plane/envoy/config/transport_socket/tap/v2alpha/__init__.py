# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/transport_socket/tap/v2alpha/tap.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class Tap(betterproto.Message):
    """
    Configuration for tap transport socket. This wraps another transport
    socket, providing the ability to interpose and record in plain text any
    traffic that is surfaced to Envoy.
    """

    # Common configuration for the tap transport socket.
    common_config: "___common_tap_v2_alpha__.CommonExtensionConfig" = (
        betterproto.message_field(1)
    )
    # The underlying transport socket being wrapped.
    transport_socket: "____api_v2_core__.TransportSocket" = betterproto.message_field(2)


from .....api.v2 import core as ____api_v2_core__
from ....common.tap import v2alpha as ___common_tap_v2_alpha__
