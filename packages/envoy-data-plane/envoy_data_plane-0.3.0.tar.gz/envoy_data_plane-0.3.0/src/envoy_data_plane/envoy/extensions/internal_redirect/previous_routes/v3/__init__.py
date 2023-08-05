# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/internal_redirect/previous_routes/v3/previous_routes_config.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class PreviousRoutesConfig(betterproto.Message):
    """
    An internal redirect predicate that rejects redirect targets that are
    pointing to a route that has been followed by a previous redirect from the
    current route. [#extension:
    envoy.internal_redirect_predicates.previous_routes]
    """

    pass
