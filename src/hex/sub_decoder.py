#!/usr/bin/env python3
"""
sub hex decoder - Decodes sub.hex Intel HEX records and prints the banner.
Author: Subhobhai (subhobhai943)
GitHub: https://github.com/subhobhai943
Usage: python3 sub_decoder.py
"""

def parse_intel_hex(filepath):
    data = bytearray()
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line.startswith(':'):
                continue
            line = line[1:]  # strip ':'
            byte_count  = int(line[0:2],  16)
            record_type = int(line[6:8],  16)
            if record_type == 0x01:  # EOF
                break
            if record_type == 0x00:  # data
                raw = bytes.fromhex(line[8:8 + byte_count * 2])
                data.extend(raw)
    return data

if __name__ == "__main__":
    import os
    hex_file = os.path.join(os.path.dirname(__file__), "sub.hex")
    banner_bytes = parse_intel_hex(hex_file)
    # Strip null bytes
    text = banner_bytes.replace(b'\x00', b'').decode('ascii', errors='ignore')
    print(text)
    print("  [Decoded from Intel HEX by sub_decoder.py]")
