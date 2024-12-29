"""Base entities for SDCP Printer integration."""

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .coordinator import SDCPPrinterDataUpdateCoordinator


class BaseSDCPPrinterEntity(CoordinatorEntity[SDCPPrinterDataUpdateCoordinator]):
    """Base class for SDCP Printer entities."""

    def __init__(self, coordinator: SDCPPrinterDataUpdateCoordinator):
        """Constructor"""
        super().__init__(coordinator)
