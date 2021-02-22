from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

ol_status = ['unknown', 'online(1)', 'offline(2)']
ac_status = ['unknown', 'noStatus(1)', 'normal(2)', 'highCritical(3)', 'lowCritical(4)', 'sensorError(5)', 'relayOn(6)', 'relayOff(7)']

class AKCPACvoltage(SnmpPlugin):
    relname = 'akcpacvoltages'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPACvoltage'

    snmpGetTableMaps = (
        GetTableMap(
            'ACvoltageSensorEntry', '1.3.6.1.4.1.3854.2.3.13.1', {
                '.2': 'SensorACvoltageDescription',
                '.6': 'SensorACvoltageStatus',
                '.8': 'SensorACvoltageOnline',
                '.35': 'SensorPort',
                }
            ),
        )

    def process(self, device, results, log):
        ac_sensors = results[1].get('ACvoltageSensorEntry', {})

        rm = self.relMap()
        for snmpindex, row in ac_sensors.items():
            name = row.get('SensorACvoltageDescription')
            if not name:
                log.warn('Skipping Sensor didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'SensorACvoltageStatus': ac_status[row.get('SensorACvoltageStatus')],
                'SensorACvoltageOnline': ol_status[row.get('SensorACvoltageOnline')],
                'SensorPort': row.get('SensorPort'),
                }))

        return rm
