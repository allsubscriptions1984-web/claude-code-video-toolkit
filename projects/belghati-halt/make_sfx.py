#!/usr/bin/env python3
"""Synthesize the story's sound effects (free, no samples): knocks, drip, punch-machine thunk,
old phone bell, latch, power-down and a distant train whistle. Writes audio/sfx/<name>.wav.

Run from the toolkit root: uv run projects/belghati-halt/make_sfx.py
"""
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 44100
OUT = Path(__file__).parent / "audio" / "sfx"
rng = np.random.default_rng(3)


def t(secs: float) -> np.ndarray:
    return np.arange(int(SR * secs)) / SR


def env(x: np.ndarray, attack: float, decay: float) -> np.ndarray:
    tt = np.arange(len(x)) / SR
    return x * np.minimum(1, tt / max(attack, 1e-4)) * np.exp(-tt / decay)


def lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    for i in range(1, len(x)):
        y[i] = (1 - a) * x[i] + a * y[i - 1]
    return y


def place(total: float, *events) -> np.ndarray:
    out = np.zeros(int(SR * total))
    for at, sound in events:
        i = int(SR * at)
        out[i:i + len(sound)] += sound[: len(out) - i]
    return out


def knock() -> np.ndarray:
    """A knuckle on a wooden shutter: a low body thump plus a short woody click."""
    body = env(np.sin(2 * np.pi * 95 * t(0.35)) + 0.6 * np.sin(2 * np.pi * 170 * t(0.35)), 0.002, 0.06)
    click = env(lowpass(rng.normal(0, 1, len(t(0.35))), 1800), 0.0005, 0.012)
    return 0.8 * body + 0.5 * click


def knocks(n: int, slow_last: bool) -> np.ndarray:
    times = [0.0, 0.55, 1.1] + ([2.6] if slow_last else [1.65])[: max(0, n - 3)]
    return place(times[-1] + 0.6, *[(at, knock()) for at in times[:n]])


def drip() -> np.ndarray:
    def one(f):  # a falling drop: a quick upward chirp
        tt = t(0.12)
        return env(np.sin(2 * np.pi * (f + 2200 * tt) * tt), 0.001, 0.025)
    return place(3.2, (0.0, one(900)), (1.1, one(1000)), (2.2, one(860)))


def khat() -> np.ndarray:
    """Brass ticket punch: a metallic clack with a ring."""
    clack = env(lowpass(rng.normal(0, 1, len(t(0.4))), 3500), 0.0005, 0.02)
    ring = env(np.sin(2 * np.pi * 1750 * t(0.4)) + 0.5 * np.sin(2 * np.pi * 2630 * t(0.4)), 0.001, 0.08)
    thud = env(np.sin(2 * np.pi * 120 * t(0.4)), 0.001, 0.05)
    return 0.9 * clack + 0.25 * ring + 0.6 * thud


def phone() -> np.ndarray:
    """Old electromechanical bell: 2 s rings of a ~20 Hz hammer on two tones."""
    def ring(secs):
        tt = t(secs)
        tone = np.sin(2 * np.pi * 820 * tt) + 0.7 * np.sin(2 * np.pi * 1240 * tt)
        hammer = (np.sin(2 * np.pi * 20 * tt) > 0).astype(float)
        return tone * (0.4 + 0.6 * lowpass(hammer, 300)) * np.minimum(1, tt / 0.01) * np.minimum(1, (secs - tt) / 0.05)
    return place(5.2, (0.0, ring(1.6)), (3.0, ring(1.6)))


def latch() -> np.ndarray:
    scrape = env(lowpass(rng.normal(0, 1, len(t(0.35))), 2500), 0.05, 0.12) * 0.4
    clack = env(lowpass(rng.normal(0, 1, len(t(0.3))), 4000), 0.0005, 0.015)
    return place(0.8, (0.0, scrape), (0.3, clack))


def power_down() -> np.ndarray:
    tt = t(2.2)
    f = 120 * np.exp(-tt * 1.3)
    hum = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.2)
    clunk = env(np.sin(2 * np.pi * 70 * t(0.5)) + lowpass(rng.normal(0, 1, len(t(0.5))), 600), 0.001, 0.08)
    return place(2.4, (0.0, clunk), (0.02, 0.6 * hum))


def whistle() -> np.ndarray:
    """Distant train whistle: a soft chord with slow vibrato, swelling and fading."""
    tt = t(3.5)
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5 * tt)
    chord = sum(a * np.sin(2 * np.pi * f * vib * tt) for f, a in ((622, 1), (740, 0.8), (932, 0.6)))
    shape = np.sin(np.pi * np.clip(tt / 3.5, 0, 1)) ** 1.5
    breath = lowpass(rng.normal(0, 1, len(tt)), 2000) * 0.15
    return lowpass((chord + breath) * shape, 2500)


def save(name: str, x: np.ndarray, peak: float = 0.7) -> None:
    x = x / (np.abs(x).max() + 1e-9) * peak
    tail = int(SR * 0.6)  # a little room ambience so effects don't sound pasted on
    wet = np.convolve(x, np.exp(-np.arange(tail) / (SR * 0.12)) * rng.normal(0, 1, tail) * 0.02)[: len(x) + tail]
    y = np.concatenate([x, np.zeros(tail)])
    y[: len(wet)] += wet
    sf.write(OUT / f"{name}.wav", np.stack([y, y], 1), SR)
    print(f"{name}.wav  {len(y) / SR:.1f}s")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    save("knock3", knocks(3, False))
    save("knock4", knocks(4, True))
    save("drip", drip(), 0.5)
    save("khat", khat())
    save("phone", phone(), 0.55)
    save("latch", latch(), 0.6)
    save("power-down", power_down())
    save("whistle", whistle(), 0.32)


if __name__ == "__main__":
    main()
