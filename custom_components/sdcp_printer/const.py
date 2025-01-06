"""Constants for the SDCP Printer integration."""

from enum import StrEnum

# Integration constants
DOMAIN = "sdcp_printer"
PLATFORMS = ["sensor"]

# Config Flow
CONF_IP_ADDRESS = "ip_address"


class SDCPMachineStatusKey(StrEnum):
    """Translation keys for the machine status."""

    IDLE = "idle"
    PRINTING = "printing"
    FILE_TRANSFER = "file_transfer"
    EXPOSURE_TEST = "exposure_test"
    DEVICE_TEST = "device_test"
