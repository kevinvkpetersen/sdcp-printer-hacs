from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "sdcp_printer"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.states.async_set(f"{DOMAIN}.test", "Hello World")
    return True
