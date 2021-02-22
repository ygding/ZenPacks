from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class SliceStorFanStatus(SnmpPlugin):
    relname = 'sliceStorFanStatuss'
    modname = 'ZenPacks.apple.CleverSafe.SliceStorFanStatus'

    snmpGetTableMaps = (
        GetTableMap(
            'FanSpeedEntry', '1.3.6.1.4.1.28129.1.3.4.5.2.1', {
#            'HardDriveEntry', '1.3.6.1.4.1.5528.100.4.1.1.1', {
# please remove above line and uncomment above-above line before deployment
                '.1': 'FanSpeedIndex',
                '.3': 'FanSpeedMin',
                '.4': 'FanSpeedMax'
                }
            ),
        )

    def process(self, device, results, log):
        temp_sensors = results[1].get('FanSpeedEntry', {})

        rm = self.relMap()
        for snmpindex, row in temp_sensors.items():
            name = row.get('FanSpeedIndex')
            if not name:
                log.warn('Skipping Fan didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'FanSpeedMin': row.get('FanSpeedMin'),
                'FanSpeedMax': row.get('FanSpeedMax'),
                }))

        return rm
