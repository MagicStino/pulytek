# VU meter design

These are output-level VU-style indicators, not peak/clipping or loudness meters. Both channels read processed output; bypass reads the bypassed signal. Audio gain is unaffected.

The original rc1–rc3 implementation smoothed squared samples, updated only ten times a second, mapped dB linearly to needle angle and used a fixed -18 dBFS reference. Loud sample programme material therefore stayed above +3 VU.

rc4 measures absolute voltage and applies two equal 45.2 ms one-pole stages in series. Their combined step response reaches about 99% in 300 ms, starts smoothly and returns on the same schedule; short transients barely move it. The sine calibration factor pi/(2 sqrt(2)) converts mean-absolute voltage to equivalent RMS. Frame position and printed tick angles are proportional to linear voltage, with 0 VU at about 71% travel and +3 at full travel. A 20 Hz display update reduces visible stepping.

The programme-friendly reference is **0 VU = -9 dBFS RMS** for a steady sine (peak -6 dBFS). This is an explicitly chosen digital alignment for loud sample playback, not a claim that -9 is a universal analogue standard. A -18 dBFS RMS sine reads -9 VU. A -6 dBFS RMS sine reads +3. Sustained hotter audio still pegs legitimately; do not use this meter to certify sample/true-peak headroom. Complex waveforms need not match RMS exactly, as with a rectified-average VU.

The behaviour follows the averaging and approximately 300 ms settling described by [Shure’s VU explanation](https://www.shure.com/en-US/insights/shure-tech-tip-vu-and-ppm-audio-meters-an-elementary-explanation) and [Classic Audio’s practical VU circuit design](https://michaelfidler.com/articles/practical-vu-meter-circuits/). The cascade is a software approximation of mechanical inertia, with no overshoot; it is not a certified IEC/ANSI meter.

Tests check steady sine alignment, stereo independence, rise/fall timing, impulse rejection and reset at 44.1/48/96 kHz.

The EQUALIZER front places **OUTPUT COMP** beside the meters. This is the existing global output trim (-20 to +20 dB), applied after every processing stage and before metering. It is manual compensation, not automatic loudness matching or a limiter. Presets and old projects retain their existing output values; no second gain control is introduced. Bypass leaves audio exactly unchanged, including bypassing output compensation.
