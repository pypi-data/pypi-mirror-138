import struct
from enum import Enum
# BYTE_LENGTH =1
# WORD_LENGTH =2
# LONG_LENGTH =4
# TIMESTAMP_LENGTH =8
# SINGLE_LENGTH =4

class SimpleType(Enum):
    byte ='B'
    word ='H'
    long ='L'
    # timestamp ='Q'
    single = 'f'
    double ='d'
    integer = 'i'
    uint64='Q'

BLANK =b'\x00'

def create_struct(endian,stype):
    return struct.Struct('%s%s' %(endian,stype.value))

class StructBuilder:
    def __init__(self,endian='>',encoding='utf8'):
        self.endian = endian
        self.encoding = encoding
        self._stype_structs={stype:create_struct(self.endian,stype) for stype in SimpleType}

    def read_stype(self,stype,buf,position):
        stype_struct = self._stype_structs[stype]
        ret =stype_struct.unpack_from(buf,position)
        return ret[0],stype_struct.size

    def write_stype(self,stype,v):
        stype_struct = self._stype_structs[stype]
        return stype_struct.pack(v)

    def read_byte(self,buf,position=0):
        return self.read_stype(SimpleType.byte,buf,position)

    def write_byte(self,v):
        return self.write_stype(SimpleType.byte,v)

    def read_word(self, buf, position=0):
        return self.read_stype(SimpleType.word, buf, position)

    def write_word(self, v):
        return self.write_stype(SimpleType.word, v)

    def read_long(self, buf, position=0):
        return self.read_stype(SimpleType.long, buf, position)

    def write_long(self, v):
        return self.write_stype(SimpleType.long, v)

    def read_uint64(self, buf, position=0):
        return self.read_stype(SimpleType.uint64, buf, position)

    def write_uint64(self, v):
        return self.write_stype(SimpleType.uint64, v)

    def read_timestamp(self, buf, position=0):
        return self.read_uint64(buf,position)
        # return self.read_stype(SimpleType.timestamp, buf, position)

    def write_timestamp(self, v):
        return self.write_uint64( v)

    def read_single(self, buf, position=0):
        return self.read_stype(SimpleType.single, buf, position)

    def write_single(self, v):
        return self.write_stype(SimpleType.single, v)

    def read_double(self, buf, position=0):
        return self.read_stype(SimpleType.double, buf, position)

    def write_double(self, v):
        return self.write_stype(SimpleType.double, v)

    def read_integer(self,buf,position =0):
        return self.read_stype(SimpleType.integer,buf,position)

    def write_integer(self,v):
        return self.write_stype(SimpleType.integer,v)

    def read_stype_string(self,stype,buf,position=0):
        length,stype_length = self.read_stype(stype,buf,position)
        data = buf[position+stype_length:position+stype_length+ length]
        return data.decode().strip(),stype_length + length

    def write_stype_string(self,stype,s):
        data = s.encode()
        buf =self.write_stype(stype,len(data))
        return buf + data

    def buf_fmt(self,fmt):
        return '%s%s' %(self.endian,fmt)

    def read_bytex(self,buf,length,position =0):
        buf = buf[position:position+length]
        assert len(buf)>= length
        ret =struct.unpack_from(self.buf_fmt('%dB' %(length)),buf,position)
        return list(ret),length

    def write_bytex(self,v,length):
        #done: check length
        v = v[:length]
        if len(v)<length:
            v += [0]* (length - len(v))
        return struct.pack(self.buf_fmt('%dB' % length),*v)

    def read_charx(self,buf,length,position=0):
        data =buf[position:position+ length]
        assert len(buf) >= length
        data =data.strip(BLANK)
        return data.decode(),length

    def write_charx(self,v,length):
        buf =v.encode()
        buf = buf[:length]
        if len(buf)<length:
            buf +=BLANK * (length - len(buf))
        return buf[:length]


    def read_bytestring(self,buf):
        return self.read_stype_string(SimpleType.byte,buf)

    def write_bytestring(self,v):
        return self.write_stype_string(SimpleType.byte,v)

    def read_wordstring(self,buf):
        return self.read_stype_string(SimpleType.word,buf)

    def write_wordstring(self,v):
        return self.write_stype_string(SimpleType.word,v)

    def read_byteboolean(self,buf):
        v,length =self.read_byte(buf)
        return bool(v),length

    def write_byteboolean(self,v):
        return self.write_byte(int(v))

# def create_struct(define,endian):
#     return struct.Struct('%s%s' % (endian,define) )
#
# class BufExt:
#     def __init__(self,endian ='>'):
#         self.endian = endian
#         self._byte = create_struct('B',endian)
#         self._word = create_struct('H',endian)
#         self._long = create_struct('L',endian)
#         self._timestamp = create_struct('Q',endian)
#         self._single = create_struct('f',endian)
#
#     def read_byte(self,buf,position =0):
#         assert len(buf)>= BYTE_LENGTH
#         ret = self._byte.unpack_from(buf,position)
#         return ret[0],BYTE_LENGTH
#
#     def write_byte(self,v):
#         assert v >=0 and v<=255
#         return self._byte.pack(v)
#
#     def read_word(self,buf,position =0):
#         assert len(buf)>=WORD_LENGTH
#         ret = self._word.unpack_from(buf,position)
#         return ret[0],WORD_LENGTH
#
#     def write_word(self,v):
#         assert v >=0 and v <=65535
#         return self._word.pack(v)
#
#     def read_long(self,buf,position =0):
#         assert len(buf)>=LONG_LENGTH
#         ret = self._long.unpack_from(buf,position)
#         return ret[0],LONG_LENGTH
#
#     def write_long(self,v):
#         return self._long.pack(v)
#
#     def read_timestamp(self,buf,position =0):
#         assert len(buf)>=TIMESTAMP_LENGTH
#         ret = self._timestamp.unpack_from(buf, position)
#         return ret[0], TIMESTAMP_LENGTH
#
#     def write_timestamp(self,v):
#         return self._timestamp.pack(v)
#
#     def buf_fmt(self,fmt):
#         return '%s%s' %(self.endian,fmt)
#
#     def bytex_fmt(self,length):
#         return '%s%dB' % (self.endian,length)
#
#     def read_single(self,buf,position):
#         ret = self._single.unpack_from(buf,position)
#         return ret[0],SINGLE_LENGTH
#
#     def write_single(self,v):
#         return self._single.pack(v)
#
#     def read_bytex(self,buf,length,position=0):
#         ret = struct.unpack_from(self.bytex_fmt(length), buf,position)
#         return list(ret),length * BYTE_LENGTH
#
#     def write_bytex(self,v,length):
#         if v is None:
#             v = [0] * length
#         return struct.pack(self.bytex_fmt(length),*v)
#
#     def read_variant_data(self,buf,length,position=0):
#         return buf[position :position+length],length
#
#     def write_variant_data(self,data,length):
#         return data
#
#     def write_variant_string(self,s,length=None):
#         data = s.encode()
#         if length is None:
#             length = len(data)
#         return self.write_variant_data(data,length)
#
#
#     def read_variant_string(self,buf,length,position =0):
#         data,data_length = self.read_variant_data(buf,length,position)
#         return data.decode().strip(),data_length
#
#     def read_bytestring(self,buf,position=0):
#         length,offset =self.read_byte(buf,position)
#         position += offset
#         s,s_length = self.read_variant_string(buf,length,position)
#         return s ,offset+ s_length
#
#     def write_bytestring(self,s):
#         buf =self.write_byte(len(s))
#         buf +=self.write_variant_string(s,len(s))
#         return buf




if __name__ == '__main__':
    buidler = StructBuilder('>')


    # class Header:
    #     def __init__(self):
    #         self.vtid =[]
    #         self.len =0
    #
    #     @classmethod
    #     def read(cls,buf):
    #         self = cls()
    #         position =0
    #         self.vtid,offset = buidler.read_bytex(buf,4)
    #         position +=offset
    #         self.len,offset = buidler.read_byte(buf[position:])
    #         position +=offset
    #         return self,position
    #
    # class Command:
    #     def __init__(self):
    #         self.header =Header()
    #         self.len =0
    #
    #     @classmethod
    #     def read(cls,buf):
    #         self =cls()
    #         position =0
    #         self.header,offset =Header.read(buf)
    #         position += offset
    #         self.len = buidler.read_byte(buf[position:])
    #         position += offset
    #         return self,position
    #
    #     def write(self):
    #         buf =b''
    #         buf += self.header.write()
    #         buf += buidler.write_byte(self.len)
    #         return buf



    # b = BufExt()
    # buf =b.write_bytex([1,2,3,4],4)
    # print(buf)
    # v,length =b.read_bytex(buf,4)
    # print(v)
    #
    # buf.decode()
    pass

