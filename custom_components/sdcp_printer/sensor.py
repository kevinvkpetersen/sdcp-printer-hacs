"""Sensors for SDCP printers."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from sdcp_printer.enum import SDCPStatus

from .const import DOMAIN
from .coordinator import SDCPPrinterDataUpdateCoordinator
from .entity import BaseSDCPPrinterEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: SDCPPrinterDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SDCPPrinterCurrentStatusSensor(coordinator)])


class SDCPPrinterCurrentStatusSensor(BaseSDCPPrinterEntity, SensorEntity):
    """Sensor for the printer status."""

    _attr_name = "Current Status"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        current_status: list[SDCPStatus] = self.coordinator.printer.current_status
        if not current_status:
            return None

        if SDCPStatus.IDLE in current_status:
            return "Idle"
        if SDCPStatus.PRINTING in current_status:
            return "Printing"
        if SDCPStatus.EXPOSURE_TESTING in current_status:
            return "Exposure Testing"
        if SDCPStatus.DEVICES_TESTING in current_status:
            return "Calibrating"
        if SDCPStatus.TRANSFERRING in current_status:
            return "Uploading File"

        return "Unknown"
