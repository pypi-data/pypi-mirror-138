import struct
from tminterface.eventbuffer import Event
from enum import IntEnum, auto


class MessageType(IntEnum):
    S_RESPONSE = auto()
    S_ON_REGISTERED = auto()
    S_SHUTDOWN = auto()
    S_ON_RUN_STEP = auto()
    S_ON_SIM_BEGIN = auto()
    S_ON_SIM_STEP = auto()
    S_ON_SIM_END = auto()
    S_ON_CHECKPOINT_COUNT_CHANGED = auto()
    S_ON_LAPS_COUNT_CHANGED = auto()
    S_ON_CUSTOM_COMMAND = auto()
    S_ON_BRUTEFORCE_EVALUATE = auto()
    C_REGISTER = auto()
    C_DEREGISTER = auto()
    C_PROCESSED_CALL = auto()
    C_SET_INPUT_STATES = auto()
    C_RESPAWN = auto()
    C_GIVE_UP = auto()
    C_HORN = auto()
    C_SIM_REWIND_TO_STATE = auto()
    C_SIM_GET_STATE = auto()
    C_SIM_GET_EVENT_BUFFER = auto()
    C_GET_CONTEXT_MODE = auto()
    C_SIM_SET_EVENT_BUFFER = auto()
    C_SIM_SET_TIME_LIMIT = auto()
    C_GET_CHECKPOINT_STATE = auto()
    C_SET_CHECKPOINT_STATE = auto()
    C_SET_GAME_SPEED = auto()
    C_EXECUTE_COMMAND = auto()
    C_SET_EXECUTE_COMMANDS = auto()
    C_SET_TIMEOUT = auto()
    C_REMOVE_STATE_VALIDATION = auto()
    C_PREVENT_SIMULATION_FINISH = auto()
    C_REGISTER_CUSTOM_COMMAND = auto()
    C_LOG = auto()
    ANY = auto()


class ByteWriter(object):
    def __init__(self):
        self.data = bytearray()

    def write_string(self, s: str):
        self.data.extend(s.encode('utf-8'))

    def write_event(self, event: Event):
        self.write_uint32(event.time)
        self.write_int32(event.data)

    def write_uint8(self, n):
        self.data.extend(struct.pack('B', n))

    def write_int16(self, n: int):
        self.data.extend(struct.pack('h', n))

    def write_uint16(self, n: int):
        self.data.extend(struct.pack('H', n))

    def write_int32(self, n: int):
        self.data.extend(struct.pack('i', n))

    def write_uint32(self, n: int):
        self.data.extend(struct.pack('I', n))

    def write_double(self, n: float):
        self.data.extend(struct.pack('d', n))

    def write_buffer(self, buffer: bytearray):
        self.data.extend(buffer)

    def write_zeros(self, n_bytes):
        self.data.extend(bytearray(n_bytes))

    def write_int(self, n, size):
        if size == 1:
            self.write_uint8(n)
        elif size == 2:
            if n < 0:
                self.write_int16(n)
            else:
                self.write_uint16(n)
        elif size == 4:
            if n == 0xffffffff:
                self.write_uint32(n)
            else:
                self.write_int32(n)

class Message(object):
    """
    The Message class represents a binary buffer that contains useful methods to construct
    a message to send to the server. A message additionally contains its type, whether it is
    a response to a server call, or a normal client call. It also contains an error code,
    if there was any failure writing the message.

    Args:
        _type (int): the message type
        error_code (int): the error code of the message, 0 if none

    Attributes:
        _type (int): the message type
        error_code (int): the error code of the message, 0 if none
        data (bytearray): the binary data
    """
    def __init__(self, _type: int, error_code=0):
        self._type = _type
        self.error_code = error_code
        self.body = ByteWriter()

    def to_data(self) -> bytearray:
        return bytearray(struct.pack('i', self._type)) + bytearray(struct.pack('i', self.error_code)) + self.body.data

    def __len__(self):
        return 8 + len(self.data)
