"""Base entities for SDCP Printer integration."""

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SDCPPrinterDataUpdateCoordinator


class BaseSDCPPrinterEntity(CoordinatorEntity[SDCPPrinterDataUpdateCoordinator]):
    """Base class for SDCP Printer entities."""

    def __init__(self, coordinator: SDCPPrinterDataUpdateCoordinator):
        """Constructor"""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.printer.uuid

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
