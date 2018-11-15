class Tap:
    def __init__(self,
                 sender, recipient, fileCreationTimeStamp,
                 localCurrencyCode, exchangeRate,
                 gprsCallTimestamp, subscriber_pdpAddress, subscriber_imsi,
                 subscriber_msisdn, apnNI, apnOI, gprsNetworkLocationArea, gprsNetworkLocationCellId,
                 imei, gprsCall_volumeIncoming, gprsCall_volumeOutgoing, gprsCall_totalCharge,
                 gprsCall_chargedUnits):
        self.sender = sender
        self.recipient = recipient
        self.fileCreationTimeStamp = fileCreationTimeStamp
        self.localCurrencyCode = localCurrencyCode
        self.exchangeRate = exchangeRate
        self.gprsCallTimestamp = gprsCallTimestamp
        self.subscriber_pdpAddress = subscriber_pdpAddress
        self.subscriber_imsi = subscriber_imsi
        self.subscriber_msisdn = subscriber_msisdn
        self.apnNI = apnNI
        self.apnOI = apnOI
        self.gprsNetworkLocationArea = gprsNetworkLocationArea
        self.gprsNetworkLocationCellId = gprsNetworkLocationCellId
        self.imei = imei
        self.gprsCall_volumeIncoming = gprsCall_volumeIncoming
        self.gprsCall_volumeOutgoing = gprsCall_volumeOutgoing
        self.gprsCall_totalCharge = gprsCall_totalCharge
        self.gprsCall_chargedUnits = gprsCall_chargedUnits

    def scvPrint(self):
        return str('(''\'' + self.sender + '\',' +
                   '\'' + self.recipient + '\',' +
                   '\'' + self.fileCreationTimeStamp + '\',' +
                   '\'' + self.localCurrencyCode + '\',' +
                   self.exchangeRate + ',' +
                   '\'' + self.gprsCallTimestamp + '\',' +
                   '\'' + self.subscriber_pdpAddress + '\',' +
                   self.subscriber_imsi + ',' +
                   self.subscriber_msisdn + ',' +
                   '\'' + self.apnNI + '\',' +
                   '\'' + self.apnOI + '\',' +
                   self.gprsNetworkLocationArea + ',' +
                   self.gprsNetworkLocationCellId + ',' +
                   self.imei + ',' +
                   self.gprsCall_volumeIncoming + ',' +
                   self.gprsCall_volumeOutgoing + ',' +
                   self.gprsCall_totalCharge + ',' +
                   self.gprsCall_chargedUnits + '),'
                   )
