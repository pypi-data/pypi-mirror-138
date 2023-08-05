# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/listener/tls_inspector/v3/tls_inspector.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class TlsInspector(betterproto.Message):
    # Populate `JA3` fingerprint hash using data from the TLS Client Hello
    # packet. Default is false.
    enable_ja3_fingerprinting: Optional[bool] = betterproto.message_field(
        1, wraps=betterproto.TYPE_BOOL
    )
