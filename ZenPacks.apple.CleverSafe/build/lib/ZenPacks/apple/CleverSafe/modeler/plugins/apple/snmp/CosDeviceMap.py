from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CosDeviceMap(SnmpPlugin):
#    relname = 'cosDeviceMaps'
    modname = 'ZenPacks.apple.CleverSafe.CosDeviceMap'

    snmpGetMap = GetMap ({
        '.1.3.6.1.4.1.28129.1.3.4.2.6.0': 'setHWSerialNumber',
        '.1.3.6.1.4.1.28129.1.3.4.2.7.0': 'setHWProductKey',
        '.1.3.6.1.4.1.28129.1.3.4.2.5.0': 'setOSProductKey',
        })

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        log.warning("Get Data = %s", getdata)
        log.warning("Table Data = %s", tabledata)
        om = self.objectMap(getdata)
        om.setHWSerialNumber = str(om.setHWSerialNumber)
        om.setHWProductKey = MultiArgs(om.setHWProductKey, "IBM")
        om.setOSProductKey = MultiArgs(om.setOSProductKey, "ClevOS")
        return om
