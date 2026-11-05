# Strip: Kochava (and why Upsight needs nothing)

Follow-up for the server shutdown: stop the game's Kochava attribution/ad SDK from making network requests.
It works at the IL2CPP method level, with one verified byte patch to `Media/Modules/Il2CppAssemblies.suprx`.
`global-metadata.dat` is untouched and no function changes size.

- `patches/0003-kochava-network-coroutines-off.json`: the three Kochava coroutines that build a `WWW` (`Init_KV` -> control.kochava.com/track/kvinit, `processQueue` -> kvTracker / bidder.kochava.com/adserver, `KochavaAttributionTimerFired` -> kvquery) now return "finished" at their first step.
- `apply_patch.py`: applies a patch to your own suprx. It refuses unless the original bytes match.
- `NOTES.md`: how the targets were found, the call-site scan, and why Upsight is already inert on Vita (all 14 native entry points are gated on `Application.platform == 11`).

```
python3 strip/apply_patch.py strip/patches/0003-kochava-network-coroutines-off.json \
    Media/Modules/Il2CppAssemblies.suprx Media/Modules/Il2CppAssemblies.suprx.new
```
Replace the module inside `ux0:app/POMO00137/Media/Modules/` with the `.new` file (keep a copy of the original).

Status: static analysis only. Not yet confirmed by a packet capture on hardware. Linking is unchanged, so this is a runtime stub, not removal of the SDK's code.
