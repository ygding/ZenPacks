from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

ol_status = ['unknown', 'online(1)', 'offline(2)']
io_status = ['input(0)', 'output(1)']
dc_status = ['unknown', 'noStatus(1)', 'normal(2)', 'unknown', 'highCritical(4)', 'unknown', 'lowCritical(6)', 'sensorError(7)', 'outputLow(8)', 'outputHigh(9)']

class AKCPWetContact(SnmpPlugin):
    relname = 'akcpwetContacts'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPWetContact'

    snmpGetTableMaps = (
        GetTableMap(
            'DryContactEntry', '1.3.6.1.4.1.3854.2.3.4.1', {
                '.2': 'SensorDryContactDescription',
                '.6': 'SensorDryContactStatus',
                '.8': 'SensorDryContactOnline',
                '.22': 'SensorDryContactDirection',
                }
            ),
        )

    def process(self, device, results, log):
        dc_sensors = results[1].get('DryContactEntry', {})

        rm = self.relMap()
        for snmpindex, row in dc_sensors.items():
            name = row.get('SensorDryContactDescription')
            if not name:
                log.warn('Skipping Sensor didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'SensorDryContactStatus': dc_status[row.get('SensorDryContactStatus')],
                'SensorDryContactOnline': ol_status[row.get('SensorDryContactOnline')],
                'SensorDryContactDirection': io_status[row.get('SensorDryContactDirection')],
                }))

        return rm
