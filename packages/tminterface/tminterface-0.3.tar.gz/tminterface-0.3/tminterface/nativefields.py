from abc import ABC, abstractmethod
import struct
import numpy as np

class StructBase(type):
    def __new__(cls, name, bases, attrs):
        for key, field in attrs.copy().items():
            if key.startswith('_'):
                continue

            attrs[key] = property(field._getvalue, field._setvalue)

        return super(StructBase, cls).__new__(cls, name, bases, attrs)


class NativeField(ABC):
    @abstractmethod
    def _getvalue(self, native_struct):
        pass

    @abstractmethod
    def _setvalue(self, native_struct, value):
        pass


class NativeStruct(bytearray, metaclass=StructBase):
    def __init__(self, data: bytearray = None, master_offset=0, **kwargs):
        if data:
            self[:] = data
        self.master_offset = master_offset

    def _calc_offset(self, native_field):
        return self.master_offset + native_field.offset


class StructField(NativeField):
    def __init__(self, offset: int, struct_type: type):
        self.offset = offset
        self.struct_type = struct_type

    def _getvalue(self, native_struct: NativeStruct):
        inner = self.struct_type(native_struct, master_offset=self.offset)
        return inner

    def _setvalue(self, native_struct: NativeStruct, value: int):
        return super()._setvalue(native_struct, value)


class SimpleField(NativeField):
    def __init__(self, format: str, offset: int, **kwargs):
        self.format = format
        self.offset = offset
        self.size = struct.calcsize(format)

    def _getvalue(self, native_struct: NativeStruct):
        offset = native_struct._calc_offset(self)
        if offset + self.size > len(native_struct.data):
            raise Exception('Failed to get value: field is out of bounds')

        return struct.unpack(self.format, native_struct[offset:self.offset + 4])[0]

    def _setvalue(self, native_struct: NativeStruct, value):
        offset = native_struct._calc_offset(self)
        if offset + self.size > len(native_struct):
            raise Exception('Failed to set value: field is out of bounds')

        native_struct[offset:offset + 4] = struct.pack(self.format, value)


class IntegerField(SimpleField):
    def __init__(self, offset: int, signed=True):
        super().__init__('i' if signed else 'I', offset=offset)


class FloatField(SimpleField):
    def __init__(self, offset: int):
        super().__init__('f', offset=offset)


class BooleanField(IntegerField):
    def __init__(self, offset: int):
        super().__init__(offset=offset, signed=False)

    def _getvalue(self, native_struct: NativeStruct):
        return bool(super()._getvalue(native_struct))

    def _setvalue(self, native_struct: NativeStruct, value):
        return super()._setvalue(native_struct, int(value))


class MatrixField(NativeField):
    def __init__(self, offset: int, shape: tuple, elem_type_format: str) -> None:
        self.offset = offset
        self.shape = shape[:]
        self.elem_type_format = elem_type_format
        self.elem_size = struct.calcsize(self.elem_type_format)

    def _getvalue(self, native_struct: NativeStruct):
        begin_offset = native_struct._calc_offset(self)
        arr = np.zeros(shape=self.shape)
        if len(self.shape) == 2:
            for row in range(self.shape[0]):
                for col in range(self.shape[1]):
                    offset = begin_offset + (row * self.shape[1] + col) * self.elem_size
                    arr[row, col] = struct.unpack(self.elem_type_format, native_struct[offset:offset+self.elem_size])[0]
        else:
            for elem in range(self.shape[0]):
                offset = begin_offset + elem * self.elem_size
                arr[elem] = struct.unpack(self.elem_type_format, native_struct[offset:offset+self.elem_size])[0]

        return arr

    def _setvalue(self, native_struct: NativeStruct, value):
        pass