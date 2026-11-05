"""Tiny verified byte-patch format: JSON {target, patches:[{offset, old, new}]} (hex strings).
Refuses to apply unless `old` matches, so a patch can never silently hit the wrong build."""
import json, sys

def apply(data: bytes, spec: dict) -> bytes:
    out = bytearray(data)
    for p in spec["patches"]:
        off, old, new = p["offset"], bytes.fromhex(p["old"]), bytes.fromhex(p["new"])
        assert len(old) == len(new), "size-changing patches are not supported"
        if bytes(out[off:off+len(old)]) != old:
            raise SystemExit(f"patch mismatch at 0x{off:x} in {spec['target']}: have {bytes(out[off:off+len(old)]).hex()}, want {old.hex()}")
        out[off:off+len(new)] = new
    return bytes(out)

def load(path):
    return json.load(open(path))
