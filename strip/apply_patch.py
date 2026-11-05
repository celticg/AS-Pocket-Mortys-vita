#!/usr/bin/env python3
"""Apply a verified byte patch (strip/patches/*.json) to your own Il2CppAssemblies.suprx.
usage: apply_patch.py PATCH.json IN.suprx OUT.suprx
Refuses to write unless every `old` byte string matches, so it cannot hit the wrong build."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import patchlib

def main(patch, src, dst):
    spec = patchlib.load(patch)
    out = patchlib.apply(pathlib.Path(src).read_bytes(), spec)
    pathlib.Path(dst).write_bytes(out)
    print(f"applied {len(spec['patches'])} edit(s) from {pathlib.Path(patch).name} -> {dst}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    main(*sys.argv[1:4])
