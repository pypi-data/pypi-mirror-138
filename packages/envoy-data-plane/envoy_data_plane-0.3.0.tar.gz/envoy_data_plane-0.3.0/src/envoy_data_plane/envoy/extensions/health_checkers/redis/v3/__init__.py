# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/health_checkers/redis/v3/redis.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class Redis(betterproto.Message):
    # If set, optionally perform ``EXISTS <key>`` instead of ``PING``. A return
    # value from Redis of 0 (does not exist) is considered a passing healthcheck.
    # A return value other than 0 is considered a failure. This allows the user
    # to mark a Redis instance for maintenance by setting the specified key to
    # any value and waiting for traffic to drain.
    key: str = betterproto.string_field(1)
