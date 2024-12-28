"""SDCP Printer integration for Home Assistant."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from sdcp_printer import SDCPPrinter

from .const import DOMAIN

_logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up a printer from a config entry."""

    printer: SDCPPrinter = config_entry.data["printer"]
    _logger.debug("Setting up printer: %s", printer.ip_address)
    printer.refresh_status()

    hass.data[DOMAIN] = {"printer": printer}

    await hass.config_entries.async_forward_entry_setup(config_entry, "sensor")

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a printer config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(
        config_entry, "sensor"
    )

    if unload_ok:
        hass.data.pop(DOMAIN)

    return unload_ok
