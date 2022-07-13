import base64
import struct

from ConstCode import *


class KeyBlock:
    __base = "%^$^GHsgjdsad24dffgjkdhw4"

    __key: bytes = None

    @staticmethod
    def new_block(sun_login_code: str = ""):
        if len(sun_login_code) > 31:
            raise Exception("invalid key")
        result = KeyBlock()
        temp = sun_login_code + result.__base
        size = struct.pack("<I", len(temp))
        for i in range(56 - len(temp)):
            temp += "\x00"
        result.__key = bytes(temp.encode() + size)
        return result

    def get_result(self) -> bytes:
        return self.__key


class Init(Base):
    __key: bytes = None

    def __init__(self, key_block: KeyBlock):
        self.__key = key_block.get_result()
        super().__init__()

    def on_create(self):
        obj = self._get_handle()
        obj.mem_map(self._code_ptr, align(len(init_code)))
        obj.mem_write(self._code_ptr, init_code)

        obj.mem_map(self._data_ptr, 0x2000)
        obj.mem_write(self._data_ptr, bytes(self.__key))
        obj.reg_write(unicorn.x86_const.UC_X86_REG_RCX, self._data_ptr)

    def get_result(self) -> bytes:
        return bytes(self._get_handle().mem_read(self._data_ptr + 60, 0x2000 - 60))


class Decrypt(Base):
    __save_ptr = 0x100000

    def __init__(self, encoded_data, box):
        self.__encoded_data = encoded_data
        self.__box = box
        super().__init__()

    def on_create(self):
        obj = self._get_handle()
        obj.mem_map(self._code_ptr, align(len(decrypt_code)))
        obj.mem_write(self._code_ptr, decrypt_code)

        obj.mem_map(self._data_ptr, 0x2000)
        obj.mem_write(self._data_ptr, self.__box)
        obj.reg_write(unicorn.x86_const.UC_X86_REG_RDX, self._data_ptr)

        obj.mem_map(self.__save_ptr, align(len(self.__encoded_data)))
        obj.mem_write(self.__save_ptr, self.__encoded_data)
        obj.reg_write(unicorn.x86_const.UC_X86_REG_R8, self.__save_ptr)
        obj.reg_write(unicorn.x86_const.UC_X86_REG_R9, int(len(self.__encoded_data) / 8))

    def get_result(self) -> bytes:
        return self._get_handle().mem_read(self.__save_ptr, len(self.__encoded_data))


