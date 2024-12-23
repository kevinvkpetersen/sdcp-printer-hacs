import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.exceptions import ConfigEntryError

import sdcp_printer.scanner

DOMAIN = 'sdcp_printer'

_logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.states.async_set(f"{DOMAIN}.test", "Hello World")

    printers = sdcp_printer.scanner.discover_devices()
    _logger.info(f'Found {len(printers)} printers')
    if not printers:
        raise ConfigEntryError('No printers found')

    printers[0].refresh_status()

    hass.data[DOMAIN] = {
        'printer': printers[0]
    }

    return True
