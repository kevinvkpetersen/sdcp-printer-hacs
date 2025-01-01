"""Config flow for SDCP Printer integration."""

import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow

from sdcp_printer import SDCPPrinter

from .const import CONF_IP_ADDRESS, DOMAIN

_logger = logging.getLogger(__package__)


class SDCPPrinterConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for adding a printer."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            try:
                await SDCPPrinter.get_printer_async(user_input[CONF_IP_ADDRESS])
            except TimeoutError as exception:
                _logger.warning("Failed to connect to printer: %s", exception)
                errors["base"] = "connection"
            except AttributeError as exception:
                _logger.warning("Failed to parse printer response: %s", exception)
                errors["base"] = "invalid_response"
            except Exception as exception:
                _logger.exception("Unexpected error: %s", exception)
                errors["base"] = "unknown"
            else:
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
            errors=errors,
        )
