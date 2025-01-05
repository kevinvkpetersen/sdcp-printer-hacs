"""Sensors for SDCP printers."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from sdcp_printer.enum import SDCPMachineStatus

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
        current_status: list[SDCPMachineStatus] = (
            self.coordinator.printer.current_status
        )
        if not current_status:
            return None

        if SDCPMachineStatus.IDLE in current_status:
            return "Idle"
        if SDCPMachineStatus.PRINTING in current_status:
            return "Printing"
        if SDCPMachineStatus.EXPOSURE_TEST in current_status:
            return "Exposure Testing"
        if SDCPMachineStatus.DEVICE_TEST in current_status:
            return "Calibrating"
        if SDCPMachineStatus.FILE_TRANSFER in current_status:
            return "Uploading File"

        return "Unknown"
