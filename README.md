# AS-Pocket-Mortys-vita
A native PS Vita port of Pocket Mortys. Originally released for iOS/Android/PC and shut down along with its servers in April of 2026, this port was meant to get the offline version of the game running natively on the ps vita so players could still enjoy this amazing game.

Built with Unity 2018.2.19f1 (PSP2), based on version 1.94 apk.

# Installation
No VPK is provided directly. Release contains an xdelta patch that must be applied to your own copy of the original game. You need to have the Pocket_Mortys_version 1.94.apk (must be the correct hash).

Install PocketMortys_Stub.vpk on your Vita with VitaShell
Download [xdelta3](https://github.com/jmacd/xdelta) [(Windows builds here)](https://github.com/jmacd/xdelta-gpl/releases) and put xdelta3.exe, the Pocket_Morties_version1.94.apk and PocketMortysData.xdelta in the same folder
Open a command prompt in that folder and run:
./xdelta3 -d -B 134217728 -s NameofYourAPK.apk PocketMortysData.xdelta PocketMortysData.zip

Extract PocketMortysData.zip and copy its contents into ux0:app/POMO00137/ and merge with the existing files
Launch Pocket Mortys

Saves are stored in ux0:/data/PocketMortys/. Saves survive updates and reinstalls as they are separate from the game's actual data files.

