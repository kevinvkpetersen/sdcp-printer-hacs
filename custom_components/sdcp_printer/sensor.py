"""Sensors for SDCP printers."""

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# pylint: disable-next=import-error, no-name-in-module
from sdcp_printer.enum import SDCPMachineStatus

from .const import DOMAIN, SDCPMachineStatusKey
from .coordinator import SDCPPrinterDataUpdateCoordinator
from .entity import BaseSDCPPrinterEntity, BaseSDCPPrinterEntityDescription


@dataclass(kw_only=True)
class SDCPSensorEntityDescription(
    BaseSDCPPrinterEntityDescription, SensorEntityDescription
):
    """Base class for SDCP Printer sensor entity descriptions."""


CURRENT_STATUS_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="current_status",
    device_class=SensorDeviceClass.ENUM,
    options=list(SDCPMachineStatusKey),
)

SENSOR_DESCRIPTIONS = [
    SDCPSensorEntityDescription(
        key="uv_led_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda coordinator: coordinator.printer.uv_led_temperature,
    ),
]


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
            *[
                SDCPPrinterSensor(coordinator, description)
                for description in SENSOR_DESCRIPTIONS
            ],
        ]
    )


class SDCPPrinterSensor(BaseSDCPPrinterEntity, SensorEntity):
    """Generic sensor for the printer."""


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
