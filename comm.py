'''Retrieve data from Chiller'''
from pylogix import PLC
from pylogix import comm as comm_err

class PLCCommunication:
    def __init__(self, plc_ip):
        self.plc = PLC()
        self.plc.IPAddress = plc_ip

    def _establish_connection(self):
        try:
            self.plc.open()
            return True
        except comm_err.CommError:
            return False

    def read_tags(self, tags):
        if not self._establish_connection():
            return [None] * len(tags)
        try:
            return self.plc.Read(tags)
        except comm_err.CommError:
            return [None] * len(tags)

    def read_tags_with_datatypes(self, tags):
        if not self._establish_connection():
            return [{'name': tag, 'value': None, 'datatype': None} for tag in tags]
        try:
            data = self.plc.Read(tags, datatype=True)
            return [{'name': tag, 'value': value, 'datatype': datatype} for tag, value, datatype in data]
        except comm_err.CommError:
            return [{'name': tag, 'value': None, 'datatype': None} for tag in tags]

