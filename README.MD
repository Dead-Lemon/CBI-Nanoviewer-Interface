# CBI Nanoviewer inFluxDB interface

inFluxDB Power logger using Serial decoding interface from [CBi Nanoview](http://nanoview.co.za/protocol.html)

## Requirements

- pySerial
- influxdb-client[ciso]

### Protocal Spec

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
