"""Constants for the SDCP Printer integration."""

from enum import StrEnum

# pylint: disable-next=import-error, no-name-in-module
from sdcp_printer.enum import SDCPPrintStatus

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


class SDCPPrintStatusKey(StrEnum):
    """Translation keys for the print status."""

    IDLE = "idle"
    HOMING = "homing"
    DROPPING = "dropping"
    EXPOSING = "exposing"
    LIFTING = "lifting"
    PAUSING = "pausing"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    COMPLETE = "complete"
    FILE_CHECKING = "file_checking"


SDCP_PRINT_STATUS_MAPPING: dict[SDCPPrintStatus, SDCPPrintStatusKey] = {
    SDCPPrintStatus.IDLE: SDCPPrintStatusKey.IDLE,
    SDCPPrintStatus.HOMING: SDCPPrintStatusKey.HOMING,
    SDCPPrintStatus.DROPPING: SDCPPrintStatusKey.DROPPING,
    SDCPPrintStatus.EXPOSING: SDCPPrintStatusKey.EXPOSING,
    SDCPPrintStatus.LIFTING: SDCPPrintStatusKey.LIFTING,
    SDCPPrintStatus.PAUSING: SDCPPrintStatusKey.PAUSING,
    SDCPPrintStatus.PAUSED: SDCPPrintStatusKey.PAUSED,
    SDCPPrintStatus.STOPPING: SDCPPrintStatusKey.STOPPING,
    SDCPPrintStatus.STOPPED: SDCPPrintStatusKey.STOPPED,
    SDCPPrintStatus.COMPLETE: SDCPPrintStatusKey.COMPLETE,
    SDCPPrintStatus.FILE_CHECKING: SDCPPrintStatusKey.FILE_CHECKING,
}
