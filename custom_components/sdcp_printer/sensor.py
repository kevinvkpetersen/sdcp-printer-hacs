from homeassistant.components.sensor import SensorEntity

from . import DOMAIN
from sdcp_printer.printer import SDCPPrinter


def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([SDCPPrinterStatusSensor()])


class SDCPPrinterStatusSensor(SensorEntity):
    def __init__(self):
        self._state = None

    @property
    def name(self):
        return 'Printer Status'

    @property
    def state(self):
        return self._state

    def update(self):
        printer: SDCPPrinter = self.hass.data[DOMAIN]['printer']

        self._state = printer._status
