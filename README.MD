# CBI Nanoviewer inFluxDB interface

Reads and decodes data from [CBi Nanoview](http://nanoview.co.za) and logs data to inFluxDB

### Electrical connection

- Pin 1 (**Black**) - Ground
- Pin 4 (**white**) - Tx

### Requirements
#### Python3
- pySerial
- influxdb-client[ciso]

Install with the following comand
```
pip install -r requirements.txt
```
##### InfluxDB v2
- Initilised DB to be able to create tokens and such


### Protocol Spec for Nanoview Serial Interface

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
   - Mains Voltage [Volts] (unsigned integer 16bits)
   - 16x Live Power [Watt] (unsigned integer 16bits)
  - Accumulated Energy Packet (64 bytes):
   - 16x Energy Counters [Watt hour] (unsigned integer 32bits)
  - NanoHub Firmware Version Packet (1 byte):
   - Version Number (unsigned char)

* Checksum (2x unsigned chars):
  - CRC1 (unsigned char)
  - CRC2 (unsigned char)
