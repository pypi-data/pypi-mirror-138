# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/network/meta_protocol_proxy/v3/meta_protocol_proxy.proto, envoy/extensions/filters/network/meta_protocol_proxy/v3/route.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class RouteConfiguration(betterproto.Message):
    """
    [#protodoc-title: Meta Protocol Proxy Route Configuration] The meta
    protocol proxy makes use of the `xds matching API` for routing
    configurations. In the below example, we combine a top level tree matcher
    with a linear matcher to match the incoming requests, and send the matching
    requests to v1 of the upstream service. name: demo-v1 route:
    matcher_tree:     input:       name: request-service       typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.network.meta_protocol
    _proxy.matcher.v3.ServiceMatchInput     exact_match_map:       map:
    org.apache.dubbo.samples.basic.api.DemoService:           matcher:
    matcher_list:               matchers:               - predicate:
    and_matcher:                     predicate:                     -
    single_predicate:                         input:
    name: request-properties                           typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.network.meta_protocol
    _proxy.matcher.v3.PropertyMatchInput
    property_name: version                         value_match:
    exact: v1                     - single_predicate:
    input:                           name: request-properties
    typed_config:                             "@type": type.googleapis.com/envo
    y.extensions.filters.network.meta_protocol_proxy.matcher.v3.PropertyMatchIn
    put                             property_name: user
    value_match:                           exact: john
    on_match:                   action:                     name: route
    typed_config:                       "@type": type.googleapis.com/envoy.exte
    nsions.filters.network.meta_protocol_proxy.matcher.action.v3.routeAction
    cluster: outbound|20880|v1|org.apache.dubbo.samples.basic.api.demoservice
    [#not-implemented-hide:]
    """

    # The name of the route configuration. For example, it might match
    # route_config_name in
    # envoy.extensions.filters.network.meta_protocol_proxy.v3.Rds.
    name: str = betterproto.string_field(1)
    # The match tree to use when resolving route actions for incoming requests.
    route: "______xds_type_matcher_v3__.Matcher" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class MetaProtocolProxy(betterproto.Message):
    """[#not-implemented-hide:] [#next-free-field: 6]"""

    # The human readable prefix to use when emitting statistics.
    stat_prefix: str = betterproto.string_field(1)
    # The application protocol built on top of the meta protocol proxy.
    application_protocol: "ApplicationProtocol" = betterproto.message_field(2)
    # The meta protocol proxies route table will be dynamically loaded via the
    # meta RDS API.
    rds: "MetaRds" = betterproto.message_field(3, group="route_specifier")
    # The route table for the meta protocol proxy is static and is specified in
    # this property.
    route_config: "RouteConfiguration" = betterproto.message_field(
        4, group="route_specifier"
    )
    # A list of individual Layer-7 filters that make up the filter chain for
    # requests made to the meta protocol proxy. Order matters as the filters are
    # processed sequentially as request events happen.
    meta_protocol_filters: List[
        "_____config_core_v3__.TypedExtensionConfig"
    ] = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class ApplicationProtocol(betterproto.Message):
    """[#not-implemented-hide:]"""

    # The name of the application protocol.
    name: str = betterproto.string_field(1)
    # The codec which encodes and decodes the application protocol.
    codec: "_____config_core_v3__.TypedExtensionConfig" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class MetaRds(betterproto.Message):
    """[#not-implemented-hide:]"""

    # Configuration source specifier for RDS.
    config_source: "_____config_core_v3__.ConfigSource" = betterproto.message_field(1)
    # The name of the route configuration. This name will be passed to the RDS
    # API. This allows an Envoy configuration with multiple meta protocol proxies
    # to use different route configurations.
    route_config_name: str = betterproto.string_field(2)


from .......xds.type.matcher import v3 as ______xds_type_matcher_v3__
from ......config.core import v3 as _____config_core_v3__
