# sub — Hex Edition

**File:** `sub.hex` (Intel HEX format)  
**Decoder:** `sub_decoder.py`

The `sub.hex` file encodes the SUB banner as raw bytes in Intel HEX format — the same format used to flash firmware to microcontrollers (AVR, STM32, ESP32, etc.).

## Decode & Print Banner

```bash
python3 src/hex/sub_decoder.py
```

## Flash to Microcontroller (AVR example)

```bash
# Flash via avrdude to an Arduino/AVR board
avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 -U flash:w:sub.hex:i
```

## Intel HEX Format

Each line: `:LLAAAATT[DD...]CC`

| Field | Meaning |
|---|---|
| `LL` | Byte count |
| `AAAA` | Address |
| `TT` | Record type (`00`=data, `01`=EOF) |
| `DD` | Data bytes |
| `CC` | Checksum |
