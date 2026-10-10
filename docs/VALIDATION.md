# Validation scope

Checked locally on 10 October 2026:

- DSP checks at 22.05, 44.1, 48 and 96 kHz, including extreme parameter combinations and finite output.
- Low-frequency WDF boost response; four side peaking bands; all six AIR frequencies.
- Independent channels, exact bypass above 0 dBFS, width-neutral identity, mono fold-down and preserved mid signal.
- Tube enabled/disabled, zero mix matching the dry EQ and actual nonlinear colour at full mix.
- Tube response at 44.1/48/96 kHz: maximum Warmth gives approximately +2.50 dB at 180 Hz and −3.44 to −3.48 dB at 12 kHz. Even/odd harmonics, compression, DC removal and tail decay pass. First-stage ADAA reduces a folded third harmonic by 9.62 dB in the fixed 48 kHz/10 kHz comparison test.
- VU reference/ballistics; complete parameter state round trip; invalid state rejected without partial changes.
- ASan/UBSan native host tests: parameters, selectors/data-wheel/Q-Links, independent instances, NULL input,
  accumulated processing, state and concurrent screen/audio access.
- ARM ELF32 EABI hard-float, Cortex-A17, exported VSTPluginMain, maximum glibc 2.29; C++ runtime linked statically.
- ARM QEMU smoke test against the owner's existing extracted Force 3.9.1 system libraries: dlopen, 35 parameters,
  48 kHz, 257-frame floating-point audio, exact bypass, combined processing, state, reset and destruction.
- Native skin bounds, bindings, three pages and Q-Link assets; offline visual inspection. Actual touch operation
  and live meter update on hardware are not established by these tests.
- Portable package manifests/checksums and sandboxed installer/uninstaller using temporary MPC.settings.

The native wrapper extension replaces int16 conversion/buffering only for this port and forwards host sample-rate/reset
calls. It preserves upstream parameter, skin, Q-Link and chunk conventions. No proprietary headers are required.
Source changes to the upstream circuit are documented in NOTICE.md.

Still required on physical Force (then separately on MPC Gen1):

1. Save/back up, install the pilot package, confirm the effect appears and all three pages draw.
2. Verify every selector, switch, knob, Q-Link bank and meter response, with readable labels at normal viewing distance.
3. Listen for parameter-change clicks, tube-stage aliasing, extreme boost/headroom and mono/stereo behavior.
4. Measure CPU/underruns at 128-frame blocks, including multiple instances with tube/side/AIR enabled.
5. Save/reload a project, reopen the effect, reboot, update and uninstall.

No physical-device result, zero-aliasing claim, tube circuit accuracy, CPU budget or universal firmware compatibility is
claimed. Additional stages run at the host sample rate without oversampling. Automation applies changes at block
boundaries; abrupt filter changes can click. Keep headroom when boosting; the floating-point plugin does not act as a limiter.

The optional Linux VST3 is a separate build target. Its CI build result should be checked before distributing it;
its editor is the host-style JUCE generic editor, and it has not been loaded on Force.
