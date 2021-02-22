from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class AKCPDeviceMap(SnmpPlugin):
#    relname = 'cosDeviceMaps'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPDeviceMap'

    snmpGetMap = GetMap ({
        '.1.3.6.1.4.1.3854.1.2.2.1.3.0': 'setHWSerialNumber',
        })

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        log.warning("Get Data = %s", getdata)
        log.warning("Table Data = %s", tabledata)
        om = self.objectMap(getdata)
        om.setHWSerialNumber = str(om.setHWSerialNumber).replace(":","-")
        return om
