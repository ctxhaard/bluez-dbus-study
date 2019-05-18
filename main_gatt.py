#!/usr/bin/python3

import dbus
import dbus.mainloop.glib
from socket import gethostname
from util import find_adapter
from gatt import Application, Service, Characteristic

from gi.repository import GObject
import sys

mainloop = None

BLUEZ_SERVICE_NAME = 'org.bluez'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'

class PCMonService(Service):
    """
    Provides information about a PC

    """
    UUID = 'ce5b796b-5337-4877-a1a2-948b4fbc8669'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(NameChrc(bus, 0, self))
#        self.add_characteristic(BatteryLevelChrc(bus, 1, self))
#        self.add_characteristic(IPv4Chrc(bus, 2, self))
#        self.add_characteristic(IPv6Chrc(bus, 3, self))
#        self.add_characteristic(CoreTempChrc(bus, 4, self))
        self.energy_expended = 0

class NameChrc(Characteristic):
    UUID = '5b1082dc-c61d-4db3-9384-f7036a0b4e91'

    def __init__(self, bus, index, service):
        Characteristic.__init__(
                self, bus, index,
                self.UUID,
                ['read'],
                service)

#    @util.log
    def ReadValue(self, options):
        s = gethostname()
        ay = [dbus.Byte(c) for c in bytes(s, 'utf-8')]
        return ay

# TODO: definire le caratteristiche del mio servizio

def register_app_cb():
    print('GATT application registered')


def register_app_error_cb(error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()

class PCMonApplication(Application):

    def __init__(self, bus):
        Application.__init__(self, bus)
        self.add_service(PCMonService(bus, 0))
        

def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    adapter = find_adapter(bus)
    if not adapter:
        print('GattManager1 interface not found')
        return

    service_manager = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, adapter),
            GATT_MANAGER_IFACE)

    app = PCMonApplication(bus)

    mainloop = GObject.MainLoop()

    print('Registering GATT application...')

    service_manager.RegisterApplication(app.get_path(), {},
                                    reply_handler=register_app_cb,
                                    error_handler=register_app_error_cb)

    mainloop.run()

if __name__ == '__main__':
    main()
