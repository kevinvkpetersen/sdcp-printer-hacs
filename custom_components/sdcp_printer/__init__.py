"""SDCP Printer integration for Home Assistant."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from sdcp_printer import SDCPPrinter

from .const import CONF_IP_ADDRESS, DOMAIN, PLATFORMS
from .coordinator import SDCPPrinterDataUpdateCoordinator

_logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a printer from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    printer_ip = entry.data[CONF_IP_ADDRESS]
    _logger.debug("Setting up printer: %s", printer_ip)
    printer = await SDCPPrinter.get_printer_async(printer_ip)

    coordinator = SDCPPrinterDataUpdateCoordinator(hass, printer)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a printer config entry."""
    coordinator: SDCPPrinterDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.printer.stop_listening_async()

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        domain_data = hass.data.get(DOMAIN)
        if domain_data:
            domain_data.pop(entry.entry_id)

    return unload_ok
