from pyasn1.codec.ber.decoder import decode as decoder
from main.extractor import Extractor
from main.tap0312_schema_class import DataInterChange
import sys
import gzip
import datetime
import boto3
# debug.setLogger(debug.Debug('all'))


class Main(object):
    def run(self):
        taps = readFile('tapfiles/167.gz')
        fullTAP = decoder(taps, asn1Spec=DataInterChange())
        value = Extractor.extract(fullTAP)
        writeFileToS3(value)


def readFile(filename):
    try:
        encoded_bytes = gzip.open(filename, "rb")
        taps = encoded_bytes.read()
        encoded_bytes.close()
        return taps
    except(FileNotFoundError, IOError):
        print('File not found, please verify that file path exists')
        sys.exit(1)
    finally:
        encoded_bytes.close()


def writeFileToS3(value):
        print(value)
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d-%H-%M')
        client = boto3.client('s3')
        byteValue = str.encode(value)
        s_out = gzip.compress(byteValue)
        client.put_object(Bucket='anna-tap-files', Key='tapfiles/' + date + '_' + 'outputfile.gz', Body=s_out)


if __name__ == '__main__':
    Main().run()
