"""Base entities for SDCP Printer integration."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SDCPPrinterDataUpdateCoordinator


@dataclass(kw_only=True)
class BaseSDCPPrinterEntityDescription(EntityDescription):
    """Base class for SDCP Printer entity descriptions."""

    value_fn: Callable[[SDCPPrinterDataUpdateCoordinator], StateType]


class BaseSDCPPrinterEntity(CoordinatorEntity[SDCPPrinterDataUpdateCoordinator]):
    """Base class for SDCP Printer entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SDCPPrinterDataUpdateCoordinator,
        entity_description: BaseSDCPPrinterEntityDescription,
    ):
        """Constructor"""
        super().__init__(coordinator)
        self.entity_description = entity_description
        entity_key = entity_description.key
        self._attr_translation_key = entity_key
        self._attr_unique_id = f"{coordinator.printer.uuid}_{entity_key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.printer.uuid)},
            name=self.coordinator.printer.name,
            manufacturer=self.coordinator.printer.manufacturer,
            model=self.coordinator.printer.model,
            sw_version=self.coordinator.printer.firmware_version,
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the entity."""
        return self.entity_description.value_fn(self.coordinator)
