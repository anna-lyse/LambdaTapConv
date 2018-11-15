from binascii import hexlify
from pyasn1.compat.dateandtime import strptime
from pyasn1.error import PyAsn1Error
from main.tap import Tap


class Extractor:
    @classmethod
    def extract(self, fullTAP):
        dataInterChange = fullTAP[0]
        callEventDetailsList = dataInterChange['transferBatch']['callEventDetails']
        values = "insert into tap" \
                 "(sender,recipient,fileCreationTimeStamp,localCurrencyCode,exchangeRate,gprsCallTimestamp,subscriber_pdpAddress,subscriber_imsi,subscriber_msisdn,apnNI,apnOI,gprsNetworkLocationArea, " \
                 "gprsNetworkLocationCellId,imei, gprsCall_volumeIncoming,gprsCall_volumeOutgoing,gprsCall_totalCharge,gprsCall_chargedUnits)\nvalues"

        for callEventDetail in callEventDetailsList:

            sender = str(dataInterChange['transferBatch']['batchControlInfo']['sender'])
            recipient = str(dataInterChange['transferBatch']['batchControlInfo']['recipient'])
            fileCreationTimeStamp = self.__createTimestamp(str(dataInterChange['transferBatch']['batchControlInfo']['fileCreationTimeStamp']['localTimeStamp']))
            localCurrencyCode = str(dataInterChange['transferBatch']['accountingInfo']['localCurrency'])
            numberOfDecimalPlaces = int(dataInterChange['transferBatch']['accountingInfo']['currencyConversionInfo'][0]['numberOfDecimalPlaces'])
            exchangerate = int(dataInterChange['transferBatch']['accountingInfo']['currencyConversionInfo'][0]['exchangeRate'])
            newExchangerate = self.__calculateExchangeRate(exchangerate, numberOfDecimalPlaces)
            gprsCallTimestamp = self.__createTimestamp(str(callEventDetail['gprsCall']['gprsBasicCallInformation']['callEventStartTimeStamp']['localTimeStamp']))
            try:
                subscriber_pdpAddress = str(callEventDetail['gprsCall']['gprsBasicCallInformation']['gprsChargeableSubscriber']['pdpAddress'])
            except PyAsn1Error:
                subscriber_pdpAddress = '0'
            subscriber_imsi = self.__encodeFromOctet(callEventDetail['gprsCall']['gprsBasicCallInformation']['gprsChargeableSubscriber']['chargeableSubscriber']['simChargeableSubscriber']['imsi'])
            try:
                subscriber_msisdn = self.__encodeFromOctet(callEventDetail['gprsCall']['gprsBasicCallInformation']['gprsChargeableSubscriber']['chargeableSubscriber']['simChargeableSubscriber']['msisdn'])
            except PyAsn1Error:
                subscriber_msisdn = '0'
            apnNI = str(callEventDetail['gprsCall']['gprsBasicCallInformation']['gprsDestination']['accessPointNameNI'])
            try:
                apnOI = str(callEventDetail['gprsCall']['gprsBasicCallInformation']['gprsDestination']['accessPointNameOI'])
            except PyAsn1Error:
                apnOI = '0'
            try:
                gprsNetworkLocationArea = str(callEventDetail['gprsCall']['gprsLocationInformation']['gprsNetworkLocation']['locationArea'])
            except PyAsn1Error:
                gprsNetworkLocationArea = '0'
            try:
                gprsNetworkLocationCellId = str(callEventDetail['gprsCall']['gprsLocationInformation']['gprsNetworkLocation']['cellId'])
            except PyAsn1Error:
                gprsNetworkLocationCellId = '0'
            imei = self.__encodeFromOctet(callEventDetail['gprsCall']['equipmentIdentifier']['imei'])
            gprsCall_volumeIncoming = str(callEventDetail['gprsCall']['gprsServiceUsed']['dataVolumeIncoming'])
            gprsCall_volumeOutgoing = str(callEventDetail['gprsCall']['gprsServiceUsed']['dataVolumeOutgoing'])
            gprsCall_totalCharge = str(callEventDetail['gprsCall']['gprsServiceUsed']['chargeInformationList'][0]['chargeDetailList'][0]['charge'])
            gprsCall_chargedUnits = str(callEventDetail['gprsCall']['gprsServiceUsed']['chargeInformationList'][0]['chargeDetailList'][0]['chargeableUnits'])

            tap = Tap(sender, recipient, fileCreationTimeStamp, localCurrencyCode, newExchangerate,
                      gprsCallTimestamp, subscriber_pdpAddress, subscriber_imsi, subscriber_msisdn, apnNI, apnOI, gprsNetworkLocationArea, gprsNetworkLocationCellId, imei, gprsCall_volumeIncoming,
                        gprsCall_volumeOutgoing, gprsCall_totalCharge, gprsCall_chargedUnits)

            values += tap.scvPrint() + '\n'
        return values


    @staticmethod
    def __encodeFromOctet(value):
        octetString =str(hexlify(str(value).encode()))
        encodedString = octetString.replace("c2", "").replace("f", "").replace("b", "")
        return encodedString

    @staticmethod
    def __createTimestamp(value):
        dateObject = strptime(value,'%Y%m%d%H%M%S')
        date =  dateObject.strftime('%Y-%m-%d %H:%M:%S')
        return str(date)

    @staticmethod
    def __calculateExchangeRate(exchangerate, numberOfDecimalPlaces):
        new = exchangerate / 10**numberOfDecimalPlaces
        return str(new)


