"""Sensors for SDCP printers."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from sdcp_printer import SDCPPrinter

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([SDCPPrinterStatusSensor()])


class SDCPPrinterStatusSensor(SensorEntity):
    """Sensor for the printer status."""

    def __init__(self):
        self._state = None

    @property
    def name(self):
        return "Printer Status"

    @property
    def state(self):
        return self._state

    def update(self):
        printer: SDCPPrinter = self.hass.data[DOMAIN]["printer"]

        self._state = printer._status
