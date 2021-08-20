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
import serial

test1 = b'\xE6\x00'
serialDataBuffer1 = b'\xAA\x10\xE6\x00\xE0\x2E\x64\x00\xC8\x00\x2C\x01\x90\x01\xF4\x01\x58\x02\xBC\x02\x20\x03\x84\x03\xE8\x03\x4C\x04\xB0\x04\x14\x05\x78\x05\xDC\x05\xFB\xD5'
serialDataBuffer2 = b'\xAA\x11\xC0\xD4\x01\x00\xE8\x03\x00\x00\xD0\x07\x00\x00\xB8\x0B\x00\x00\xA0\x0F\x00\x00\x88\x13\x00\x00\x70\x17\x00\x00\x58\x1B\x00\x00\x40\x1F\x00\x00\x28\x23\x00\x00\x10\x27\x00\x00\xF8\x2A\x00\x00\xE0\x2E\x00\x00\xC8\x32\x00\x00\xB0\x36\x00\x00\x98\x3A\x00\x00\x21\x80'
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

def checkID(data):
    switch={
    b'\x10':livePowerBuffSize,
    b'\x11':accEnergyBuffSize,
    b'\x12':firmwareBuffSize
    }
    return switch.get(data, 'null')

def processLivePower(data):
    newData = struct.unpack('<' + 'H'*int(livePowerBuffSize/2), data)
    print(newData)
    return newData

def processAccEnergy(data):
    newData = struct.unpack('<' + 'L'*int(accEnergyBuffSize/4), data)
    print(newData)
    return newData

def processFirmware(data):
    print(data)
    return


try:
    cbiSerial = serial.Serial('/dev/ttyUSB0', baudrate=2400, timeout=0.5)  # open first serial port
    cbiSerial.write(test1)
    cbiSerial.write(serialDataBuffer1)
    cbiSerial.write(serialDataBuffer2)
except:
    print("Unable to open /dev/ttyUSB0")
    quit()


buffer = bytearray(0)

while True:
    if (cbiSerial.inWaiting()):
        if (cbiSerial.read()==packetStartID): #check if first byte in serial buffer is the start ID, will continue to loop until the buffer is empty or detects 0xAA startID
            ID = cbiSerial.read() #reads the next byte in buffer, expected to be the ID
            print(ID)
            packetSize = checkID(ID)  #get the packet size for the correspoding ID
            if (packetSize == 'null'): #check if the extracted ID is valid
                print("invalid packet ID")
                cbiSerial.flush()
                pass
            print(packetSize)
            buffer = cbiSerial.read(packetSize+2) #reads the exact buffer size for packet type and CRC from serial
            print(buffer)
            if (testCRC(buffer)):
                data = buffer[:-2] #remove crc data before passing on for value conversion
                processPacket = {
                    b'\x10':processLivePower,
                    b'\x11':processAccEnergy,
                    b'\x12':processFirmware
                    }
                processPacket[ID](data)
                print("done")
            else:
                print("CRC check failed")
                cbiSerial.flush()
                pass
    else:
        time.sleep(1)
