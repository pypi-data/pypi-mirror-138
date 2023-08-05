# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/filter/http/aws_request_signing/v2alpha/aws_request_signing.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class AwsRequestSigning(betterproto.Message):
    """Top level configuration for the AWS request signing filter."""

    # The `service namespace <https://docs.aws.amazon.com/general/latest/gr/aws-
    # arns-and-namespaces.html#genref-aws-service-namespaces>`_ of the HTTP
    # endpoint. Example: s3
    service_name: str = betterproto.string_field(1)
    # The `region <https://docs.aws.amazon.com/general/latest/gr/rande.html>`_
    # hosting the HTTP endpoint. Example: us-west-2
    region: str = betterproto.string_field(2)
    # Indicates that before signing headers, the host header will be swapped with
    # this value. If not set or empty, the original host header value will be
    # used and no rewrite will happen. Note: this rewrite affects both signing
    # and host header forwarding. However, this option shouldn't be used with
    # :ref:`HCM host rewrite <envoy_api_field_route.RouteAction.host_rewrite>`
    # given that the value set here would be used for signing whereas the value
    # set in the HCM would be used for host header forwarding which is not the
    # desired outcome.
    host_rewrite: str = betterproto.string_field(3)
