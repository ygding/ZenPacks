from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class AccesserVaultStatus(SnmpPlugin):
    relname = 'accesserVaultStatuss'
    modname = 'ZenPacks.apple.CleverSafe.AccesserVaultStatus'

    snmpGetTableMaps = (
        GetTableMap(
            'AccVault', '1.3.6.1.4.1.28129.1.3.4.11.2.1', {
#            'HardDriveEntry', '1.3.6.1.4.1.5528.100.4.1.1.1', {
# please remove above line and uncomment above-above line before deployment
                '.1': 'AccVaultIndex',
                '.2': 'AccVaultUUID',
                '.3': 'InternalNetworkDataIn',
                '.4': 'InternalNetworkDataOut',
                '.5': 'ExternalNetworkDataIn',
                '.6': 'ExternalNetworkDataOut',
                }
            ),
        )

    def process(self, device, results, log):
        temp_sensors = results[1].get('AccVault', {})

        rm = self.relMap()
        for snmpindex, row in temp_sensors.items():
            name = row.get('AccVaultIndex')
            if not name:
                log.warn('Skipping Valut didnot exist')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
#                'title': name,
                'snmpindex': snmpindex.strip('.'),
                'AccVaultUUID': row.get('AccVaultUUID'),
                'InternalNetworkDataIn': row.get('InternalNetworkDataIn'),
                'InternalNetworkDataOut': row.get('InternalNetworkDataOut'),
                'ExternalNetworkDataIn': row.get('ExternalNetworkDataIn'),
                'ExternalNetworkDataOut': row.get('ExternalNetworkDataOut'),
                }))

        return rm
