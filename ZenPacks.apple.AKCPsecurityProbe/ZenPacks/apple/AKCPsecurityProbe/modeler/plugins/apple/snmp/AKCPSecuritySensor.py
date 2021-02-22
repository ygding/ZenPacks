from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

ol_status = ['unknown', 'online(1)', 'offline(2)']
wd_status = ['unknown', 'noStatus(1)', 'Closed(2)', 'unknown', 'Opened(4)', 'unknown', 'Opened(6)', 'sensorError(7)', 'outputLow(8)', 'outputHigh(9)']

class AKCPSecuritySensor(SnmpPlugin):
    relname = 'akcpsecuritySensors'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPSecuritySensor'

    snmpGetTableMaps = (
        GetTableMap(
            'SecuritySensorEntry', '1.3.6.1.4.1.3854.2.3.10.1', {
                '.2': 'SecuritySensorDescription',
                '.6': 'SecuritySensorStatus',
                '.8': 'SecuritySensorOnline',
                '.35': 'SensorPort',
                }
            ),
        )

    def process(self, device, results, log):
        wd_sensors = results[1].get('SecuritySensorEntry', {})

        rm = self.relMap()
        for snmpindex, row in wd_sensors.items():
            name = row.get('SecuritySensorDescription')
            if not name:
                log.warn('Skipping Sensor didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'SecuritySensorStatus': wd_status[row.get('SecuritySensorStatus')],
                'SecuritySensorOnline': ol_status[row.get('SecuritySensorOnline')],
                'SensorPort': row.get('SensorPort'),
                }))

        return rm
