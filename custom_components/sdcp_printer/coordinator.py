"""Data update coordinator for fetching data from SDCP printers."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from sdcp_printer import SDCPPrinter
from sdcp_printer.enum import SDCPFrom

from .const import DOMAIN

_logger = logging.getLogger(__package__)


class SDCPPrinterDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from SDCP printers."""

    def __init__(self, hass: HomeAssistant, printer: SDCPPrinter):
        """Constructor."""
        super().__init__(
            hass,
            logger=_logger,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )
        self.printer = printer

    async def _async_setup(self):
        """Start listening for printer updates."""
        self.printer.register_callback(self._handle_callback)
        self.hass.async_create_background_task(
            self.printer.start_listening_async(),
            "Printer Listener",
        )
        await self.printer.wait_for_connection_async()

    def _handle_callback(self, data):
        """Handle printer updates."""
        self.async_set_updated_data(data)

    async def _async_update_data(self):
        """Fetch data from the printer."""
        await self.printer.refresh_status_async(sdcp_from=SDCPFrom.SERVER)
