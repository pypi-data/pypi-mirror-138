# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/data/cluster/v3/outlier_detection_event.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class OutlierEjectionType(betterproto.Enum):
    """Type of ejection that took place"""

    # In case upstream host returns certain number of consecutive 5xx. If :ref:`o
    # utlier_detection.split_external_local_origin_errors<envoy_v3_api_field_conf
    # ig.cluster.v3.OutlierDetection.split_external_local_origin_errors>` is
    # *false*, all type of errors are treated as HTTP 5xx errors. See
    # :ref:`Cluster outlier detection <arch_overview_outlier_detection>`
    # documentation for details.
    CONSECUTIVE_5XX = 0
    # In case upstream host returns certain number of consecutive gateway errors
    CONSECUTIVE_GATEWAY_FAILURE = 1
    # Runs over aggregated success rate statistics from every host in cluster and
    # selects hosts for which ratio of successful replies deviates from other
    # hosts in the cluster. If :ref:`outlier_detection.split_external_local_origi
    # n_errors<envoy_v3_api_field_config.cluster.v3.OutlierDetection.split_extern
    # al_local_origin_errors>` is *false*, all errors (externally and locally
    # generated) are used to calculate success rate statistics. See :ref:`Cluster
    # outlier detection <arch_overview_outlier_detection>` documentation for
    # details.
    SUCCESS_RATE = 2
    # Consecutive local origin failures: Connection failures, resets, timeouts,
    # etc This type of ejection happens only when :ref:`outlier_detection.split_e
    # xternal_local_origin_errors<envoy_v3_api_field_config.cluster.v3.OutlierDet
    # ection.split_external_local_origin_errors>` is set to *true*. See
    # :ref:`Cluster outlier detection <arch_overview_outlier_detection>`
    # documentation for
    CONSECUTIVE_LOCAL_ORIGIN_FAILURE = 3
    # Runs over aggregated success rate statistics for local origin failures for
    # all hosts in the cluster and selects hosts for which success rate deviates
    # from other hosts in the cluster. This type of ejection happens only when :r
    # ef:`outlier_detection.split_external_local_origin_errors<envoy_v3_api_field
    # _config.cluster.v3.OutlierDetection.split_external_local_origin_errors>` is
    # set to *true*. See :ref:`Cluster outlier detection
    # <arch_overview_outlier_detection>` documentation for
    SUCCESS_RATE_LOCAL_ORIGIN = 4
    # Runs over aggregated success rate statistics from every host in cluster and
    # selects hosts for which ratio of failed replies is above configured value.
    FAILURE_PERCENTAGE = 5
    # Runs over aggregated success rate statistics for local origin failures from
    # every host in cluster and selects hosts for which ratio of failed replies
    # is above configured value.
    FAILURE_PERCENTAGE_LOCAL_ORIGIN = 6


class Action(betterproto.Enum):
    """Represents possible action applied to upstream host"""

    # In case host was excluded from service
    EJECT = 0
    # In case host was brought back into service
    UNEJECT = 1


@dataclass(eq=False, repr=False)
class OutlierDetectionEvent(betterproto.Message):
    """[#next-free-field: 12]"""

    # In case of eject represents type of ejection that took place.
    type: "OutlierEjectionType" = betterproto.enum_field(1)
    # Timestamp for event.
    timestamp: datetime = betterproto.message_field(2)
    # The time in seconds since the last action (either an ejection or
    # unejection) took place.
    secs_since_last_action: Optional[int] = betterproto.message_field(
        3, wraps=betterproto.TYPE_UINT64
    )
    # The :ref:`cluster <envoy_v3_api_msg_config.cluster.v3.Cluster>` that owns
    # the ejected host.
    cluster_name: str = betterproto.string_field(4)
    # The URL of the ejected host. E.g., ``tcp://1.2.3.4:80``.
    upstream_url: str = betterproto.string_field(5)
    # The action that took place.
    action: "Action" = betterproto.enum_field(6)
    # If ``action`` is ``eject``, specifies the number of times the host has been
    # ejected (local to that Envoy and gets reset if the host gets removed from
    # the upstream cluster for any reason and then re-added).
    num_ejections: int = betterproto.uint32_field(7)
    # If ``action`` is ``eject``, specifies if the ejection was enforced.
    # ``true`` means the host was ejected. ``false`` means the event was logged
    # but the host was not actually ejected.
    enforced: bool = betterproto.bool_field(8)
    eject_success_rate_event: "OutlierEjectSuccessRate" = betterproto.message_field(
        9, group="event"
    )
    eject_consecutive_event: "OutlierEjectConsecutive" = betterproto.message_field(
        10, group="event"
    )
    eject_failure_percentage_event: "OutlierEjectFailurePercentage" = (
        betterproto.message_field(11, group="event")
    )


@dataclass(eq=False, repr=False)
class OutlierEjectSuccessRate(betterproto.Message):
    # Host’s success rate at the time of the ejection event on a 0-100 range.
    host_success_rate: int = betterproto.uint32_field(1)
    # Average success rate of the hosts in the cluster at the time of the
    # ejection event on a 0-100 range.
    cluster_average_success_rate: int = betterproto.uint32_field(2)
    # Success rate ejection threshold at the time of the ejection event.
    cluster_success_rate_ejection_threshold: int = betterproto.uint32_field(3)


@dataclass(eq=False, repr=False)
class OutlierEjectConsecutive(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class OutlierEjectFailurePercentage(betterproto.Message):
    # Host's success rate at the time of the ejection event on a 0-100 range.
    host_success_rate: int = betterproto.uint32_field(1)
