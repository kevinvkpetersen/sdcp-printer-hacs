"""SDCP Printer integration for Home Assistant."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from sdcp_printer import SDCPPrinter

from .const import CONF_IP_ADDRESS, DOMAIN, PLATFORMS

_logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up a printer from a config entry."""

    printer_ip = config_entry.data[CONF_IP_ADDRESS]
    _logger.debug("Setting up printer: %s", printer_ip)
    printer = SDCPPrinter.get_printer_info(printer_ip)
    printer.refresh_status()

    hass.data[DOMAIN] = {"printer": printer}

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a printer config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data.pop(DOMAIN)

    return unload_ok
