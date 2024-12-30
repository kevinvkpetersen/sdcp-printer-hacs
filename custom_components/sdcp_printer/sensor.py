"""Sensors for SDCP printers."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import SDCPPrinterDataUpdateCoordinator
from .entity import BaseSDCPPrinterEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: SDCPPrinterDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SDCPPrinterStatusSensor(coordinator)])


class SDCPPrinterStatusSensor(BaseSDCPPrinterEntity, SensorEntity):
    """Sensor for the printer status."""

    _attr_name = "Printer Status"

    def __init__(self, coordinator: SDCPPrinterDataUpdateCoordinator):
        """Constructor."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.printer.id

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.printer.current_status
