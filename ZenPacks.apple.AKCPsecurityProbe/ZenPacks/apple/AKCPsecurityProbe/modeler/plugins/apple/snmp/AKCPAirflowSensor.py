from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )

af_status = ['unknown', 'noStatus(1)', 'normal(2)', 'unknown', 'highCritical(4)', 'unknown', 'lowCritical(6)', 'sensorError(7)', 'relayOn(8)', 'relayOff(9)']
ol_status = ['unknown', 'online(1)', 'offline(2)']

class AKCPAirflowSensor(SnmpPlugin):
    relname = 'akcpairflowSensors'
    modname = 'ZenPacks.apple.AKCPsecurityProbe.AKCPAirflowSensor'

    snmpGetTableMaps = (
        GetTableMap(
            'AirflowSensorEntry', '1.3.6.1.4.1.3854.2.3.7.1', {
                '.2': 'SensorAirflowDescription',
                '.4': 'SensorAirflowValue',
                '.6': 'SensorAirflowStatus',
                '.8': 'SensorAirflowOnline',
                '.9': 'SensorAirflowLowCritical',
                '.10': 'SensorAirflowLowWarning',
                '.11': 'SensorAirflowHighWarning',
                '.12': 'SensorAirflowHighCritical',
                '.35': 'SensorAirflowPort',
                }
            ),
        )

    def process(self, device, results, log):
        airflow_sensors = results[1].get('AirflowSensorEntry', {})

        rm = self.relMap()
        for snmpindex, row in airflow_sensors.items():
            name = row.get('SensorAirflowDescription')
            if not name:
                log.warn('Skipping Sensor didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'SensorAirflowValue': row.get('SensorAirflowValue'),
                'SensorAirflowStatus': af_status[row.get('SensorAirflowStatus')],
                'SensorAirflowPort': row.get('SensorAirflowPort'),
                'SensorAirflowOnline': ol_status[row.get('SensorAirflowOnline')],
                'SensorAirflowHighWarning': row.get('SensorAirflowHighWarning'),
                'SensorAirflowHighCritical': row.get('SensorAirflowHighCritical'),
                'SensorAirflowLowWarning': row.get('SensorAirflowLowWarning'),
                'SensorAirflowLowCritical': row.get('SensorAirflowLowCritical'),
                }))

        return rm
