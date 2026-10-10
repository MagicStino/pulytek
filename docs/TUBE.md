# Tube Warmth design

PulyTek adds an original, amp-inspired colour processor to Alberto Barrera's passive WDF equalizer.
It is not a component-level simulation of a named tube amp, nor code borrowed from one.

- **DRIVE** continuously maps 0–100% to 0–18 dB internal excitation. Each of two asymmetric soft
  stages is normalized to unity small-signal gain at its operating point. Higher settings compress
  peaks and generate even and odd harmonics; they do not simply add output gain.
- **WARMTH** continuously adds a broad 180 Hz bell (0–2.5 dB, Q 0.55) before the stages and a
  gentle 4.5 kHz high shelf (0 to −3.5 dB) afterwards. It also increases asymmetry and a bounded
  envelope-dependent compression term with 8 ms attack and 120 ms release. This is a deliberately
  tuned colour curve, not a claim that all valves have this frequency response.
- **MIX** continuously blends the EQ/AIR signal with that processed signal from 0–100%.
  0% is exactly the untreated signal; disabling Tube also leaves it untreated. Default Drive 25%,
  Warmth 50%, Mix 50%, Tube off. Output trim follows the blend.

Each nonlinear stage uses first-order antiderivative antialiasing (ADAA): the divided difference
of the stable log(cosh) primitive of biased tanh. Near equal adjacent samples it uses the analytic
midpoint limit. This reduces folded harmonics compared with direct waveshaping. It does not remove
all aliasing. The stages introduce frequency-dependent smoothing and approximately one sample of
combined delay at low levels; parallel mixing can change the high-frequency response. There is no
additional host block latency. A 10 Hz DC blocker removes the asymmetric stages' offset. Drive and
bias targets smooth over 20 ms; filter coefficients update with Warmth, so fast automated Warmth
changes and switch transitions still need listening tests on hardware.

Research informing the method:
[Parker, Zavalishin and Le Bivic, *Reducing the Aliasing of Nonlinear Waveshaping Using Continuous-Time
Convolution*, DAFx 2016](https://www.dafx.de/paper-archive/details/vem_XXF5qBbfiWOH2RVVAA).
[Macak and Schimmel, *Real-Time Guitar Tube Amplifier Simulation using an Approximation of Differential
Equations*, DAFx 2010](https://www.dafx.de/paper-archive/2010/DAFx10/MacakSchimmel_DAFx10_P12.pdf)
explains why coupling and dynamic bias matter in physical amp models; PulyTek's bounded envelope
term is an artistic approximation, not that paper's circuit solver. No research implementation is copied.

`tests/tube_test.cpp` measures the colour curve at 44.1/48/96 kHz, even/odd harmonics, DC removal,
compression, tail decay, and folded-third-harmonic reduction against direct shaping in one fixed case.
Full-core tests check dry mix, bypass, stereo isolation, extreme controls and state restoration.
Device listening and CPU/underrun measurements remain required before a stable hardware release.
