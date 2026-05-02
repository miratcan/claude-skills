#!/usr/bin/env python3
"""Convert a TIC-80 .py text cartridge to a .tic binary cartridge.

Usage: python3 py2tic.py input.py [output.tic]

If output is omitted, writes to input with .tic extension.
Does NOT require TIC-80 PRO.
"""

import re
import struct
import sys

# TIC-80 .tic chunk types
CHUNK_MARKER = 0x11
CHUNK_TILES = 0x01
CHUNK_MAP = 0x12
CHUNK_PALETTE = 0x09
CHUNK_DEFAULT = 0x0E
CHUNK_CODE = 0x05


def make_chunk(chunk_type: int, data: bytes, reserved: int = 0) -> bytes:
    """Build a .tic chunk: type(1) + size(2 LE) + reserved(1) + data."""
    return struct.pack('<BHB', chunk_type, len(data), reserved) + data


def parse_hex_section(text: str, tag: str) -> dict[int, bytes]:
    """Parse a TIC-80 text section (TILES, MAP, etc.) into {id: bytes}."""
    start = text.find(f'# <{tag}>')
    end = text.find(f'# </{tag}>')
    if start == -1 or end == -1:
        return {}
    section = text[start:end]
    result = {}
    for m in re.finditer(r'# (\d{3}):([0-9a-fA-F]+)', section):
        result[int(m.group(1))] = bytes.fromhex(m.group(2))
    return result


def build_tile_data(tiles: dict[int, bytes]) -> bytes:
    """Pack sprite tiles into contiguous binary (32 bytes per 8x8 tile)."""
    if not tiles:
        return b''
    max_id = max(tiles.keys())
    data = bytearray((max_id + 1) * 32)
    for tid, tdata in tiles.items():
        offset = tid * 32
        data[offset:offset + len(tdata)] = tdata
    return bytes(data.rstrip(b'\x00'))


def build_map_data(rows: dict[int, bytes]) -> bytes:
    """Pack map rows into contiguous binary (240 bytes per row)."""
    if not rows:
        return b''
    max_row = max(rows.keys())
    data = bytearray((max_row + 1) * 240)
    for rid, rdata in rows.items():
        offset = rid * 240
        data[offset:offset + len(rdata)] = rdata
    return bytes(data.rstrip(b'\x00'))


def extract_code(text: str) -> bytes:
    """Extract Python code (everything before first # <SECTION> tag)."""
    for tag in ['TILES', 'SPRITES', 'MAP', 'WAVES', 'SFX', 'TRACKS',
                'PALETTE', 'FLAGS', 'SCREEN']:
        marker = f'\n# <{tag}>'
        pos = text.find(marker)
        if pos != -1:
            return (text[:pos].rstrip() + '\n').encode('ascii')
    return text.encode('ascii')


def convert(py_path: str, tic_path: str) -> None:
    with open(py_path, 'r') as f:
        text = f.read()

    code = extract_code(text)
    tiles = parse_hex_section(text, 'TILES')
    map_rows = parse_hex_section(text, 'MAP')

    # Palette: 48 bytes (16 colors * 3 RGB)
    pal_match = re.search(
        r'# <PALETTE>.*?# \d{3}:([0-9a-fA-F]+)', text, re.DOTALL)
    palette = bytes.fromhex(pal_match.group(1)) if pal_match else b'\x00' * 48

    # Build .tic file
    output = bytearray()
    output += make_chunk(CHUNK_MARKER, b'')

    tile_data = build_tile_data(tiles)
    if tile_data:
        output += make_chunk(CHUNK_TILES, tile_data)

    map_data = build_map_data(map_rows)
    if map_data:
        output += make_chunk(CHUNK_MAP, map_data)

    # Palette chunk (padded to 48 bytes minimum)
    pal_data = bytearray(48)
    pal_data[:len(palette)] = palette[:48]
    output += make_chunk(CHUNK_PALETTE, bytes(pal_data))

    output += make_chunk(CHUNK_DEFAULT, b'\x01')
    output += make_chunk(CHUNK_CODE, code)

    with open(tic_path, 'wb') as f:
        f.write(output)

    print(f'Written {len(output)} bytes to {tic_path}')
    print(f'  Code: {len(code)} bytes')
    print(f'  Tiles: {len(tiles)} sprites')
    print(f'  Map: {len(map_rows)} rows')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} input.py [output.tic]')
        sys.exit(1)

    py_path = sys.argv[1]
    tic_path = sys.argv[2] if len(sys.argv) > 2 else py_path.rsplit('.', 1)[0] + '.tic'
    convert(py_path, tic_path)
