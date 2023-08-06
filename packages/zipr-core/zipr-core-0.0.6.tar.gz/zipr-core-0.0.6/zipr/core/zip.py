from dataclasses import dataclass, fields
import inspect
import struct

@dataclass(frozen=True)
class EOCD:
    disk_index: int
    cd_start_disk: int
    cd_records_on_disk: int
    cd_records_total: int
    cd_size: int
    cd_offset: int
    comment_len: int
    comment: str

    @classmethod
    def from_bytes(cls, b: bytes):
        def e(start: int, end: int):
            return int.from_bytes(b[start:end], byteorder='little')

        # Find signature...start from smallest possible EOCD (no comment) to largest
        for i in range(len(b)-22, -1, -1):
            if b[i:i+4] == b'PK\x05\x06':
                fixed_data = struct.unpack(r'<4H2LH', b[i+4:i+22])
                comment_last_byte = i+22+fixed_data[6]
                comment = '' if len(b) < comment_last_byte else b[i+22:comment_last_byte].decode()
                return cls(**dict(zip(map(lambda field: field.name, fields(EOCD)), fixed_data + (comment,))))
        return None

    def to_bytes(self) -> bytes:
        def d(value: int, size: int) -> bytes:
            return int.to_bytes(value, length=size, byteorder='little')

        return b'PK\x05\x06' \
            + d(self.disk_index, 2) \
            + d(self.cd_start_disk, 2) \
            + d(self.cd_records_on_disk, 2) \
            + d(self.cd_records_total, 2) \
            + d(self.cd_size, 4) \
            + d(self.cd_offset, 4) \
            + d(self.comment_len, 2) \
            + self.comment.encode()

@dataclass(frozen=True)
class CDFileHeader:
    made_by_version: int
    min_version_needed: int
    bit_flags: bytes
    compression_method: int
    last_mod_time: int
    last_mod_date: int
    uncompressed_crc: bytes
    compressed_size: int
    uncompressed_size: int
    filename_len: int
    extra_field_len: int
    file_comment_len: int
    disk_of_file_start: int
    internal_file_attr: bytes
    external_file_attr: bytes
    file_header_offset: int
    filename: str
    extra_field: str
    comment: str

    @classmethod
    def from_bytes(cls, b: bytes):
        # Find signature
        for i in range(0, len(b) - 4):
            if b[i:i+4] == b'PK\x01\x02':
                fixed_data = struct.unpack(r'<6H4s2L4H2s4sL', b[i+4:i+46])
                variable_length = fixed_data[9] + fixed_data[10] + fixed_data[11]
                variable_data = struct.unpack(
                    f"{fixed_data[9]}s{fixed_data[10]}s{fixed_data[11]}s",
                    b[i+46:i+46+variable_length],
                )
                payload = fixed_data + tuple(map(bytes.decode, variable_data))
                return cls(**dict(zip(map(lambda field: field.name, fields(CDFileHeader)), payload)))
        return None

    @classmethod
    def gen_from_bytes(cls, b: bytes):
        start_byte = 0
        while start_byte < len(b):
            signature = b[start_byte:start_byte+4]
            if signature == b'PK\x05\x06': # Found EOCD
                break
            elif signature == b'PK\x01\x02': # Found CDFileHeader
                cd_meta = cls.from_bytes(b[start_byte:])
                if cd_meta:
                    yield cd_meta
                    start_byte += 46+cd_meta.filename_len+cd_meta.file_comment_len+cd_meta.extra_field_len
                else:
                    start_byte += 1
            else:
                start_byte += 1

    def to_bytes(self) -> bytes:
        def d(value: int, size: int) -> bytes:
            return int.to_bytes(value, length=size, byteorder='little')

        return b'PK\x01\x02' \
            + d(self.made_by_version, 2) \
            + d(self.min_version_needed, 2) \
            + self.bit_flags \
            + d(self.compression_method, 2) \
            + d(self.last_mod_time, 2) \
            + d(self.last_mod_date, 2) \
            + self.uncompressed_crc \
            + d(self.compressed_size, 4) \
            + d(self.uncompressed_size, 4) \
            + d(self.filename_len, 2) \
            + d(self.extra_field_len, 2) \
            + d(self.file_comment_len, 2) \
            + d(self.disk_of_file_start, 2) \
            + self.internal_file_attr \
            + self.external_file_attr \
            + d(self.file_header_offset, 4) \
            + self.filename.encode() \
            + self.extra_field.encode() \
            + self.comment.encode()

@dataclass(frozen=True)
class FileHeader:
    min_version_needed: int
    bit_flags: bytes
    compression_method: int
    last_mod_time: int
    last_mod_date: int
    uncompressed_crc: bytes
    compressed_size: int
    uncompressed_size: int
    filename_len: int
    extra_field_len: int
    filename: str
    extra_field: str

    @classmethod
    def from_bytes(cls, b: bytes):
        def e(start: int, end: int):
            return int.from_bytes(b[start:end], byteorder='little')

        # Find signature
        for i in range(0, len(b) - 4):
            if b[i:i+4] == b'PK\x03\x04':
                fixed_data = struct.unpack(r'<5H3L2H', b[i+4:i:30])
                variable_length = fixed_data[8] + fixed_data[9]
                variable_data = struct.unpack(
                    f"{fixed_data[8]}s{fixed_data[9]}s",
                    b[i+30:i+30+variable_length],
                )
                payload = fixed_data + tuple(map(bytes.decode, variable_data))
                return cls(**dict(zip(map(lambda field: field.name, fields(FileHeader)), payload)))
        return None

    @classmethod
    def from_central_directory(cls, cd_meta: CDFileHeader):
        return cls(**{
            i: cd_meta.__getattribute__(i) for i in map(lambda field: field.name, fields(cd_meta))
            if i in inspect.signature(cls).parameters
        })

    def to_bytes(self) -> bytes:
        def d(value: int, size: int) -> bytes:
            return int.to_bytes(value, length=size, byteorder='little')

        return b'PK\x03\x04' \
            + d(self.min_version_needed, 2) \
            + self.bit_flags \
            + d(self.compression_method, 2) \
            + d(self.last_mod_time, 2) \
            + d(self.last_mod_date, 2) \
            + self.uncompressed_crc \
            + d(self.compressed_size, 4) \
            + d(self.uncompressed_size, 4) \
            + d(self.filename_len, 2) \
            + d(self.extra_field_len, 2) \
            + self.filename.encode() \
            + self.extra_field.encode()
