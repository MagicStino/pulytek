PulyTek is a separate open-source Pultec-style EQ port for the native Akai Force/MPC Gen1 OpenPlugin format.

- Blue vintage panel, Bakelite-style knobs, ribbed selector buttons, warm lamps and stereo VU meters.
- Upstream EQP-WDF-1A passive WDF circuit by Alberto Barrera / ABSounds, GPLv3.
- Extra tube-colour switch with DRIVE, WARMTH and continuous wet/dry MIX, six-frequency AIR shelf with one continuous AMOUNT control, output trim and full bypass.
- Side Mixing on/off, 0–200% stereo width, side level and four side-only parametric bands.
- Native ARMv7 hard-float VST2 effect, Akai TUI skin, Q-Link mappings, portable installer and complete corresponding source.

**The maintainer reports hardware testing of the preceding plugin version. This release’s new LED touch behavior still needs device verification; a detailed device/firmware record and CPU benchmark are pending.**
Desktop DSP and native host tests passed with sanitizers. ARM loading/audio/state passed under QEMU with Force 3.9.1
system libraries; that is not a physical-device compatibility guarantee. Read README.md and docs/VALIDATION.md.

The portable ZIP is for Force/MPC; the optional desktop Linux VST3 is a separate CI artifact and is not installed on Force.

0.1.0-rc2 adds a combined Tube & AIR page with Drive and Mix controls. Legacy rc1 tube/EQ state chunks load with the original +3 dB, fully wet AIR defaults.

0.1.0-rc3 removes the redundant AIR Mix knob, renames AIR Drive to Amount and turns AIR off below 2%. Tube controls are unchanged. Legacy native state migrates; rc2 partial AIR mixes preserve high-frequency gain approximately through the shelf transition.

49 original factory programs: Init and six each for Voice, Drums, Bass, Guitar, Keys, Bus, Master and Stereo. Native PRESET menu and desktop VST3 program support; complete control recall, including AIR amount before enable. Includes Drums Smash Bassdrum and Master Light / Hard Colour / Air / Smile / Warm / Wide Polish.

0.1.0-rc4 corrects VU metering: sine-calibrated rectified averaging, two-pole needle inertia (approximately 300 ms to 99%), symmetric smooth return, 20 Hz visual updates and voltage-proportional scale spacing. The clearly labelled programme reference is now 0 VU = -9 dBFS RMS, to avoid pinning on louder samples. +3 VU is -6 dBFS RMS-equivalent; sustained levels above that still legitimately reach the stop. Audio processing and preset settings are unchanged.

Global OUTPUT COMP is beside the stereo meters. It reuses the existing final output parameter and preserves preset/project gains; metering follows it.

1.0.0 makes AIR enable independent of Amount at every setting, including 0%. All LED lamps toggle on touch; POWER toggles global bypass and lights when processing is active. Tube, AIR and Side lamps toggle their own sections. Existing project and preset parameter keys are unchanged.
