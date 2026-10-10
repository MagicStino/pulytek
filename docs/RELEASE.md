PulyTek is a separate open-source Pultec-style EQ port for the native Akai Force/MPC Gen1 OpenPlugin format.

- Blue vintage panel, Bakelite-style knobs, ribbed selector buttons, warm lamps and stereo VU meters.
- Upstream EQP-WDF-1A passive WDF circuit by Alberto Barrera / ABSounds, GPLv3.
- Extra tube-colour switch with DRIVE, WARMTH and continuous wet/dry MIX, six-frequency AIR shelf, output trim and full bypass.
- Side Mixing on/off, 0–200% stereo width, side level and four side-only parametric bands.
- Native ARMv7 hard-float VST2 effect, Akai TUI skin, Q-Link mappings, portable installer and complete corresponding source.

**Pilot release: physical Force/MPC audio, CPU, controls, meter refresh, project reload and installation still need testing.**
Desktop DSP and native host tests passed with sanitizers. ARM loading/audio/state passed under QEMU with Force 3.9.1
system libraries; that is not a physical-device compatibility guarantee. Read README.md and docs/VALIDATION.md.

The portable ZIP is for Force/MPC; the optional desktop Linux VST3 is a separate CI artifact and is not installed on Force.
