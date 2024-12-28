"""Config flow for SDCP Printer integration."""

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow

from .const import CONF_IP_ADDRESS, DOMAIN


class SDCPPrinterConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for adding a printer."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_IP_ADDRESS],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_IP_ADDRESS): str,
                }
            ),
        )
