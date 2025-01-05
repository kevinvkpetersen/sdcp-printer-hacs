"""Sensors for SDCP printers."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from sdcp_printer.enum import SDCPMachineStatus

from .const import DOMAIN, SDCPMachineStatusKey
from .coordinator import SDCPPrinterDataUpdateCoordinator
from .entity import BaseSDCPPrinterEntity

CURRENT_STATUS_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="current_status",
    device_class=SensorDeviceClass.ENUM,
    options=list(SDCPMachineStatusKey),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: SDCPPrinterDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            SDCPPrinterCurrentStatusSensor(
                coordinator, CURRENT_STATUS_SENSOR_DESCRIPTION
            ),
        ]
    )


class SDCPPrinterCurrentStatusSensor(BaseSDCPPrinterEntity, SensorEntity):
    """Sensor for the printer status."""

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        current_status: list[SDCPMachineStatus] = (
            self.coordinator.printer.current_status
        )
        if not current_status:
            return None

        if SDCPMachineStatus.IDLE in current_status:
            return SDCPMachineStatusKey.IDLE.value
        if SDCPMachineStatus.PRINTING in current_status:
            return SDCPMachineStatusKey.PRINTING.value
        if SDCPMachineStatus.EXPOSURE_TEST in current_status:
            return SDCPMachineStatusKey.EXPOSURE_TEST.value
        if SDCPMachineStatus.DEVICE_TEST in current_status:
            return SDCPMachineStatusKey.DEVICE_TEST.value
        if SDCPMachineStatus.FILE_TRANSFER in current_status:
            return SDCPMachineStatusKey.FILE_TRANSFER.value

        return None
