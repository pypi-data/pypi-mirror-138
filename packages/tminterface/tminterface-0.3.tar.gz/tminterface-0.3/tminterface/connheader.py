
from tminterface.structs import ConnectionHeaderStruct
from tminterface.message import ByteWriter
from enum import IntEnum

HEADER_SIZE = 12

class MessageFlags(IntEnum):
    NONE = 0x0
    CONNECTED = 0x1
    MESSAGE_READY = 0x2

class ConnectionHeader:
    def __init__(self, mfile):
        self.mfile = mfile

    @staticmethod
    def get_struct():
        data = ConnectionHeaderStruct()
        data.magic = 0
        data.size = HEADER_SIZE
        return data

    def send(self):
        data = ConnectionHeader.get_struct()
        data.flags = MessageFlags.CONNECTED | MessageFlags.MESSAGE_READY

        self.mfile.seek(0)
        self.mfile.write(data)

    def is_message_ready(self) -> bool:
        self.mfile.seek(0)
        data = ConnectionHeaderStruct(self.mfile.read(HEADER_SIZE))
        return (data.flags & MessageFlags.MESSAGE_READY) != 0

    def set_connected(self, connected: bool):
        data = ConnectionHeader.get_struct()
        if connected:
            data.flags = MessageFlags.CONNECTED
        
        self.mfile.seek(0)
        self.mfile.write(data)
