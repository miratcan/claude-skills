---
name: tic80-cartridge-editor
description: Read, write, and convert TIC-80 fantasy console cartridge files (.tic binary format). Use when working with TIC-80 game development, converting .py/.lua/.js text cartridges to .tic binary (bypasses PRO requirement), editing code/tiles/map/palette in .tic files, parsing .tic binary structure, or encountering "TIC-80 PRO is needed for text files" error. Triggers on TIC-80, .tic files, fantasy console cartridge editing, py2tic conversion.
---

# TIC-80 Cartridge Editor

Edit TIC-80 .tic binary cartridges and convert text cartridges (.py/.lua/.js) to .tic without PRO.

## Converting .py to .tic

Run the bundled script:

```bash
python3 scripts/py2tic.py input.py output.tic
```

Or build programmatically — see [references/tic-format.md](references/tic-format.md) for the binary format spec.

## Editing Code in a .tic File

To replace code in an existing .tic:

1. Parse chunks from the .tic file
2. Find the CODE chunk (type `0x05`)
3. Replace its data with new code bytes
4. Reassemble all chunks

```python
import struct

def parse_chunks(data):
    chunks = []
    pos = 0
    while pos < len(data) - 3:
        ct = data[pos]
        sz = struct.unpack_from('<H', data, pos + 1)[0]
        res = data[pos + 3]
        chunks.append((ct, res, data[pos+4:pos+4+sz]))
        pos += 4 + sz
    return chunks

def build_tic(chunks):
    out = bytearray()
    for ct, res, data in chunks:
        out += struct.pack('<BHB', ct, len(data), res) + data
    return bytes(out)

# Replace code
data = open('game.tic', 'rb').read()
chunks = parse_chunks(data)
new_chunks = []
for ct, res, cd in chunks:
    if ct == 0x05:  # CODE chunk
        cd = new_code.encode('ascii')
    new_chunks.append((ct, res, cd))
open('game.tic', 'wb').write(build_tic(new_chunks))
```

## Chunk Type Quick Reference

| Type | ID | Description |
|------|----|-------------|
| MARKER | `0x11` | File start marker (size=0, always first) |
| TILES | `0x01` | Sprite tiles (32 bytes per 8x8 tile, 4bpp) |
| MAP | `0x12` | Tilemap (240 bytes per row) |
| CODE | `0x05` | Source code (plain ASCII text) |
| CODE_ZIP | `0x04` | Compressed code (zlib) |
| PALETTE | `0x09` | 48 bytes: 16 colors x 3 RGB |
| DEFAULT | `0x0E` | Default settings (1 byte, value `0x01`) |
| SCREEN | `0x0F` | Screenshot data |

For full format details: [references/tic-format.md](references/tic-format.md)
