"""Data update coordinator for fetching data from SDCP printers."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from sdcp_printer import SDCPPrinter

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
            update_interval=timedelta(seconds=10),
        )
        self.printer = printer

    async def _async_update_data(self):
        """Fetch data from the printer."""
        self.printer.refresh_status()
