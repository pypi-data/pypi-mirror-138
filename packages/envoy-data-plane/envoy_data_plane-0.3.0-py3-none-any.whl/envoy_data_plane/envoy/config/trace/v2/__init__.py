# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/trace/v2/datadog.proto, envoy/config/trace/v2/dynamic_ot.proto, envoy/config/trace/v2/http_tracer.proto, envoy/config/trace/v2/lightstep.proto, envoy/config/trace/v2/opencensus.proto, envoy/config/trace/v2/service.proto, envoy/config/trace/v2/trace.proto, envoy/config/trace/v2/zipkin.proto
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
    HTTP_JSON_V1 = 0
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
    :ref:`Tracing.Http <envoy_api_msg_config.trace.v2.Tracing.Http>`.
    """

    # Provides configuration for the HTTP tracer.
    http: "TracingHttp" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class TracingHttp(betterproto.Message):
    """
    Configuration for an HTTP tracer provider used by Envoy. The configuration
    is defined by the :ref:`HttpConnectionManager.Tracing <envoy_api_msg_config
    .filter.network.http_connection_manager.v2.HttpConnectionManager.Tracing>`
    :ref:`provider <envoy_api_field_config.filter.network.http_connection_manag
    er.v2.HttpConnectionManager.Tracing.provider>` field.
    """

    # The name of the HTTP trace driver to instantiate. The name must match a
    # supported HTTP trace driver. Built-in trace drivers: -
    # *envoy.tracers.lightstep* - *envoy.tracers.zipkin* -
    # *envoy.tracers.dynamic_ot* - *envoy.tracers.datadog* -
    # *envoy.tracers.opencensus* - *envoy.tracers.xray*
    name: str = betterproto.string_field(1)
    config: "betterproto_lib_google_protobuf.Struct" = betterproto.message_field(
        2, group="config_type"
    )
    typed_config: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(
        3, group="config_type"
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.config:
            warnings.warn("TracingHttp.config is deprecated", DeprecationWarning)


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
    grpc_service: "___api_v2_core__.GrpcService" = betterproto.message_field(1)


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
    # Propagation modes to use by LightStep's tracer.
    propagation_modes: List["LightstepConfigPropagationMode"] = betterproto.enum_field(
        3
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
    stackdriver_grpc_service: "___api_v2_core__.GrpcService" = (
        betterproto.message_field(13)
    )
    # Enables the Zipkin exporter if set to true. The url and service name must
    # also be set.
    zipkin_exporter_enabled: bool = betterproto.bool_field(5)
    # The URL to Zipkin, e.g. "http://127.0.0.1:9411/api/v2/spans"
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
    ocagent_grpc_service: "___api_v2_core__.GrpcService" = betterproto.message_field(14)
    # List of incoming trace context headers we will accept. First one found
    # wins.
    incoming_trace_context: List[
        "OpenCensusConfigTraceContext"
    ] = betterproto.enum_field(8)
    # List of outgoing trace context headers we will produce.
    outgoing_trace_context: List[
        "OpenCensusConfigTraceContext"
    ] = betterproto.enum_field(9)


@dataclass(eq=False, repr=False)
class ZipkinConfig(betterproto.Message):
    """
    Configuration for the Zipkin tracer. [#extension: envoy.tracers.zipkin]
    [#next-free-field: 6]
    """

    # The cluster manager cluster that hosts the Zipkin collectors. Note that the
    # Zipkin cluster must be defined in the :ref:`Bootstrap static cluster
    # resources
    # <envoy_api_field_config.bootstrap.v2.Bootstrap.StaticResources.clusters>`.
    collector_cluster: str = betterproto.string_field(1)
    # The API endpoint of the Zipkin service where the spans will be sent. When
    # using a standard Zipkin installation, the API endpoint is typically
    # /api/v1/spans, which is the default value.
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
    # Determines the selected collector endpoint version. By default, the
    # ``HTTP_JSON_V1`` will be used.
    collector_endpoint_version: "ZipkinConfigCollectorEndpointVersion" = (
        betterproto.enum_field(5)
    )


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
from ....api.v2 import core as ___api_v2_core__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
