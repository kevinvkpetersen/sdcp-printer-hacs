"""Sensors for SDCP printers."""

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# pylint: disable-next=import-error, no-name-in-module
from sdcp_printer.enum import SDCPMachineStatus

from .const import (
    DOMAIN,
    SDCP_PRINT_ERROR_MAPPING,
    SDCP_PRINT_STATUS_MAPPING,
    SDCPMachineStatusKey,
    SDCPPrintErrorKey,
    SDCPPrintStatusKey,
)
from .coordinator import SDCPPrinterDataUpdateCoordinator
from .entity import BaseSDCPPrinterEntity, BaseSDCPPrinterEntityDescription


@dataclass(kw_only=True)
class SDCPSensorEntityDescription(
    BaseSDCPPrinterEntityDescription, SensorEntityDescription
):
    """Base class for SDCP Printer sensor entity descriptions."""


SENSOR_DESCRIPTIONS = [
    SDCPSensorEntityDescription(
        key="uv_led_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda coordinator: coordinator.printer.uv_led_temperature,
    ),
    SDCPSensorEntityDescription(
        key="screen_usage",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        unit_of_measurement=UnitOfTime.HOURS,
        suggested_display_precision=0,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:sun-clock-outline",
        value_fn=lambda coordinator: coordinator.printer.screen_usage,
    ),
    SDCPSensorEntityDescription(
        key="film_usage",
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:file-arrow-up-down-outline",
        value_fn=lambda coordinator: coordinator.printer.film_usage,
    ),
]

CURRENT_STATUS_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="current_status",
    device_class=SensorDeviceClass.ENUM,
    options=list(SDCPMachineStatusKey),
)

PRINT_STATUS_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="print_status",
    device_class=SensorDeviceClass.ENUM,
    options=list(SDCPPrintStatusKey),
)

PRINT_ERROR_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="print_error",
    device_class=SensorDeviceClass.ENUM,
    options=list(SDCPPrintErrorKey),
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
            *[
                SDCPPrinterSensor(coordinator, description)
                for description in SENSOR_DESCRIPTIONS
            ],
            SDCPPrinterCurrentStatusSensor(
                coordinator, CURRENT_STATUS_SENSOR_DESCRIPTION
            ),
            SDCPPrinterPrintStatusSensor(coordinator, PRINT_STATUS_SENSOR_DESCRIPTION),
            SDCPPrinterPrintErrorSensor(coordinator, PRINT_ERROR_SENSOR_DESCRIPTION),
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


class SDCPPrinterPrintStatusSensor(BaseSDCPPrinterEntity, SensorEntity):
    """Sensor for the print job status."""

    @property
    def native_value(self) -> str:
        if self.coordinator.printer.print_status is not None:
            return SDCP_PRINT_STATUS_MAPPING.get(self.coordinator.printer.print_status)

        return None


class SDCPPrinterPrintErrorSensor(BaseSDCPPrinterEntity, SensorEntity):
    """Sensor for the print job error."""

    @property
    def native_value(self) -> str:
        if self.coordinator.printer.print_error is not None:
            return SDCP_PRINT_ERROR_MAPPING.get(self.coordinator.printer.print_error)

        return None
