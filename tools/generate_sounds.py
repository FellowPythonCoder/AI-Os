#!/usr/bin/env python3
"""
Synthesize the AURA sound theme (no samples, no licensing questions).

Soft sine chimes with gentle envelopes in AURA's "glass bell" character.
Run: python3 tools/generate_sounds.py → rootfs/usr/share/sounds/aura/stereo/*.wav
"""
import math
import os
import struct
import wave

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "rootfs", "usr", "share", "sounds", "aura", "stereo")
SR = 44100


def tone(freq, dur, vol=0.5, attack=0.012, decay=None, slide_to=None):
    n = int(SR * dur)
    decay = decay if decay is not None else dur
    out = []
    for i in range(n):
        t = i / SR
        f = freq if slide_to is None else freq + (slide_to - freq) * (i / n)
        env = min(1.0, t / attack) * math.exp(-3.0 * t / decay)
        # fundamental + a whisper of harmonic shimmer
        s = math.sin(2 * math.pi * f * t) + 0.18 * math.sin(2 * math.pi * f * 2 * t)
        out.append(vol * env * s / 1.18)
    return out


def noise(dur, vol=0.4):
    import random
    random.seed(42)
    n = int(SR * dur)
    return [vol * (1 - i / n) ** 2 * (random.random() * 2 - 1) for i in range(n)]


def mix(*tracks_with_offset):
    length = max(int(off * SR) + len(tr) for tr, off in tracks_with_offset)
    buf = [0.0] * length
    for tr, off in tracks_with_offset:
        o = int(off * SR)
        for i, v in enumerate(tr):
            buf[o + i] += v
    peak = max(abs(v) for v in buf) or 1.0
    if peak > 0.95:
        buf = [v * 0.95 / peak for v in buf]
    return buf


def save(name, samples):
    path = os.path.join(OUT, name)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        packed = []
        for v in samples:
            s = int(max(-1.0, min(1.0, v)) * 32767)
            packed.append(struct.pack("<hh", s, s))
        w.writeframes(b"".join(packed))
    print("sound:", name, f"({len(samples) / SR:.2f}s)")


def main():
    os.makedirs(OUT, exist_ok=True)
    C5, E5, G5, C6 = 523.25, 659.25, 783.99, 1046.50
    # Welcome: rising mountain arpeggio
    save("desktop-login.wav", mix(
        (tone(C5, 1.1, 0.45), 0.0), (tone(E5, 1.1, 0.45), 0.13),
        (tone(G5, 1.15, 0.45), 0.26), (tone(C6, 1.3, 0.5), 0.39)))
    # Goodbye: gentle descent
    save("desktop-logout.wav", mix(
        (tone(C6, 0.9, 0.4), 0.0), (tone(G5, 0.9, 0.4), 0.14),
        (tone(E5, 1.1, 0.42), 0.28), (tone(C5, 1.25, 0.42), 0.42)))
    save("message-new-instant.wav", mix((tone(880, 0.5, 0.4), 0),
                                        (tone(1318.5, 0.7, 0.35), 0.09)))
    save("dialog-information.wav", tone(987.77, 0.45, 0.35))
    save("dialog-warning.wav", mix((tone(440, 0.4, 0.4), 0),
                                   (tone(440, 0.5, 0.4), 0.22)))
    save("dialog-error.wav", mix((tone(220, 0.55, 0.42), 0),
                                 (tone(233.08, 0.55, 0.35), 0.02)))
    save("audio-volume-change.wav", tone(740, 0.16, 0.3, decay=0.16))
    save("bell.wav", tone(1046.5, 0.7, 0.4))
    save("camera-shutter.wav", mix((noise(0.05, 0.5), 0),
                                   (noise(0.09, 0.35), 0.07)))
    save("trash-empty.wav", tone(660, 0.55, 0.35, slide_to=180))
    save("device-added.wav", mix((tone(659.25, 0.35, 0.35), 0),
                                 (tone(987.77, 0.5, 0.35), 0.1)))
    save("device-removed.wav", mix((tone(987.77, 0.35, 0.35), 0),
                                    (tone(659.25, 0.5, 0.35), 0.1)))
    save("complete.wav", mix((tone(G5, 0.5, 0.35), 0),
                             (tone(C6, 0.8, 0.4), 0.12)))
    # theme index
    idx = os.path.join(os.path.dirname(OUT), "index.theme")
    with open(idx, "w", encoding="utf-8") as fh:
        fh.write("""[Sound Theme]
Name=AURA
Comment=AURA OS glass-bell sound theme
Directories=stereo

[stereo]
OutputProfile=stereo
""")
    print("Sound theme generated.")


if __name__ == "__main__":
    main()
