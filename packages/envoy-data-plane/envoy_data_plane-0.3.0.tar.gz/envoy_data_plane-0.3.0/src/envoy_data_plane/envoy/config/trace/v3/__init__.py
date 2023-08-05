# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/trace/v3/datadog.proto, envoy/config/trace/v3/dynamic_ot.proto, envoy/config/trace/v3/http_tracer.proto, envoy/config/trace/v3/lightstep.proto, envoy/config/trace/v3/opencensus.proto, envoy/config/trace/v3/service.proto, envoy/config/trace/v3/skywalking.proto, envoy/config/trace/v3/trace.proto, envoy/config/trace/v3/xray.proto, envoy/config/trace/v3/zipkin.proto
# plugin: python-betterproto
import warnings
from dataclasses import dataclass
from typing import List, Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class LightstepConfigPropagationMode(betterproto.Enum):
    ENVOY = 0
    LIGHTSTEP = 1
    B3 = 2
    TRACE_CONTEXT = 3


class OpenCensusConfigTraceContext(betterproto.Enum):
    NONE = 0
    TRACE_CONTEXT = 1
    GRPC_TRACE_BIN = 2
    CLOUD_TRACE_CONTEXT = 3
    B3 = 4


class ZipkinConfigCollectorEndpointVersion(betterproto.Enum):
    DEPRECATED_AND_UNAVAILABLE_DO_NOT_USE = 0
    HTTP_JSON = 1
    HTTP_PROTO = 2
    GRPC = 3


@dataclass(eq=False, repr=False)
class Tracing(betterproto.Message):
    """
    The tracing configuration specifies settings for an HTTP tracer provider
    used by Envoy. Envoy may support other tracers in the future, but right now
    the HTTP tracer is the only one supported. .. attention::   Use of this
    message type has been deprecated in favor of direct use of
    :ref:`Tracing.Http <envoy_v3_api_msg_config.trace.v3.Tracing.Http>`.
    """

    # Provides configuration for the HTTP tracer.
    http: "TracingHttp" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class TracingHttp(betterproto.Message):
    """
    Configuration for an HTTP tracer provider used by Envoy. The configuration
    is defined by the :ref:`HttpConnectionManager.Tracing <envoy_v3_api_msg_ext
    ensions.filters.network.http_connection_manager.v3.HttpConnectionManager.Tr
    acing>` :ref:`provider <envoy_v3_api_field_extensions.filters.network.http_
    connection_manager.v3.HttpConnectionManager.Tracing.provider>` field.
    """

    # The name of the HTTP trace driver to instantiate. The name must match a
    # supported HTTP trace driver. See the :ref:`extensions listed in
    # typed_config below <extension_category_envoy.tracers>` for the default list
    # of the HTTP trace driver.
    name: str = betterproto.string_field(1)
    typed_config: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(
        3, group="config_type"
    )


@dataclass(eq=False, repr=False)
class DynamicOtConfig(betterproto.Message):
    """
    DynamicOtConfig is used to dynamically load a tracer from a shared library
    that implements the `OpenTracing dynamic loading API
    <https://github.com/opentracing/opentracing-cpp>`_. [#extension:
    envoy.tracers.dynamic_ot]
    """

    # Dynamic library implementing the `OpenTracing API
    # <https://github.com/opentracing/opentracing-cpp>`_.
    library: str = betterproto.string_field(1)
    # The configuration to use when creating a tracer from the given dynamic
    # library.
    config: "betterproto_lib_google_protobuf.Struct" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class TraceServiceConfig(betterproto.Message):
    """Configuration structure."""

    # The upstream gRPC cluster that hosts the metrics service.
    grpc_service: "__core_v3__.GrpcService" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class XRayConfig(betterproto.Message):
    """[#extension: envoy.tracers.xray]"""

    # The UDP endpoint of the X-Ray Daemon where the spans will be sent. If this
    # value is not set, the default value of 127.0.0.1:2000 will be used.
    daemon_endpoint: "__core_v3__.SocketAddress" = betterproto.message_field(1)
    # The name of the X-Ray segment.
    segment_name: str = betterproto.string_field(2)
    # The location of a local custom sampling rules JSON file. For an example of
    # the sampling rules see: `X-Ray SDK documentation
    # <https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-go-
    # configuration.html#xray-sdk-go-configuration-sampling>`_
    sampling_rule_manifest: "__core_v3__.DataSource" = betterproto.message_field(3)
    # Optional custom fields to be added to each trace segment. see: `X-Ray
    # Segment Document documentation
    # <https://docs.aws.amazon.com/xray/latest/devguide/xray-api-
    # segmentdocuments.html>`__
    segment_fields: "XRayConfigSegmentFields" = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class XRayConfigSegmentFields(betterproto.Message):
    # The type of AWS resource, e.g. "AWS::AppMesh::Proxy".
    origin: str = betterproto.string_field(1)
    # AWS resource metadata dictionary. See: `X-Ray Segment Document
    # documentation <https://docs.aws.amazon.com/xray/latest/devguide/xray-api-
    # segmentdocuments.html#api-segmentdocuments-aws>`__
    aws: "betterproto_lib_google_protobuf.Struct" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class LightstepConfig(betterproto.Message):
    """
    Configuration for the LightStep tracer. [#extension:
    envoy.tracers.lightstep]
    """

    # The cluster manager cluster that hosts the LightStep collectors.
    collector_cluster: str = betterproto.string_field(1)
    # File containing the access token to the `LightStep
    # <https://lightstep.com/>`_ API.
    access_token_file: str = betterproto.string_field(2)
    # Access token to the `LightStep <https://lightstep.com/>`_ API.
    access_token: "__core_v3__.DataSource" = betterproto.message_field(4)
    # Propagation modes to use by LightStep's tracer.
    propagation_modes: List["LightstepConfigPropagationMode"] = betterproto.enum_field(
        3
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.access_token_file:
            warnings.warn(
                "LightstepConfig.access_token_file is deprecated", DeprecationWarning
            )


@dataclass(eq=False, repr=False)
class OpenCensusConfig(betterproto.Message):
    """
    Configuration for the OpenCensus tracer. [#next-free-field: 15]
    [#extension: envoy.tracers.opencensus]
    """

    # Configures tracing, e.g. the sampler, max number of annotations, etc.
    trace_config: "____opencensus_proto_trace_v1__.TraceConfig" = (
        betterproto.message_field(1)
    )
    # Enables the stdout exporter if set to true. This is intended for debugging
    # purposes.
    stdout_exporter_enabled: bool = betterproto.bool_field(2)
    # Enables the Stackdriver exporter if set to true. The project_id must also
    # be set.
    stackdriver_exporter_enabled: bool = betterproto.bool_field(3)
    # The Cloud project_id to use for Stackdriver tracing.
    stackdriver_project_id: str = betterproto.string_field(4)
    # (optional) By default, the Stackdriver exporter will connect to production
    # Stackdriver. If stackdriver_address is non-empty, it will instead connect
    # to this address, which is in the gRPC format:
    # https://github.com/grpc/grpc/blob/master/doc/naming.md
    stackdriver_address: str = betterproto.string_field(10)
    # (optional) The gRPC server that hosts Stackdriver tracing service. Only
    # Google gRPC is supported. If :ref:`target_uri
    # <envoy_v3_api_field_config.core.v3.GrpcService.GoogleGrpc.target_uri>` is
    # not provided, the default production Stackdriver address will be used.
    stackdriver_grpc_service: "__core_v3__.GrpcService" = betterproto.message_field(13)
    # Enables the Zipkin exporter if set to true. The url and service name must
    # also be set. This is deprecated, prefer to use Envoy's :ref:`native Zipkin
    # tracer <envoy_v3_api_msg_config.trace.v3.ZipkinConfig>`.
    zipkin_exporter_enabled: bool = betterproto.bool_field(5)
    # The URL to Zipkin, e.g. "http://127.0.0.1:9411/api/v2/spans". This is
    # deprecated, prefer to use Envoy's :ref:`native Zipkin tracer
    # <envoy_v3_api_msg_config.trace.v3.ZipkinConfig>`.
    zipkin_url: str = betterproto.string_field(6)
    # Enables the OpenCensus Agent exporter if set to true. The ocagent_address
    # or ocagent_grpc_service must also be set.
    ocagent_exporter_enabled: bool = betterproto.bool_field(11)
    # The address of the OpenCensus Agent, if its exporter is enabled, in gRPC
    # format: https://github.com/grpc/grpc/blob/master/doc/naming.md
    # [#comment:TODO: deprecate this field]
    ocagent_address: str = betterproto.string_field(12)
    # (optional) The gRPC server hosted by the OpenCensus Agent. Only Google gRPC
    # is supported. This is only used if the ocagent_address is left empty.
    ocagent_grpc_service: "__core_v3__.GrpcService" = betterproto.message_field(14)
    # List of incoming trace context headers we will accept. First one found
    # wins.
    incoming_trace_context: List[
        "OpenCensusConfigTraceContext"
    ] = betterproto.enum_field(8)
    # List of outgoing trace context headers we will produce.
    outgoing_trace_context: List[
        "OpenCensusConfigTraceContext"
    ] = betterproto.enum_field(9)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.zipkin_exporter_enabled:
            warnings.warn(
                "OpenCensusConfig.zipkin_exporter_enabled is deprecated",
                DeprecationWarning,
            )
        if self.zipkin_url:
            warnings.warn(
                "OpenCensusConfig.zipkin_url is deprecated", DeprecationWarning
            )


@dataclass(eq=False, repr=False)
class SkyWalkingConfig(betterproto.Message):
    """
    Configuration for the SkyWalking tracer. Please note that if SkyWalking
    tracer is used as the provider of http tracer, then :ref:`start_child_span
    <envoy_v3_api_field_extensions.filters.http.router.v3.Router.start_child_sp
    an>` in the router must be set to true to get the correct topology and
    tracing data. Moreover, SkyWalking Tracer does not support SkyWalking
    extension header (``sw8-x``) temporarily. [#extension:
    envoy.tracers.skywalking]
    """

    # SkyWalking collector service.
    grpc_service: "__core_v3__.GrpcService" = betterproto.message_field(1)
    client_config: "ClientConfig" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class ClientConfig(betterproto.Message):
    """Client config for SkyWalking tracer."""

    # Service name for SkyWalking tracer. If this field is empty, then local
    # service cluster name that configured by :ref:`Bootstrap node
    # <envoy_v3_api_field_config.bootstrap.v3.Bootstrap.node>` message's
    # :ref:`cluster <envoy_v3_api_field_config.core.v3.Node.cluster>` field or
    # command line option :option:`--service-cluster` will be used. If both this
    # field and local service cluster name are empty, ``EnvoyProxy`` is used as
    # the service name by default.
    service_name: str = betterproto.string_field(1)
    # Service instance name for SkyWalking tracer. If this field is empty, then
    # local service node that configured by :ref:`Bootstrap node
    # <envoy_v3_api_field_config.bootstrap.v3.Bootstrap.node>` message's :ref:`id
    # <envoy_v3_api_field_config.core.v3.Node.id>` field or command line  option
    # :option:`--service-node` will be used. If both this field and local service
    # node are empty, ``EnvoyProxy`` is used as the instance name by default.
    instance_name: str = betterproto.string_field(2)
    # Inline authentication token string.
    backend_token: str = betterproto.string_field(3, group="backend_token_specifier")
    # Envoy caches the segment in memory when the SkyWalking backend service is
    # temporarily unavailable. This field specifies the maximum number of
    # segments that can be cached. If not specified, the default is 1024.
    max_cache_size: Optional[int] = betterproto.message_field(
        4, wraps=betterproto.TYPE_UINT32
    )


@dataclass(eq=False, repr=False)
class ZipkinConfig(betterproto.Message):
    """
    Configuration for the Zipkin tracer. [#extension: envoy.tracers.zipkin]
    [#next-free-field: 7]
    """

    # The cluster manager cluster that hosts the Zipkin collectors.
    collector_cluster: str = betterproto.string_field(1)
    # The API endpoint of the Zipkin service where the spans will be sent. When
    # using a standard Zipkin installation.
    collector_endpoint: str = betterproto.string_field(2)
    # Determines whether a 128bit trace id will be used when creating a new trace
    # instance. The default value is false, which will result in a 64 bit trace
    # id being used.
    trace_id_128_bit: bool = betterproto.bool_field(3)
    # Determines whether client and server spans will share the same span
    # context. The default value is true.
    shared_span_context: Optional[bool] = betterproto.message_field(
        4, wraps=betterproto.TYPE_BOOL
    )
    # Determines the selected collector endpoint version.
    collector_endpoint_version: "ZipkinConfigCollectorEndpointVersion" = (
        betterproto.enum_field(5)
    )
    # Optional hostname to use when sending spans to the collector_cluster.
    # Useful for collectors that require a specific hostname. Defaults to
    # :ref:`collector_cluster
    # <envoy_v3_api_field_config.trace.v3.ZipkinConfig.collector_cluster>` above.
    collector_hostname: str = betterproto.string_field(6)


@dataclass(eq=False, repr=False)
class DatadogConfig(betterproto.Message):
    """
    Configuration for the Datadog tracer. [#extension: envoy.tracers.datadog]
    """

    # The cluster to use for submitting traces to the Datadog agent.
    collector_cluster: str = betterproto.string_field(1)
    # The name used for the service when traces are generated by envoy.
    service_name: str = betterproto.string_field(2)


from .....opencensus.proto.trace import v1 as ____opencensus_proto_trace_v1__
from ...core import v3 as __core_v3__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
