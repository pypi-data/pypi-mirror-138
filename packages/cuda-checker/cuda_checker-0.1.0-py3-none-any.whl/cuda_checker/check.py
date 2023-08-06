from __future__ import annotations

import dataclasses
import logging
import typing

import tensorflow

_LOGGER = logging.getLogger(__name__)


@typing.final
@dataclasses.dataclass(frozen=True)
class CudaPropertiesPyTorch:
    device_count: int
    current_device: int
    device_name: str
    is_available: bool


@typing.final
@dataclasses.dataclass(frozen=True)
class CudaPropertiesTensorFlow:
    physical_devices: list[tensorflow.config.PhysicalDevice]
    logical_devices: list[tensorflow.config.LogicalDevice]


def get_pytorch_properties() -> CudaPropertiesPyTorch:
    import torch

    device = torch.cuda.current_device()
    properties = CudaPropertiesPyTorch(
        device_count=torch.cuda.device_count(),
        current_device=device,
        device_name=torch.cuda.get_device_name(device),
        is_available=torch.cuda.is_available(),
    )
    _LOGGER.info(properties)
    return properties


def get_tensorflow_properties() -> CudaPropertiesTensorFlow:
    properties = CudaPropertiesTensorFlow(
        physical_devices=tensorflow.config.list_physical_devices(),
        logical_devices=tensorflow.config.list_logical_devices(),
    )
    print(type(properties.physical_devices[0]))
    _LOGGER.info(properties)
    return properties
