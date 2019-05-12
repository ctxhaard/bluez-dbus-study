from pydbus import SystemBus
from gi.repository import GLib

def log(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args,**kwargs)
    return wrapper

class LEAdvertisement1:
    """
<node>
    <interface name="org.bluez.LEAdvertisement1">
        <method name="Release">
            <annotation name="org.freedesktop.DBus.Method.NoReply" value="true"/>
        </method>
        <annotation name="org.freedesktop.DBus.Properties.PropertiesChanged" value="const"/>
        <property name="Type" type="s" access="read"/>
        <property name="ServiceUUIDs" type="as" access="read"/>
        <property name="SolicitUUIDs" type="as" access="read"/>
        <property name="ManufacturerData" type="a{qv}" access="read"/>
        <property name="ServiceData" type="a{qv}" access="read"/>
        <property name="Includes" type="as" access="read"/>
        <property name="LocalName" type="s" access="read"/>
        <property name="Appearance" type="q" access="read"/>
        <property name="Duration" type="q" access="read"/>
        <property name="Timeout" type="q" access="read"/>
    </interface>
</node>
    """

    def Release(self):
        print("released!!!")

    @property
    @log
    def Type(self):
        return 'peripheral'

    @property
    @log
    def ServiceUUIDs(self):
        return ['180D', '180F']

    @property
    @log
    def SolicitUUIDs(self):
        return []

    @property
    @log
    def ManufacturerData(self):
        return { 0xFFFF: GLib.Variant("ay", [0x00, 0x01, 0x02, 0x03, 0x04]) }
    
    @property
    @log
    def ServiceData(self):
        return { 0x9999: GLib.Variant("ay", [0x01, 0x02, 0x03, 0x04, 0x05]) }

    @property
    @log
    def Includes(self):
        return []

    @property
    @log
    def LocalName(self):
        return "CARLO"

    @property
    @log
    def Appearance(self):
        return 0x00C1

    @property
    @log
    def Duration(self):
        return 2

    @property
    @log
    def Timeout(self):
        return 120

 
if __name__ == '__main__':
    bus = SystemBus()
    loop = GLib.MainLoop()

    obj_path = '/org/bluez/example/advertisement0'
    bus.register_object(obj_path, LEAdvertisement1(), None)

    mgr = bus.get('org.bluez','/org/bluez/hci0')

    try:
        print('Registering advertisement')
        mgr.RegisterAdvertisement(obj_path, {})
        loop.run()
    except KeyboardInterrupt:
        print('Unregistering advertisement')
        mgr.UnregisterAdvertisement(obj_path)

