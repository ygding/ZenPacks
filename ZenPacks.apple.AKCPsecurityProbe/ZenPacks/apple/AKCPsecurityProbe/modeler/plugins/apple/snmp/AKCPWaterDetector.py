from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

ol_status = ['unknown', 'online(1)', 'offline(2)']
wd_status = ['unknown', 'noStatus(1)', 'normal(2)', 'unknown', 'highCritical(4)', 'unknown', 'lowCritical(6)', 'sensorError(7)', 'outputLow(8)', 'outputHigh(9)']

class AKCPWaterDetector(SnmpPlugin):
    relname = 'akcpwaterDetectors'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPWaterDetector'

    snmpGetTableMaps = (
        GetTableMap(
            'WaterDetectorEntry', '1.3.6.1.4.1.3854.2.3.9.1', {
                '.2': 'SensorWaterDetectorDescription',
                '.6': 'SensorWaterDetectorStatus',
                '.8': 'SensorWaterDetectorOnline',
                '.35': 'SensorPort',
                }
            ),
        )

    def process(self, device, results, log):
        wd_sensors = results[1].get('WaterDetectorEntry', {})

        rm = self.relMap()
        for snmpindex, row in wd_sensors.items():
            name = row.get('SensorWaterDetectorDescription')
            if not name:
                log.warn('Skipping Sensor didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'SensorWaterDetectorStatus': wd_status[row.get('SensorWaterDetectorStatus')],
                'SensorWaterDetectorOnline': ol_status[row.get('SensorWaterDetectorOnline')],
                'SensorPort': row.get('SensorPort'),
                }))

        return rm
