"""SDCP Printer integration for Home Assistant."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryError
from homeassistant.helpers.typing import ConfigType
from sdcp_printer import SDCPPrinter

DOMAIN = "sdcp_printer"

_logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the SDCP Printer component."""
    hass.states.async_set(f"{DOMAIN}.test", "Hello World")

    printer_configs = config[DOMAIN].get("printers")
    if not printer_configs:
        raise ConfigEntryError("No printers configured")

    printer_ip = printer_configs[0].get("ip")
    printer = SDCPPrinter.get_printer_info(printer_ip)
    printer.refresh_status()

    hass.data[DOMAIN] = {"printer": printer}

    hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)

    return True
