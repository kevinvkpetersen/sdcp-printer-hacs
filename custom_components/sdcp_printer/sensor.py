"""Sensors for SDCP printers."""

from homeassistant.components.sensor import SensorEntity
from sdcp_printer import SDCPPrinter

from . import DOMAIN


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([SDCPPrinterStatusSensor()])


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
