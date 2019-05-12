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

        <property name="LocalName" type="s" access="read"/>
        <property name="Type" type="s" access="read"/>
        <property name="ServiceUUIDs" type="as" access="read"/>
        <property name="ManufacturerData" type="a{sv}" access="read"/>
        <property name="SolicitUUIDs" type="as" access="read"/>
        <property name="ServiceData" type="a{sv}" access="read"/>
        <property name="IncludeTxPower" type="b" access="read"/>
    </interface>
</node>
    """

    def Release(self):
        print("released!!!")

    @property
    @log
    def LocalName(self):
        return "Carlo!"

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
    def ManufacturerData(self):
        return None
    
    @property
    @log
    def SolicitUUIDs(self):
        return []

    @property
    @log
    def ServiceData(self):
        return []

    @property
    @log
    def IncludeTxPower(self):
        return True

if __name__ == '__main__':
    bus = SystemBus()
    loop = GLib.MainLoop()
    bus.register_object('/org/bluez/example/advertisement0', LEAdvertisement1(), None)

    mgr = bus.get('org.bluez','/org/bluez/hci0')
    mgr.RegisterAdvertisement('/org/bluez/example/advertisement0', {})
    loop.run()
