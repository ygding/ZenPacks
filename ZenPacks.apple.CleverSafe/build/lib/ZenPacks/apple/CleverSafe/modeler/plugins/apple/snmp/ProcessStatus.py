from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class ProcessStatus(SnmpPlugin):
    relname = 'processStatuss'
    modname = 'ZenPacks.apple.CleverSafe.ProcessStatus'

    snmpGetTableMaps = (
        GetTableMap(
            'ProcessEntry', '1.3.6.1.4.1.28129.1.3.4.10.2.1', {
#            'HardDriveEntry', '1.3.6.1.4.1.5528.100.4.1.1.1', {
# please remove above line and uncomment above-above line before deployment
#                '.1': 'ProcessIndex',
                '.2': 'ProcessName',
                '.3': 'ProcessOnlineStatus'
                }
            ),
        )

    def process(self, device, results, log):
        temp_sensors = results[1].get('ProcessEntry', {})

        rm = self.relMap()
        for snmpindex, row in temp_sensors.items():
            name = row.get('ProcessName')
            if not name:
                log.warn('Skipping Process didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'ProcessOnlineStatus': row.get('ProcessOnlineStatus'),
                }))

        return rm
