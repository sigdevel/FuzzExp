package Monitoring::GLPlugin::SNMP::MibsAndOids::LIEBERTGPPDUMIB;
$Monitoring::GLPlugin::SNMP::MibsAndOids::origin->{'LIEBERT-GP-PDU-MIB'} = {
url => '',
name => 'LIEBERT-GP-PDU-MIB',
};
$Monitoring::GLPlugin::SNMP::MibsAndOids::mib_ids->{'LIEBERT-GP-PDU-MIB'} =
'1.3.6.1.4.1.476.1.42.3.8';
$Monitoring::GLPlugin::SNMP::MibsAndOids::mibs_and_oids->{'LIEBERT-GP-PDU-MIB'} = {
liebertGlobalProductsPduModule => '1.3.6.1.4.1.476.1.42.1.9.1',
lgpPduCluster => '1.3.6.1.4.1.476.1.42.3.8.10',
lgpPduGrpSysStatus => '1.3.6.1.4.1.476.1.42.3.8.10.5',
lgpPduGrpSysStatusDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduGrpSysStatus',
lgpPduTableCount => '1.3.6.1.4.1.476.1.42.3.8.19',
lgpPduTable => '1.3.6.1.4.1.476.1.42.3.8.20',
lgpPduEntry => '1.3.6.1.4.1.476.1.42.3.8.20.1',
lgpPduEntryIndex => '1.3.6.1.4.1.476.1.42.3.8.20.1.1',
lgpPduEntryId => '1.3.6.1.4.1.476.1.42.3.8.20.1.5',
lgpPduEntryUsrLabel => '1.3.6.1.4.1.476.1.42.3.8.20.1.10',
lgpPduEntrySysAssignLabel => '1.3.6.1.4.1.476.1.42.3.8.20.1.15',
lgpPduEntryPositionRelative => '1.3.6.1.4.1.476.1.42.3.8.20.1.20',
lgpPduEntrySysStatus => '1.3.6.1.4.1.476.1.42.3.8.20.1.25',
lgpPduEntrySysStatusDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduEntrySysStatus',
lgpPduEntryUsrTag1 => '1.3.6.1.4.1.476.1.42.3.8.20.1.35',
lgpPduEntryUsrTag2 => '1.3.6.1.4.1.476.1.42.3.8.20.1.40',
lgpPduEntrySerialNumber => '1.3.6.1.4.1.476.1.42.3.8.20.1.45',
lgpPduEntryRbCount => '1.3.6.1.4.1.476.1.42.3.8.20.1.50',
lgpPduPowerSource => '1.3.6.1.4.1.476.1.42.3.8.30',
lgpPduPsTableCount => '1.3.6.1.4.1.476.1.42.3.8.30.19',
lgpPduPsTable => '1.3.6.1.4.1.476.1.42.3.8.30.20',
lgpPduPsEntry => '1.3.6.1.4.1.476.1.42.3.8.30.20.1',
lgpPduPsEntryIndex => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.5',
lgpPduPsEntryId => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.10',
lgpPduPsEntrySysAssignLabel => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.15',
lgpPduPsEntryModel => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.20',
lgpPduPsEntryWiringType => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.25',
lgpPduPsEntryWiringTypeDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduPsEntryWiringType',
lgpPduPsEntryEpInputRated => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.30',
lgpPduPsEntryEcInputRated => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.35',
lgpPduPsEntryFreqRated => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.40',
lgpPduPsEntryEnergyAccum => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.50',
lgpPduPsEntrySerialNum => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.55',
lgpPduPsEntryFirmwareVersion => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.60',
lgpPduPsEntryPwrTotal => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.65',
lgpPduPsEntryEcNeutral => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.70',
lgpPduPsEntryEcNeutralThrshldOvrWarn => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.75',
lgpPduPsEntryEcNeutralThrshldOvrAlarm => '1.3.6.1.4.1.476.1.42.3.8.30.20.1.80',
lgpPduPsLineTable => '1.3.6.1.4.1.476.1.42.3.8.30.40',
lgpPduPsLineEntry => '1.3.6.1.4.1.476.1.42.3.8.30.40.1',
lgpPduPsLineEntryIndex => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.5',
lgpPduPsLineEntryId => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.10',
lgpPduPsLineEntryLine => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.15',
lgpPduPsLineEntryLineDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduPsLineEntryLine',
lgpPduPsLineEntryEpLNTenths => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.19',
lgpPduPsLineEntryEpLN => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.20',
lgpPduPsLineEntryEc => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.21',
lgpPduPsLineEntryEcHundredths => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.22',
lgpPduPsLineEntryEcThrshldUndrAlarm => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.35',
lgpPduPsLineEntryEcThrshldOvrWarn => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.36',
lgpPduPsLineEntryEcThrshldOvrAlarm => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.37',
lgpPduPsLineEntryEcAvailBeforeAlarm => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.38',
lgpPduPsLineEntryEcUsedBeforeAlarm => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.39',
lgpPduPsLineEntryEpLL => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.60',
lgpPduPsLineEntryEpLLTenths => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.61',
lgpPduPsLineEntryEcAvailBeforeAlarmHundredths => '1.3.6.1.4.1.476.1.42.3.8.30.40.1.62',
lgpPduReceptacleBranch => '1.3.6.1.4.1.476.1.42.3.8.40',
lgpPduRbTableCount => '1.3.6.1.4.1.476.1.42.3.8.40.19',
lgpPduRbTable => '1.3.6.1.4.1.476.1.42.3.8.40.20',
lgpPduRbEntry => '1.3.6.1.4.1.476.1.42.3.8.40.20.1',
lgpPduRbEntryIndex => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.1',
lgpPduRbEntryId => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.5',
lgpPduRbEntryUsrLabel => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.8',
lgpPduRbEntrySysAssignLabel => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.20',
lgpPduRbEntryPositionRelative => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.25',
lgpPduRbEntrySerialNum => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.30',
lgpPduRbEntryModel => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.35',
lgpPduRbEntryFirmwareVersion => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.40',
lgpPduRbEntryUsrTag1 => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.41',
lgpPduRbEntryUsrTag2 => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.42',
lgpPduRbEntryReceptacleType => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.45',
lgpPduRbEntryReceptacleTypeDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRbEntryReceptacleType',
lgpPduRbEntryCapabilities => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.50',
lgpPduRbEntryCapabilitiesDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRbEntryCapabilities',
lgpPduRbEntryLineSource => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.55',
lgpPduRbEntryLineSourceDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRbEntryLineSource',
lgpPduRbEntryRcpCount => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.60',
lgpPduRbEntryEpRated => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.70',
lgpPduRbEntryEcRated => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.75',
lgpPduRbEntryFreqRated => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.80',
lgpPduRbEntryEnergyAccum => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.85',
lgpPduRbEntryEpLNTenths => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.100',
lgpPduRbEntryPwr => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.115',
lgpPduRbEntryAp => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.120',
lgpPduRbEntryPf => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.125',
lgpPduRbEntryEcHundredths => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.130',
lgpPduRbEntryEcThrshldUndrAlm => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.135',
lgpPduRbEntryEcThrshldOvrWarn => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.140',
lgpPduRbEntryEcThrshldOvrAlm => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.145',
lgpPduRbEntryEcAvailBeforeAlarmHundredths => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.150',
lgpPduRbEntryEcUsedBeforeAlarm => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.160',
lgpPduRbEntryEpLLTenths => '1.3.6.1.4.1.476.1.42.3.8.40.20.1.170',
lgpPduRbLineTable => '1.3.6.1.4.1.476.1.42.3.8.40.40',
lgpPduRbLineEntry => '1.3.6.1.4.1.476.1.42.3.8.40.40.1',
lgpPduRbLineEntryIndex => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.1',
lgpPduRbLineEntryId => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.5',
lgpPduRbLineEntryLine => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.10',
lgpPduRbLineEntryLineDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRbLineEntryLine',
lgpPduRbLineEntryEpLNTenths => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.19',
lgpPduRbLineEntryEpLN => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.20',
lgpPduRbLineEntryEc => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.21',
lgpPduRbLineEntryPwr => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.22',
lgpPduRbLineEntryAp => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.23',
lgpPduRbLineEntryPf => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.24',
lgpPduRbLineEntryEcHundredths => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.25',
lgpPduRbLineEntryEcThrshldUndrAlm => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.35',
lgpPduRbLineEntryEcThrshldOvrWarn => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.36',
lgpPduRbLineEntryEcThrshldOvrAlm => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.37',
lgpPduRbLineEntryEcAvailBeforeAlarmHundredths => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.39',
lgpPduRbLineEntryEcAvailBeforeAlarm => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.40',
lgpPduRbLineEntryEcUsedBeforeAlarm => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.41',
lgpPduRbLineEntryEpLL => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.60',
lgpPduRbLineEntryEpLLTenths => '1.3.6.1.4.1.476.1.42.3.8.40.40.1.61',
lgpPduReceptacle => '1.3.6.1.4.1.476.1.42.3.8.50',
lgpPduRcpTableCount => '1.3.6.1.4.1.476.1.42.3.8.50.19',
lgpPduRcpTable => '1.3.6.1.4.1.476.1.42.3.8.50.20',
lgpPduRcpEntry => '1.3.6.1.4.1.476.1.42.3.8.50.20.1',
lgpPduRcpEntryIndex => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.1',
lgpPduRcpEntryId => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.5',
lgpPduRcpEntryUsrLabel => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.10',
lgpPduRcpEntryUsrTag1 => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.15',
lgpPduRcpEntryUsrTag2 => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.20',
lgpPduRcpEntrySysAssignLabel => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.25',
lgpPduRcpEntryPosition => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.30',
lgpPduRcpEntryType => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.40',
lgpPduRcpEntryTypeDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRcpEntryType',
lgpPduRcpEntryLineSource => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.45',
lgpPduRcpEntryLineSourceDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRcpEntryLineSource',
lgpPduRcpEntryCapabilities => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.50',
lgpPduRcpEntryCapabilitiesDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRcpEntryCapabilities',
lgpPduRcpEntryEp => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.55',
lgpPduRcpEntryEpTenths => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.56',
lgpPduRcpEntryEc => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.60',
lgpPduRcpEntryEcHundredths => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.61',
lgpPduRcpEntryPwrOut => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.65',
lgpPduRcpEntryApOut => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.70',
lgpPduRcpEntryPf => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.75',
lgpPduRcpEntryFreq => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.80',
lgpPduRcpEntryEnergyAccum => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.85',
lgpPduRcpEntryPwrOnDelay => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.90',
lgpPduRcpEntryPwrState => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.95',
lgpPduRcpEntryPwrStateDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRcpEntryPwrState',
lgpPduRcpEntryControl => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.100',
lgpPduRcpEntryControlDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRcpEntryControl',
lgpPduRcpEntryControlLock => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.105',
lgpPduRcpEntryControlLockDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRcpEntryControlLock',
lgpPduRcpEntryEcThrshldUnderAlarm => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.150',
lgpPduRcpEntryEcThrshldOverWarn => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.151',
lgpPduRcpEntryEcThrshldOverAlarm => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.152',
lgpPduRcpEntryEcAvailBeforeAlarmHundredths => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.159',
lgpPduRcpEntryEcAvailBeforeAlarm => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.160',
lgpPduRcpEntryEcUsedBeforeAlarm => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.161',
lgpPduRcpEntryEcCrestFactor => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.162',
lgpPduRcpEntryBlinkLED => '1.3.6.1.4.1.476.1.42.3.8.50.20.1.200',
lgpPduRcpEntryBlinkLEDDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduRcpEntryBlinkLED',
lgpPduAuxiliarySensors => '1.3.6.1.4.1.476.1.42.3.8.60',
lgpPduAuxSensorCount => '1.3.6.1.4.1.476.1.42.3.8.60.5',
lgpPduAuxSensorTable => '1.3.6.1.4.1.476.1.42.3.8.60.10',
lgpPduAuxSensorEntry => '1.3.6.1.4.1.476.1.42.3.8.60.10.1',
lgpPduAuxSensorIndex => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.1',
lgpPduAuxSensorMeasType => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.5',
lgpPduAuxSensorMeasTypeDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduAuxSensorMeasType',
lgpPduAuxSensorId => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.10',
lgpPduAuxSensorSysAssignLabel => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.15',
lgpPduAuxSensorPositionRelative => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.20',
lgpPduAuxSensorUsrLabel => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.25',
lgpPduAuxSensorUsrTag1 => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.30',
lgpPduAuxSensorUsrTag2 => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.35',
lgpPduAuxSensorTempSerialNum => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.40',
lgpPduAuxSensorHumSerialNum => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.45',
lgpPduAuxSensorTempMeasurementDegF => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.50',
lgpPduAuxSensorTempThrshldUndrAlmDegF => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.55',
lgpPduAuxSensorTempThrshldOvrAlmDegF => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.60',
lgpPduAuxSensorTempThrshldUndrWarnDegF => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.65',
lgpPduAuxSensorTempThrshldOvrWarnDegF => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.70',
lgpPduAuxSensorTempMeasurementDegC => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.75',
lgpPduAuxSensorTempThrshldUndrAlmDegC => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.80',
lgpPduAuxSensorTempThrshldOvrAlmDegC => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.85',
lgpPduAuxSensorTempThrshldUndrWarnDegC => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.90',
lgpPduAuxSensorTempThrshldOvrWarnDegC => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.95',
lgpPduAuxSensorHumMeasurement => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.100',
lgpPduAuxSensorHumThrshldUndrAlm => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.105',
lgpPduAuxSensorHumThrshldOvrAlm => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.110',
lgpPduAuxSensorHumThrshldUndrWarn => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.115',
lgpPduAuxSensorHumThrshldOvrWarn => '1.3.6.1.4.1.476.1.42.3.8.60.10.1.120',
lgpPduAuxMeasTable => '1.3.6.1.4.1.476.1.42.3.8.60.15',
lgpPduAuxMeasEntry => '1.3.6.1.4.1.476.1.42.3.8.60.15.1',
lgpPduAuxMeasSensorIndex => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.1',
lgpPduAuxMeasSensorMeasurementIndex => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.5',
lgpPduAuxMeasType => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.10',
lgpPduAuxMeasTypeDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduAuxMeasType',
lgpPduAuxMeasSensorSysAssignLabel => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.15',
lgpPduAuxMeasUsrLabel => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.20',
lgpPduAuxMeasUsrTag1 => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.25',
lgpPduAuxMeasUsrTag2 => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.30',
lgpPduAuxMeasSensorSerialNum => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.35',
lgpPduAuxMeasTempDegF => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.40',
lgpPduAuxMeasTempThrshldUndrAlmDegF => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.50',
lgpPduAuxMeasTempThrshldOvrAlmDegF => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.55',
lgpPduAuxMeasTempThrshldUndrWarnDegF => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.60',
lgpPduAuxMeasTempThrshldOvrWarnDegF => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.65',
lgpPduAuxMeasTempDegC => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.70',
lgpPduAuxMeasTempThrshldUndrAlmDegC => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.75',
lgpPduAuxMeasTempThrshldOvrAlmDegC => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.80',
lgpPduAuxMeasTempThrshldUndrWarnDegC => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.85',
lgpPduAuxMeasTempThrshldOvrWarnDegC => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.90',
lgpPduAuxMeasHum => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.95',
lgpPduAuxMeasHumThrshldUndrAlm => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.100',
lgpPduAuxMeasHumThrshldOvrAlm => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.105',
lgpPduAuxMeasHumThrshldUndrWarn => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.110',
lgpPduAuxMeasHumThrshldOvrWarn => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.115',
lgpPduAuxMeasDrClosureState => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.120',
lgpPduAuxMeasDrClosureStateDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduAuxMeasDrClosureState',
lgpPduAuxMeasDrClosureConfig => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.125',
lgpPduAuxMeasDrClosureConfigDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduAuxMeasDrClosureConfig',
lgpPduAuxMeasCntctClosureState => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.130',
lgpPduAuxMeasCntctClosureStateDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduAuxMeasCntctClosureState',
lgpPduAuxMeasCntctClosureConfig => '1.3.6.1.4.1.476.1.42.3.8.60.15.1.135',
lgpPduAuxMeasCntctClosureConfigDefinition => 'LIEBERT-GP-PDU-MIB::lgpPduAuxMeasCntctClosureConfig',
};
$Monitoring::GLPlugin::SNMP::MibsAndOids::definitions->{'LIEBERT-GP-PDU-MIB'} = {
lgpPduAuxMeasCntctClosureState => {
'0' => 'not-specified',
'1' => 'open',
'2' => 'closed',
},
lgpPduRcpEntryLineSource => {
'0' => 'not-specified',
'1' => 'line-1-N',
'2' => 'line-2-N',
'3' => 'line-3-N',
'4' => 'line-1-line-2',
'5' => 'line-2-line-3',
'6' => 'line-3-line-1',
'7' => 'unknown-line-neutral',
'8' => 'unknown-line-line',
},
lgpPduAuxMeasType => {
'0' => 'not-specified',
'1' => 'temperature',
'2' => 'humidity',
'3' => 'door-closure',
'4' => 'contact-closure',
},
lgpPduAuxSensorMeasType => {
'0' => 'not-specified',
'1' => 'temperature',
'2' => 'humidity',
'3' => 'temperature-and-humidity',
},
lgpPduAuxMeasCntctClosureConfig => {
'0' => 'disabled',
'1' => 'alarm-when-open',
'2' => 'alarm-when-closed',
},
lgpPduRcpEntryControl => {
'0' => 'off',
'1' => 'on',
'2' => 'cycle-power',
},
lgpPduRbLineEntryLine => {
'1' => 'phase1',
'2' => 'phase2',
'3' => 'phase3',
},
lgpPduPsLineEntryLine => {
'1' => 'phase1',
'2' => 'phase2',
'3' => 'phase3',
},
lgpPduAuxMeasDrClosureState => {
'0' => 'not-specified',
'1' => 'open',
'2' => 'closed',
},
lgpPduRcpEntryBlinkLED => {
'1' => 'noAction',
'2' => 'blinkLED',
},
lgpPduAuxMeasDrClosureConfig => {
'0' => 'disabled',
'1' => 'alarm-when-open',
},
lgpPduRcpEntryCapabilities => {
'0' => 'not-specified',
'1' => 'no-optional-capabilities',
'2' => 'measurement-only',
'3' => 'measurement-and-control',
'4' => 'control-only',
'5' => 'current-measurement-only',
'6' => 'current-measurement-and-control',
},
lgpPduRcpEntryType => {
'0' => 'not-specified',
'1' => 'nema-5-20R-20-Amp',
'2' => 'iec-C13-sheet-F-10-Amp',
'3' => 'iec-C19-sheet-J-16-Amp',
'7' => 'cee-7-type-E-schuko',
},
lgpPduRbEntryLineSource => {
'0' => 'not-specified',
'1' => 'line-1-neutral',
'2' => 'line-2-neutral',
'3' => 'line-3-neutral',
'4' => 'line-1-line-2',
'5' => 'line-2-line-3',
'6' => 'line-3-line-1',
'7' => 'line-1-line-2-and-line-1-neutral',
'8' => 'line-2-line-3-and-line-2-neutral',
'9' => 'line-3-line-1-and-line-3-neutral',
'10' => 'unknown-line-neutral',
'11' => 'unknown-line-line',
},
lgpPduRbEntryReceptacleType => {
'0' => 'not-specified',
'1' => 'nema-5-20R-20-Amp',
'2' => 'iec-C13-sheet-F-10-Amp',
'3' => 'iec-C19-sheet-J-16-Amp',
'4' => 'iec-C13-sheet-F-10-Amp-and-iec-C19-sheet-J-16-Amp',
'5' => 'nema-5-20R-20-Amp-and-iec-C13-sheet-F-10-Amp',
'6' => 'nema-5-20R-20-Amp-and-iec-C19-sheet-J-16-Amp',
'7' => 'cee-7-type-E-schuko',
},
lgpPduRcpEntryPwrState => {
'0' => 'unknown',
'1' => 'off',
'2' => 'on',
'3' => 'off-pending-on-delay',
},
lgpPduRbEntryCapabilities => {
'0' => 'not-specified',
'1' => 'no-optional-capabilities',
'2' => 'measurement-only',
'3' => 'measurement-and-control',
'4' => 'control-only',
'5' => 'current-measurement-only',
'6' => 'current-measurement-and-control',
},
lgpPduRcpEntryControlLock => {
'0' => 'unknown',
'1' => 'unlocked',
'2' => 'locked',
},
lgpPduPsEntryWiringType => {
'0' => 'not-specified',
'1' => 'single-phase-3-wire-L1-N-PE',
'2' => 'two-phase-3-wire-L1-L2-PE',
'3' => 'three-phase-4-wire-L1-L2-L3-PE',
'4' => 'three-phase-5-wire-L1-L2-L3-N-PE',
'5' => 'two-phase-4-wire-L1-L2-N-PE',
},
lgpPduGrpSysStatus => sub {
my $val = shift;
$val &= 0xffffffff;
$val = unpack("B32", pack("h", $val));
my @return = ();
my $bits = {
1 => 'normalOperation',
2 => 'startUp',
4 => 'unknownNoSupport',
8 => 'normalWithWarning',
16 => 'normalWithAlarm',
32 => 'abnormalOperation',
64 => 'unknownCommFailure',
};
foreach my $bit (sort { $a <=> $b } keys %{$bits}) {
if ($val & $bit) {
push(@return, $bits->{$bit});
}
}
return join(",", @return);
},
lgpPduEntrySysStatus => sub {
my $val = shift;
$val &= 0xffffffff;
$val = unpack("B32", pack("h", $val));
my @return = ();
my $bits = {
1 => 'normalOperation',
2 => 'startUp',
4 => 'unknownNoSupport',
8 => 'normalWithWarning',
16 => 'normalWithAlarm',
32 => 'abnormalOperation',
};
foreach my $bit (sort { $a <=> $b } keys %{$bits}) {
if ($val & $bit) {
push(@return, $bits->{$bit});
}
}
return join(",", @return);
},
};
