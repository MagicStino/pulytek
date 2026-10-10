# Attribution and license notices

PulyTek is a separate Force/MPC port maintained by MagicStino. Original PulyTek adapter, side processing,
AIR shelf, tube-colour extension, panel drawings and build scripts: GPL-3.0-only.

The passive Pultec-style WDF model is **EQP-WDF-1A by Alberto Barrera (ABSounds)**, developed for a
Master's thesis at the Music Technology Group, Universitat Pompeu Fabra, supervised by Xavier Lizarraga.
Upstream: https://github.com/ABSounds/EQP-WDF-1A — GPLv3; full upstream LICENSE retained at the root.
Pinned commit: fb3d733e04fe65e73fa87843ea61fca103a0a5d7.
Only EQP1A.cpp, EQP1A.h and the bundled chowdsp_wdf.h are used. The JUCE include/math constant is
replaced by standard C++ math. The low-frequency cached selector starts at -1 so the first requested
frequency always updates the components. The circuit topology and component values are unchanged.
The desktop GUI, presets, photographs, My-JUCE-Modules and upstream trademarks/logos are not copied.

chowdsp_wdf: Chowdhury DSP / Jatin Chowdhury, BSD-3-Clause; license in licenses/.
The upstream amalgamation does not identify its exact library revision. We retain it verbatim and add
the BSD notice from the official library repository (43bcd295e8403de913f9966f4fd7ff9d17c9f1a5).
The library's embedded Stefano D'Angelo MIT notices are preserved inside chowdsp_wdf.h.

mpc-vst-plugins native VST2 wrapper, touchscreen/Q-Link skin generator and portable installer:
sd88me, MIT. Pinned revision matches force-openplugin's dependencies.json:
95cc428cd7d4042230cc854a780fb0b7dfa1921f. The local wrapper extension is generated separately:
floating-point stereo processing and host sample-rate/reset forwarding. Unmodified dependency sources
and MIT notices ship with corresponding source. force-shadow artwork tooling: sd88me, MIT.

DejaVu typefaces (Bitstream Vera derivative) and their original notices: licenses/DejaVu-fonts.txt.
The bundled serif files are used to rasterize the artwork. Live text uses firmware-native Roboto.
JUCE 7.0.12 is used only by the optional Linux VST3 build under its GPLv3 option; upstream source/license
are fetched by CMake, and should accompany any separately distributed VST3 binary.

Technical examples inspected: sd88me/mpc-vst-dx7 (Dexed) for skin format, parameter mapping and installer
conventions, and mmiroshnikov/mpc-airwindows for native effect packaging. Their designs are not copied.
PulyTek's blue panel, ribbed buttons, knob styling and VU drawings are newly created.
Pultec, Akai, MPC, Force and AIR are referenced descriptively; there is no affiliation or endorsement.
