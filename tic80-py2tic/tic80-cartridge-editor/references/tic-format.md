# TIC-80 .tic Binary Format

## Chunk Structure

A .tic file is a sequence of chunks with no file header. Each chunk:

```
[type: 1 byte] [size: 2 bytes LE] [reserved: 1 byte] [data: size bytes]
```

- **type**: chunk type ID (see table below)
- **size**: little-endian uint16, byte count of data that follows
- **reserved**: always `0x00` in practice
- **data**: raw chunk payload

## Chunk Types

| Type | Hex | Description | Data format |
|------|-----|-------------|-------------|
| TILES | 0x01 | Sprite sheet | 32 bytes per 8x8 tile, 4bpp packed. Tile N starts at offset N*32. Trailing zero bytes trimmed. |
| MAP | 0x12 | Tilemap | 240 bytes per row (1 byte = tile index). Row N starts at offset N*240. Trailing zeros trimmed. |
| CODE | 0x05 | Source code | Plain ASCII text (Python/Lua/JS/etc). No null terminator. |
| CODE_ZIP | 0x04 | Compressed code | Zlib-compressed source code. |
| PALETTE | 0x09 | Color palette | 48 bytes: 16 colors, 3 bytes (R,G,B) each. |
| DEFAULT | 0x0E | Default flag | 1 byte, value `0x01`. Meaning: use default palette if palette chunk has all zeros. |
| MARKER | 0x11 | Start marker | Size 0, no data. Always the first chunk in the file. |
| SCREEN | 0x0F | Screenshot | Screen capture data for cart preview. |
| FLAGS | 0x06 | Sprite flags | 1 byte per sprite (256 sprites = 256 bytes). |
| SAMPLES | 0x07 | SFX data | Sound effect definitions. |
| WAVEFORM | 0x08 | Waveforms | Wave pattern data for SFX. |
| MUSIC_PAT | 0x0A | Music patterns | Music pattern data. |
| MUSIC_TRK | 0x0B | Music tracks | Music track data. |

## Typical Chunk Order

```
MARKER(0x11) → TILES(0x01) → [MAP(0x12)] → PALETTE(0x09) → DEFAULT(0x0E) → CODE(0x05)
```

MAP is optional. Other sections (SFX, MUSIC, FLAGS, SCREEN) appear when present.

## Tile Data Format

Each 8x8 sprite tile = 32 bytes. Pixels are 4-bit (16 colors), packed 2 pixels per byte (low nibble = left pixel, high nibble = right pixel).

In the text format, tile hex strings are 64 chars (32 bytes). Example:
```
# 001:66eeeeee6e0000006e0000006e000ddd6e0000006e00000066eeeeee66666666
```

The binary representation is identical — `bytes.fromhex()` of the hex string.

## Map Data Format

Each map row = 240 bytes (one byte per cell, value = tile index 0-255).

In text format, rows are variable-length hex strings:
```
# 000:001020002020002030003010003043004310008000500040...
```

Each pair of hex chars = one map cell. Rows shorter than 240 bytes are zero-padded on the right.

## Palette Format

48 bytes: 16 colors × 3 bytes (R, G, B). Example (Sweetie 16):
```
1a1c2c 5d275d b13e53 ef7d57 ffcd75 a7f070 38b764 257179
29366f 3b5dc9 41a6f6 73eff7 f4f4f4 94b0c2 566c86 333c57
```

## Text-to-Binary Conversion

Text cartridges (.py/.lua/.js) embed asset data as comments:
```python
# <TILES>
# 001:66eeeeee...
# </TILES>
# <MAP>
# 000:001020...
# </MAP>
# <PALETTE>
# 000:1a1c2c5d275d...
# </PALETTE>
```

To convert: parse each `# <SECTION>` block, convert hex to binary, wrap in chunk headers, concatenate.

Code = everything before the first `# <SECTION>` tag.
