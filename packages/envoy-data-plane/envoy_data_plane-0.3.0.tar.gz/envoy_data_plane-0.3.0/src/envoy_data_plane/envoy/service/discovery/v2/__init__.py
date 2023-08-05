# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/service/discovery/v2/ads.proto, envoy/service/discovery/v2/hds.proto, envoy/service/discovery/v2/rtds.proto, envoy/service/discovery/v2/sds.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import timedelta
from typing import AsyncIterable, AsyncIterator, Dict, Iterable, List, Optional, Union

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase
import grpclib


class CapabilityProtocol(betterproto.Enum):
    HTTP = 0
    TCP = 1
    REDIS = 2


@dataclass(eq=False, repr=False)
class RtdsDummy(betterproto.Message):
    """
    [#not-implemented-hide:] Not configuration. Workaround c++ protobuf issue
    with importing services: https://github.com/google/protobuf/issues/4221
    """

    pass


@dataclass(eq=False, repr=False)
class Runtime(betterproto.Message):
    """
    RTDS resource type. This describes a layer in the runtime virtual
    filesystem.
    """

    # Runtime resource name. This makes the Runtime a self-describing xDS
    # resource.
    name: str = betterproto.string_field(1)
    layer: "betterproto_lib_google_protobuf.Struct" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class SdsDummy(betterproto.Message):
    """
    [#not-implemented-hide:] Not configuration. Workaround c++ protobuf issue
    with importing services: https://github.com/google/protobuf/issues/4221
    """

    pass


@dataclass(eq=False, repr=False)
class Capability(betterproto.Message):
    """
    Defines supported protocols etc, so the management server can assign proper
    endpoints to healthcheck.
    """

    health_check_protocols: List["CapabilityProtocol"] = betterproto.enum_field(1)


@dataclass(eq=False, repr=False)
class HealthCheckRequest(betterproto.Message):
    node: "___api_v2_core__.Node" = betterproto.message_field(1)
    capability: "Capability" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class EndpointHealth(betterproto.Message):
    endpoint: "___api_v2_endpoint__.Endpoint" = betterproto.message_field(1)
    health_status: "___api_v2_core__.HealthStatus" = betterproto.enum_field(2)


@dataclass(eq=False, repr=False)
class EndpointHealthResponse(betterproto.Message):
    endpoints_health: List["EndpointHealth"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class HealthCheckRequestOrEndpointHealthResponse(betterproto.Message):
    health_check_request: "HealthCheckRequest" = betterproto.message_field(
        1, group="request_type"
    )
    endpoint_health_response: "EndpointHealthResponse" = betterproto.message_field(
        2, group="request_type"
    )


@dataclass(eq=False, repr=False)
class LocalityEndpoints(betterproto.Message):
    locality: "___api_v2_core__.Locality" = betterproto.message_field(1)
    endpoints: List["___api_v2_endpoint__.Endpoint"] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class ClusterHealthCheck(betterproto.Message):
    """
    The cluster name and locality is provided to Envoy for the endpoints that
    it health checks to support statistics reporting, logging and debugging by
    the Envoy instance (outside of HDS). For maximum usefulness, it should
    match the same cluster structure as that provided by EDS.
    """

    cluster_name: str = betterproto.string_field(1)
    health_checks: List["___api_v2_core__.HealthCheck"] = betterproto.message_field(2)
    locality_endpoints: List["LocalityEndpoints"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class HealthCheckSpecifier(betterproto.Message):
    cluster_health_checks: List["ClusterHealthCheck"] = betterproto.message_field(1)
    # The default is 1 second.
    interval: timedelta = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class AdsDummy(betterproto.Message):
    """
    [#not-implemented-hide:] Not configuration. Workaround c++ protobuf issue
    with importing services: https://github.com/google/protobuf/issues/4221
    """

    pass


class RuntimeDiscoveryServiceStub(betterproto.ServiceStub):
    async def stream_runtime(
        self,
        request_iterator: Union[
            AsyncIterable["___api_v2__.DiscoveryRequest"],
            Iterable["___api_v2__.DiscoveryRequest"],
        ],
    ) -> AsyncIterator["___api_v2__.DiscoveryResponse"]:

        async for response in self._stream_stream(
            "/envoy.service.discovery.v2.RuntimeDiscoveryService/StreamRuntime",
            request_iterator,
            ___api_v2__.DiscoveryRequest,
            ___api_v2__.DiscoveryResponse,
        ):
            yield response

    async def delta_runtime(
        self,
        request_iterator: Union[
            AsyncIterable["___api_v2__.DeltaDiscoveryRequest"],
            Iterable["___api_v2__.DeltaDiscoveryRequest"],
        ],
    ) -> AsyncIterator["___api_v2__.DeltaDiscoveryResponse"]:

        async for response in self._stream_stream(
            "/envoy.service.discovery.v2.RuntimeDiscoveryService/DeltaRuntime",
            request_iterator,
            ___api_v2__.DeltaDiscoveryRequest,
            ___api_v2__.DeltaDiscoveryResponse,
        ):
            yield response

    async def fetch_runtime(
        self,
        *,
        version_info: str = "",
        node: "core.Node" = None,
        resource_names: Optional[List[str]] = None,
        type_url: str = "",
        response_nonce: str = "",
        error_detail: "___google_rpc__.Status" = None
    ) -> "___api_v2__.DiscoveryResponse":
        resource_names = resource_names or []

        request = ___api_v2__.DiscoveryRequest()
        request.version_info = version_info
        if node is not None:
            request.node = node
        request.resource_names = resource_names
        request.type_url = type_url
        request.response_nonce = response_nonce
        if error_detail is not None:
            request.error_detail = error_detail

        return await self._unary_unary(
            "/envoy.service.discovery.v2.RuntimeDiscoveryService/FetchRuntime",
            request,
            ___api_v2__.DiscoveryResponse,
        )


class SecretDiscoveryServiceStub(betterproto.ServiceStub):
    async def delta_secrets(
        self,
        request_iterator: Union[
            AsyncIterable["___api_v2__.DeltaDiscoveryRequest"],
            Iterable["___api_v2__.DeltaDiscoveryRequest"],
        ],
    ) -> AsyncIterator["___api_v2__.DeltaDiscoveryResponse"]:

        async for response in self._stream_stream(
            "/envoy.service.discovery.v2.SecretDiscoveryService/DeltaSecrets",
            request_iterator,
            ___api_v2__.DeltaDiscoveryRequest,
            ___api_v2__.DeltaDiscoveryResponse,
        ):
            yield response

    async def stream_secrets(
        self,
        request_iterator: Union[
            AsyncIterable["___api_v2__.DiscoveryRequest"],
            Iterable["___api_v2__.DiscoveryRequest"],
        ],
    ) -> AsyncIterator["___api_v2__.DiscoveryResponse"]:

        async for response in self._stream_stream(
            "/envoy.service.discovery.v2.SecretDiscoveryService/StreamSecrets",
            request_iterator,
            ___api_v2__.DiscoveryRequest,
            ___api_v2__.DiscoveryResponse,
        ):
            yield response

    async def fetch_secrets(
        self,
        *,
        version_info: str = "",
        node: "core.Node" = None,
        resource_names: Optional[List[str]] = None,
        type_url: str = "",
        response_nonce: str = "",
        error_detail: "___google_rpc__.Status" = None
    ) -> "___api_v2__.DiscoveryResponse":
        resource_names = resource_names or []

        request = ___api_v2__.DiscoveryRequest()
        request.version_info = version_info
        if node is not None:
            request.node = node
        request.resource_names = resource_names
        request.type_url = type_url
        request.response_nonce = response_nonce
        if error_detail is not None:
            request.error_detail = error_detail

        return await self._unary_unary(
            "/envoy.service.discovery.v2.SecretDiscoveryService/FetchSecrets",
            request,
            ___api_v2__.DiscoveryResponse,
        )


class HealthDiscoveryServiceStub(betterproto.ServiceStub):
    async def stream_health_check(
        self,
        request_iterator: Union[
            AsyncIterable["HealthCheckRequestOrEndpointHealthResponse"],
            Iterable["HealthCheckRequestOrEndpointHealthResponse"],
        ],
    ) -> AsyncIterator["HealthCheckSpecifier"]:

        async for response in self._stream_stream(
            "/envoy.service.discovery.v2.HealthDiscoveryService/StreamHealthCheck",
            request_iterator,
            HealthCheckRequestOrEndpointHealthResponse,
            HealthCheckSpecifier,
        ):
            yield response

    async def fetch_health_check(
        self,
        *,
        health_check_request: "HealthCheckRequest" = None,
        endpoint_health_response: "EndpointHealthResponse" = None
    ) -> "HealthCheckSpecifier":

        request = HealthCheckRequestOrEndpointHealthResponse()
        if health_check_request is not None:
            request.health_check_request = health_check_request
        if endpoint_health_response is not None:
            request.endpoint_health_response = endpoint_health_response

        return await self._unary_unary(
            "/envoy.service.discovery.v2.HealthDiscoveryService/FetchHealthCheck",
            request,
            HealthCheckSpecifier,
        )


class AggregatedDiscoveryServiceStub(betterproto.ServiceStub):
    async def stream_aggregated_resources(
        self,
        request_iterator: Union[
            AsyncIterable["___api_v2__.DiscoveryRequest"],
            Iterable["___api_v2__.DiscoveryRequest"],
        ],
    ) -> AsyncIterator["___api_v2__.DiscoveryResponse"]:

        async for response in self._stream_stream(
            "/envoy.service.discovery.v2.AggregatedDiscoveryService/StreamAggregatedResources",
            request_iterator,
            ___api_v2__.DiscoveryRequest,
            ___api_v2__.DiscoveryResponse,
        ):
            yield response

    async def delta_aggregated_resources(
        self,
        request_iterator: Union[
            AsyncIterable["___api_v2__.DeltaDiscoveryRequest"],
            Iterable["___api_v2__.DeltaDiscoveryRequest"],
        ],
    ) -> AsyncIterator["___api_v2__.DeltaDiscoveryResponse"]:

        async for response in self._stream_stream(
            "/envoy.service.discovery.v2.AggregatedDiscoveryService/DeltaAggregatedResources",
            request_iterator,
            ___api_v2__.DeltaDiscoveryRequest,
            ___api_v2__.DeltaDiscoveryResponse,
        ):
            yield response


class RuntimeDiscoveryServiceBase(ServiceBase):
    async def stream_runtime(
        self, request_iterator: AsyncIterator["___api_v2__.DiscoveryRequest"]
    ) -> AsyncIterator["___api_v2__.DiscoveryResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def delta_runtime(
        self, request_iterator: AsyncIterator["___api_v2__.DeltaDiscoveryRequest"]
    ) -> AsyncIterator["___api_v2__.DeltaDiscoveryResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def fetch_runtime(
        self,
        version_info: str,
        node: "core.Node",
        resource_names: Optional[List[str]],
        type_url: str,
        response_nonce: str,
        error_detail: "___google_rpc__.Status",
    ) -> "___api_v2__.DiscoveryResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_stream_runtime(self, stream: grpclib.server.Stream) -> None:
        request_kwargs = {"request_iterator": stream.__aiter__()}

        await self._call_rpc_handler_server_stream(
            self.stream_runtime,
            stream,
            request_kwargs,
        )

    async def __rpc_delta_runtime(self, stream: grpclib.server.Stream) -> None:
        request_kwargs = {"request_iterator": stream.__aiter__()}

        await self._call_rpc_handler_server_stream(
            self.delta_runtime,
            stream,
            request_kwargs,
        )

    async def __rpc_fetch_runtime(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "version_info": request.version_info,
            "node": request.node,
            "resource_names": request.resource_names,
            "type_url": request.type_url,
            "response_nonce": request.response_nonce,
            "error_detail": request.error_detail,
        }

        response = await self.fetch_runtime(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/envoy.service.discovery.v2.RuntimeDiscoveryService/StreamRuntime": grpclib.const.Handler(
                self.__rpc_stream_runtime,
                grpclib.const.Cardinality.STREAM_STREAM,
                ___api_v2__.DiscoveryRequest,
                ___api_v2__.DiscoveryResponse,
            ),
            "/envoy.service.discovery.v2.RuntimeDiscoveryService/DeltaRuntime": grpclib.const.Handler(
                self.__rpc_delta_runtime,
                grpclib.const.Cardinality.STREAM_STREAM,
                ___api_v2__.DeltaDiscoveryRequest,
                ___api_v2__.DeltaDiscoveryResponse,
            ),
            "/envoy.service.discovery.v2.RuntimeDiscoveryService/FetchRuntime": grpclib.const.Handler(
                self.__rpc_fetch_runtime,
                grpclib.const.Cardinality.UNARY_UNARY,
                ___api_v2__.DiscoveryRequest,
                ___api_v2__.DiscoveryResponse,
            ),
        }


class SecretDiscoveryServiceBase(ServiceBase):
    async def delta_secrets(
        self, request_iterator: AsyncIterator["___api_v2__.DeltaDiscoveryRequest"]
    ) -> AsyncIterator["___api_v2__.DeltaDiscoveryResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def stream_secrets(
        self, request_iterator: AsyncIterator["___api_v2__.DiscoveryRequest"]
    ) -> AsyncIterator["___api_v2__.DiscoveryResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def fetch_secrets(
        self,
        version_info: str,
        node: "core.Node",
        resource_names: Optional[List[str]],
        type_url: str,
        response_nonce: str,
        error_detail: "___google_rpc__.Status",
    ) -> "___api_v2__.DiscoveryResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_delta_secrets(self, stream: grpclib.server.Stream) -> None:
        request_kwargs = {"request_iterator": stream.__aiter__()}

        await self._call_rpc_handler_server_stream(
            self.delta_secrets,
            stream,
            request_kwargs,
        )

    async def __rpc_stream_secrets(self, stream: grpclib.server.Stream) -> None:
        request_kwargs = {"request_iterator": stream.__aiter__()}

        await self._call_rpc_handler_server_stream(
            self.stream_secrets,
            stream,
            request_kwargs,
        )

    async def __rpc_fetch_secrets(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "version_info": request.version_info,
            "node": request.node,
            "resource_names": request.resource_names,
            "type_url": request.type_url,
            "response_nonce": request.response_nonce,
            "error_detail": request.error_detail,
        }

        response = await self.fetch_secrets(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/envoy.service.discovery.v2.SecretDiscoveryService/DeltaSecrets": grpclib.const.Handler(
                self.__rpc_delta_secrets,
                grpclib.const.Cardinality.STREAM_STREAM,
                ___api_v2__.DeltaDiscoveryRequest,
                ___api_v2__.DeltaDiscoveryResponse,
            ),
            "/envoy.service.discovery.v2.SecretDiscoveryService/StreamSecrets": grpclib.const.Handler(
                self.__rpc_stream_secrets,
                grpclib.const.Cardinality.STREAM_STREAM,
                ___api_v2__.DiscoveryRequest,
                ___api_v2__.DiscoveryResponse,
            ),
            "/envoy.service.discovery.v2.SecretDiscoveryService/FetchSecrets": grpclib.const.Handler(
                self.__rpc_fetch_secrets,
                grpclib.const.Cardinality.UNARY_UNARY,
                ___api_v2__.DiscoveryRequest,
                ___api_v2__.DiscoveryResponse,
            ),
        }


class HealthDiscoveryServiceBase(ServiceBase):
    async def stream_health_check(
        self,
        request_iterator: AsyncIterator["HealthCheckRequestOrEndpointHealthResponse"],
    ) -> AsyncIterator["HealthCheckSpecifier"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def fetch_health_check(
        self,
        health_check_request: "HealthCheckRequest",
        endpoint_health_response: "EndpointHealthResponse",
    ) -> "HealthCheckSpecifier":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_stream_health_check(self, stream: grpclib.server.Stream) -> None:
        request_kwargs = {"request_iterator": stream.__aiter__()}

        await self._call_rpc_handler_server_stream(
            self.stream_health_check,
            stream,
            request_kwargs,
        )

    async def __rpc_fetch_health_check(self, stream: grpclib.server.Stream) -> None:
        request = await stream.recv_message()

        request_kwargs = {
            "health_check_request": request.health_check_request,
            "endpoint_health_response": request.endpoint_health_response,
        }

        response = await self.fetch_health_check(**request_kwargs)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/envoy.service.discovery.v2.HealthDiscoveryService/StreamHealthCheck": grpclib.const.Handler(
                self.__rpc_stream_health_check,
                grpclib.const.Cardinality.STREAM_STREAM,
                HealthCheckRequestOrEndpointHealthResponse,
                HealthCheckSpecifier,
            ),
            "/envoy.service.discovery.v2.HealthDiscoveryService/FetchHealthCheck": grpclib.const.Handler(
                self.__rpc_fetch_health_check,
                grpclib.const.Cardinality.UNARY_UNARY,
                HealthCheckRequestOrEndpointHealthResponse,
                HealthCheckSpecifier,
            ),
        }


class AggregatedDiscoveryServiceBase(ServiceBase):
    async def stream_aggregated_resources(
        self, request_iterator: AsyncIterator["___api_v2__.DiscoveryRequest"]
    ) -> AsyncIterator["___api_v2__.DiscoveryResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def delta_aggregated_resources(
        self, request_iterator: AsyncIterator["___api_v2__.DeltaDiscoveryRequest"]
    ) -> AsyncIterator["___api_v2__.DeltaDiscoveryResponse"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_stream_aggregated_resources(
        self, stream: grpclib.server.Stream
    ) -> None:
        request_kwargs = {"request_iterator": stream.__aiter__()}

        await self._call_rpc_handler_server_stream(
            self.stream_aggregated_resources,
            stream,
            request_kwargs,
        )

    async def __rpc_delta_aggregated_resources(
        self, stream: grpclib.server.Stream
    ) -> None:
        request_kwargs = {"request_iterator": stream.__aiter__()}

        await self._call_rpc_handler_server_stream(
            self.delta_aggregated_resources,
            stream,
            request_kwargs,
        )

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/envoy.service.discovery.v2.AggregatedDiscoveryService/StreamAggregatedResources": grpclib.const.Handler(
                self.__rpc_stream_aggregated_resources,
                grpclib.const.Cardinality.STREAM_STREAM,
                ___api_v2__.DiscoveryRequest,
                ___api_v2__.DiscoveryResponse,
            ),
            "/envoy.service.discovery.v2.AggregatedDiscoveryService/DeltaAggregatedResources": grpclib.const.Handler(
                self.__rpc_delta_aggregated_resources,
                grpclib.const.Cardinality.STREAM_STREAM,
                ___api_v2__.DeltaDiscoveryRequest,
                ___api_v2__.DeltaDiscoveryResponse,
            ),
        }


from ....api import v2 as ___api_v2__
from ....api.v2 import core as ___api_v2_core__
from ....api.v2 import endpoint as ___api_v2_endpoint__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
