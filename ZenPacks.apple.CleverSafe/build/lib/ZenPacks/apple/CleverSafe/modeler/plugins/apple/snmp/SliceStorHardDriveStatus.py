from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class SliceStorHardDriveStatus(SnmpPlugin):
    relname = 'sliceStorHardDriveStatuss'
    modname = 'ZenPacks.apple.CleverSafe.SliceStorHardDriveStatus'

    snmpGetTableMaps = (
        GetTableMap(
            'HardDriveEntry', '1.3.6.1.4.1.28129.1.3.4.3.2.1', {
#            'HardDriveEntry', '1.3.6.1.4.1.5528.100.4.1.1.1', {
# please remove above line and uncomment above-above line before deployment
#                '.1': 'HardDriveIndex'
                '.2': 'HardDriveDevice',
                '.4': 'HardDriveModel',
                '.5': 'HardDriveSerialNum',
                '.6': 'HardDriveFWVersion',
                '.12': 'HardDriveDiskSize',
                '.10': 'HardDriveBay',
                '.13': 'HardDriveState'
                }
            ),
        )

    def process(self, device, results, log):
        temp_sensors = results[1].get('HardDriveEntry', {})

        rm = self.relMap()
        for snmpindex, row in temp_sensors.items():
            name = row.get('HardDriveDevice')
            if not name:
                log.warn('Skipping Harddrive didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'HardDriveModel': row.get('HardDriveModel'),
                'HardDriveSerialNum': row.get('HardDriveSerialNum'),
                'HardDriveFWVersion': row.get('HardDriveFWVersion'),
                'HardDriveDiskSize': row.get('HardDriveDiskSize'),
                'HardDriveBay': row.get('HardDriveBay'),
                'HardDriveState': row.get('HardDriveState')
                }))

        return rm
