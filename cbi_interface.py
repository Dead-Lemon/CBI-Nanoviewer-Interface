"""
Protocal Spec

- Baud Rate      : 2400bps
- Character Size : 8bits
- Stop Bits      : 1
- Parity         : None

* Start Byte (unsigned char):
  - 0xAA: Start Byte

* Packet ID (unsigned char):
  - 0x10: Live Power Packet
  - 0x11: Accumulated Energy Packet
  - 0x12: NanoHub Firmware Version Packet

* Data (array of unsigned chars):
  - Live Power Packet (34 bytes):
   -- Mains Voltage [Volts] (unsigned integer 16bits)
   -- 16x Live Power [Watt] (unsigned integer 16bits)
  - Accumulated Energy Packet (64 bytes):
   -- 16x Energy Counters [Watt hour] (unsigned integer 32bits)
  - NanoHub Firmware Version Packet (1 byte):
   -- Version Number (unsigned char)

* Checksum (2x unsigned chars):
  - CRC1 (unsigned char)
  - CRC2 (unsigned char)

"""
import struct
import time

test1 = b'\xE6\x00'
serialDataBuffer1 = b'\x11\xE6\x00\xE0\x2E\x64\x00\xC8\x00\x2C\x01\x90\x01\xF4\x01\x58\x02\xBC\x02\x20\x03\x84\x03\xE8\x03\x4C\x04\xB0\x04\x14\x05\x78\x05\xDC\x05\xFB\xD5'
serialDataBuffer2 = b'\xAA\x11\xC0\xD4\x01\x00\0xE8\x03\x00\x00\xD0\x07\x00\x00\0xB8\x0B\x00\x00\0xA0\x0F\x00\x00\x88\x13\x00\x00\x70\x17\x00\x00\x58\x1B\x00\x00\x40\x1F\x00\x00\x28\x23\x00\x00\0x10\x27\x00\x00\0xF8\x2A\x00\x00\0xE0\x2E\x00\x00\xC8\x32\x00\x00\xB0\x36\x00\x00\x98\x3A\x00\x00\x21\x80'
serialDataBuffer3 = b'\xAA\x12\xFF\x00\x00'
#data sample to test with

livePowerBuffSize = int(34) #number of bytes
accEnergyBuffSize = int(64)
firmwareBuffSize = int(1)

packetStartID = b'\xAA'
testarray = bytearray(0)


def Checksum(data):
    crc1 = 0
    crc2 = 0
    for byte in data:
        crc1 += byte
        crc2 ^= crc1
    return (crc1 & 0xFF),(crc2 & 0xFF)

def testCRC(data):
    packetCRC1 = data[-2]
    packetCRC2 = data[-1]
    answer = Checksum(data[:-2])
    if ((packetCRC1 == answer[0]) & (packetCRC2 == answer[1])):
        return True
    else:
        return False


print(testCRC(serialDataBuffer1[1:]))






"""
# Start of Execution
try:
    ser = serial.Serial('/dev/ttyS0', baudrate=2400, timeout=1)  # open first serial port
except:
    print("COM PORT NOT OPEN!!!")


buffer = bytearray(0)

while True:
    buffer += ser.read(1)
    while decode_string(buffer):
        pass
"""