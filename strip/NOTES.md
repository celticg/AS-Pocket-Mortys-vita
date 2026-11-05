# Strip: Kochava + Upsight (IL2CPP method level)

All addresses are module-relative to `Il2CppAssemblies` (ELF VA = 0x81000000 + rel; suprx file offset = rel + 0x1100).
Method names come from `arm-none-eabi-nm` and `arm-none-eabi-objdump -M force-thumb` over the unpatched il2cpp ELF (`base/il2cpp.elf`, sha c45c1918…).

## Where the game can reach the network (whole-module scan, executed)
Direct call sites in the 36 MB text segment, counted from the full disassembly:

| API | Callers outside the BCL/Mono networking stack |
|---|---|
| `WWW::.ctor` | `U3CInit_KVU3Ec__Iterator0.MoveNext`, `U3CprocessQueueU3Ec__Iterator1.MoveNext`, `U3CKochavaAttributionTimerFiredU3Ec__Iterator3.MoveNext` (Kochava); `PlayGamesAchievement.LoadImage`, `U3CLoadImageU3Ec__Iterator0`, `U3CloadAvatarFromURLU3Ec__Iterator0` (Google Play Games image fetch) |
| `Application.OpenURL` | `Kochava processQueue` iterator (ad click-through), `SaveDataController.EmailCloudContainerToSupport` (user action, mailto) |
| `HttpWebRequest` / `WebRequest.Create` / `Socket..ctor` | only inside mscorlib/System (`HttpRequestCreator`, `FtpWebRequest`, `WebConnection`); no game-assembly caller |
| `UnityWebRequest` | only inside the `WWW` wrapper |

## Kochava: patched (patch 0003)
The three Kochava iterators above are the only Kochava code that builds a `WWW`. Each `MoveNext()` now begins with
`movs r0,#0 ; bx lr` (00 20 70 47), so the coroutine reports "finished" on its first step and never reaches `new WWW(...)`.

| Method | rel | suprx offset | old -> new |
|---|---|---|---|
| `U3CInit_KVU3Ec__Iterator0::MoveNext` (kvinit) | 0x6d01fc | 7148284 | 2de9f04f -> 00207047 |
| `U3CprocessQueueU3Ec__Iterator1::MoveNext` (kvTracker / adserver / OpenURL) | 0x6b6e64 | 7044964 | 2de9f04f -> 00207047 |
| `U3CKochavaAttributionTimerFiredU3Ec__Iterator3::MoveNext` (kvquery) | 0x6b5ea2 | 7040930 | 2de9f047 -> 00207047 |

Deliberately left alone: `Kochava.Start/Init/Awake/OnEnable` (they assign the static singleton that game-side `Kochava.FireEvent` callers dereference),
`U3CclearQueueU3Ec__Iterator2` (no `WWW`; local queue reset), `global-metadata.dat` (no offsets move; no size-changing patch).
Residual: `Kochava.Init` still runs and still constructs an `AndroidJavaClass` as before the strip; events are still enqueued in memory and persisted through `PlayerPrefs`. Nothing drains them.

## Upsight: no patch needed, and none written
Every native entry point of the Upsight C# wrapper is gated on `Application.platform == 11` (`RuntimePlatform.Android`):
`Upsight__cctor`, `init`, `requestAppOpen`, `sendContentRequest`, `preloadContentRequest`, `getContentBadgeNumber`, `get/setOptOutStatus`,
`trackInAppPurchase`, `reportCustomEvent`, `register/deregisterForPushNotifications`, `setLogLevel`, `getPluginVersion` (14 of 14 carry `cmp r0,#11` after `Application.get_platform`).
The only ungated body, `Upsight.dictionaryToJavaHashMap`, is reached only from those gated bodies. `UpsightController.Awake/AttemptUpsightConnection/Start` additionally test `App.SupportsNativeMobileServices`, which is `platform == 11`.
On Vita the platform value is not 11, so the Upsight SDK does nothing. The Upsight API host is not in the binary (resolved by the Android Java SDK), consistent with this.
Dead on this platform by construction; the hardware capture is the check.

## Not covered by a byte patch
- Google Play Games `WWW` image loads: reachable only through GPGS calls, which are gated behind the same Android check. Counted, not patched.
- hyperurl.co (credits link): `Application.OpenURL` has no game-assembly caller other than the ones listed; the string is reachable from scene/UI event wiring only. Dynamic capture covers it.
