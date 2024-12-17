DOMAIN = "sdcp_printer"


def setup(hass, config):
    hass.states.set("sdcp_printer.test", "Hello World")
    return True
