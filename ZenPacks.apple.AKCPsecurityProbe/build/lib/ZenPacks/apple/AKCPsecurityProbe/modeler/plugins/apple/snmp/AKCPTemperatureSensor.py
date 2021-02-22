from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

temp_status = ['unknown', 'noStatus(1)', 'normal(2)', 'highWarning(3)', 'highCritica(4)', 'lowWarning(5)', 'lowCritical(6)', 'sensorError(7)']
ol_status = ['unknown', 'online(1)', 'offline(2)']

class AKCPTemperatureSensor(SnmpPlugin):
    relname = 'akcptemperatureSensors'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPTemperatureSensor'

    snmpGetTableMaps = (
        GetTableMap(
            'tempSensorEntity', '1.3.6.1.4.1.3854.2.3.2.1', {
                '.2': 'SensorTempDescription',
                '.20': 'SensorTempDegree',
                '.5': 'SensorTempDegreeType',
                '.6': 'SensorTempStatus',
                '.8': 'SensorTempOnline',
                '.11': 'SensorTempHighWarning',
                '.12': 'SensorTempHighCritical',
                '.10': 'SensorTempLowWarning',
                '.9': 'SensorTempLowCritical',
                '.35': 'SensorPort',
                }
            ),
        )

    def process(self, device, results, log):
        temp_sensors = results[1].get('tempSensorEntity', {})

        rm = self.relMap()
        for snmpindex, row in temp_sensors.items():
            name = row.get('SensorTempDescription')
            if not name:
                log.warn('Skipping temperature sensor with no name')
                continue
            THW = row.get('SensorTempHighWarning')
            THC = row.get('SensorTempHighCritical')
            TLW = row.get('SensorTempLowWarning')
            TLC = row.get('SensorTempLowCritical')
            if THC > 100:
                THW = THW*0.1
                THC = THC*0.1
                TLW = TLW*0.1
                TLC = TLC*0.1

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'SensorTempDegree': row.get('SensorTempDegree')*0.1,
                'SensorTempDegreeType': row.get('SensorTempDegreeType'),
                'SensorPort': row.get('SensorPort'),
                'SensorTempStatus': temp_status[row.get('SensorTempStatus')],
                'SensorTempOnline': ol_status[row.get('SensorTempOnline')],
                'SensorTempHighWarning': THW,
                'SensorTempHighCritical': THC,
                'SensorTempLowWarning': TLW,
                'SensorTempLowCritical': TLC,
                }))

        return rm
