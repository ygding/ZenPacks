from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

ol_status = ['unknown', 'online(1)', 'offline(2)']
rope_status = ['unknown', 'noStatus(1)', 'normal(2)', 'unknown', 'highCritical(4)', 'unknown', 'unknown', 'sensorError(7)']

class AKCPWaterRope(SnmpPlugin):
    relname = 'akcpwaterRopes'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPWaterRope'

    snmpGetTableMaps = (
        GetTableMap(
            'WaterSensorEntry', '1.3.6.1.4.1.3854.2.3.21.1', {
                '.2': 'SensorWaterRopeDescription',
                '.4': 'SensorWaterRopeLeakLocation',
                '.5': 'SensorWaterRopeUnit',
                '.6': 'SensorWaterRopeStatus',
                '.8': 'SensorWaterRopeOnline',
                '.20': 'SensorWaterRopeRaw',
                }
            ),
        )

    def process(self, device, results, log):
        ac_sensors = results[1].get('WaterSensorEntry', {})

        rm = self.relMap()
        for snmpindex, row in ac_sensors.items():
            name = row.get('SensorWaterRopeDescription')
            if not name:
                log.warn('Skipping Sensor didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'SensorWaterRopeLeakLocation': row.get('SensorWaterRopeLeakLocation'),
                'SensorWaterRopeUnit': row.get('SensorWaterRopeUnit'),
                'SensorWaterRopeRaw': row.get('SensorWaterRopeRaw'),
                'SensorWaterRopeStatus': rope_status[row.get('SensorWaterRopeStatus')],
                'SensorWaterRopeOnline': ol_status[row.get('SensorWaterRopeOnline')],
                }))

        return rm
