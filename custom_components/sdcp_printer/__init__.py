"""SDCP Printer integration for Home Assistant."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from sdcp_printer import SDCPPrinter

from .const import CONF_IP_ADDRESS, DOMAIN

_logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up a printer from a config entry."""

    printer_ip = config_entry.data[CONF_IP_ADDRESS]
    printer = SDCPPrinter.get_printer_info(printer_ip)
    printer.refresh_status()

    hass.data[DOMAIN] = {"printer": printer}

    await hass.config_entries.async_forward_entry_setup(config_entry, "sensor")

    return True
