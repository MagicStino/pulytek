# Install PulyTek 0.1.0-rc3

Experimental release candidate for Akai Force / MPC Gen1 running OpenPlugin-compatible firmware.
The plugin has passed desktop DSP/host tests and ARM emulated loading against Force 3.9.1 libraries.
**This release has not been tested on physical Force or MPC hardware.**

1. Download `PulyTek-0.1.0-rc3-mpc-armv7.zip` and its SHA256 file from this project's GitHub release.
2. Verify the ZIP checksum, unpack the whole folder and copy it to your device.
3. Save your project. The installer stops/restarts the MPC application and backs up its settings.
4. In a device root shell, run `sh install.sh` inside the unpacked folder. Use `-y` only to skip its confirmation.
5. Insert **PulyTek** as an audio **effect**, not as an instrument.

The standard portable installer places `MagicStino - VST - PulyTek/` in `/sdcard/Synths`, registers its
VST2 entry in `pluginList-arm` and includes the native touchscreen skin. `-t /absolute/Synths/path` selects
another executable storage location. A noexec volume cannot load plugins.

After maintainer acceptance, OpenPlugin's native catalog can install the reviewed package.
Before acceptance, a posted submission does not enable a catalog download automatically.
The source scanner's latest-stable-release rule may exclude this prerelease; manual installation is the pilot route.

To remove it, run the package's `uninstall.sh`. Save first: removal also restarts the application.
MPC Gen2, desktop VST3 installation on Force, stock firmware without plugin registration, and hardware CPU
performance are outside the validated scope. Firmware is not supplied or modified by this project.

The optional Linux VST3 build uses a host-generated parameter editor, not the Akai skin. It is not installed by this package.
Complete corresponding source and license texts are included inside the portable plugin folder.
