from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

humi_status = ['unknown', 'noStatus(1)', 'normal(2)', 'highWarning(3)', 'highCritical(4)', 'lowWarning(5)', 'lowCritical(6)', 'sensorError(7)']
ol_status = ['unknown', 'online(1)', 'offline(2)']

class AKCPHumiditySensor(SnmpPlugin):
    relname = 'akcphumiditySensors'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPHumiditySensor'

    snmpGetTableMaps = (
        GetTableMap(
            'HumiditySensorEntry', '1.3.6.1.4.1.3854.2.3.3.1', {
                '.2': 'SensorHumidityDescription',
                '.4': 'SensorHumidityPercent',
                '.6': 'SensorHumidityStatus',
                '.8': 'SensorHumidityOnline',
                '.9': 'SensorHumidityLowCritical',
                '.10': 'SensorHumidityLowWarning',
                '.11': 'SensorHumidityHighWarning',
                '.12': 'SensorHumidityHighCritical',
                '.35': 'SensorPort',
                }
            ),
        )

    def process(self, device, results, log):
        humidity_sensors = results[1].get('HumiditySensorEntry', {})

        rm = self.relMap()
        for snmpindex, row in humidity_sensors.items():
            name = row.get('SensorHumidityDescription')
            if not name:
                log.warn('Skipping Sensor didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'SensorHumidityPercent': row.get('SensorHumidityPercent'),
                'SensorHumidityStatus': humi_status[row.get('SensorHumidityStatus')],
                'SensorPort': row.get('SensorPort'),
                'SensorHumidityOnline': ol_status[row.get('SensorHumidityOnline')],
                'SensorHumidityHighWarning': row.get('SensorHumidityHighWarning'),
                'SensorHumidityHighCritical': row.get('SensorHumidityHighCritical'),
                'SensorHumidityLowWarning': row.get('SensorHumidityLowWarning'),
                'SensorHumidityLowCritical': row.get('SensorHumidityLowCritical'),
                }))

        return rm
