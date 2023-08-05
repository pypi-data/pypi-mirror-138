# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/http/header_formatters/preserve_case/v3/preserve_case.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class PreserveCaseFormatterConfig(betterproto.Message):
    """
    Configuration for the preserve case header formatter. See the :ref:`header
    casing <config_http_conn_man_header_casing>` configuration guide for more
    information.
    """

    # Allows forwarding reason phrase text. This is off by default, and a
    # standard reason phrase is used for a corresponding HTTP response code.
    forward_reason_phrase: bool = betterproto.bool_field(1)
