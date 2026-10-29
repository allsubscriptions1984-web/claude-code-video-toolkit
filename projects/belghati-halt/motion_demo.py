#!/usr/bin/env python3
"""Free 2D motion-comic shot: one still → SECS of video with fog, lamp flicker, grain and an optional scare.

Run from the toolkit root:
    uv run projects/belghati-halt/motion_demo.py IMAGE OUT.mp4 SECS [SCARE_AT] [MUSIC.mp3]
SCARE_AT is the second of the shake + flash + zoom punch; pass -1 for none.
"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

W, H, FPS = 1920, 1080, 30
rng = np.random.default_rng(7)


def fog_texture(w: int, h: int, blur: int, seed: int) -> np.ndarray:
    """Soft cloudy noise in 0..1, tileable enough to scroll sideways."""
    r = np.random.default_rng(seed)
    small = Image.fromarray((r.random((h // 16, w // 16)) * 255).astype(np.uint8))
    big = small.resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(big, dtype=np.float32) / 255
    return (a - a.min()) / (a.max() - a.min() + 1e-6)


def main() -> None:
    src = Image.open(sys.argv[1]).convert("RGB")
    global SECS, SCARE
    out, SECS = sys.argv[2], float(sys.argv[3])
    SCARE = float(sys.argv[4]) if len(sys.argv) > 4 else -1.0
    music = sys.argv[5] if len(sys.argv) > 5 else None
    base = np.asarray(src.resize((int(W * 1.15), int(H * 1.15)), Image.LANCZOS), dtype=np.float32) / 255
    bh, bw, _ = base.shape

    lum = base.mean(axis=2)
    glow = np.asarray(Image.fromarray((np.clip((lum - 0.55) * 4, 0, 1) * 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(40)), dtype=np.float32)[..., None] / 255

    fog_far = fog_texture(W * 2, H, 60, 1)[..., None]
    fog_near = fog_texture(W * 2, H, 25, 2)[..., None]
    tint = np.array([0.62, 0.72, 0.66], dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    vignette = (1 - 0.55 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2))[..., None]
    vignette = np.clip(vignette, 0.25, 1).astype(np.float32)

    # lamp flicker: mostly steady, with short random dips
    n = int(SECS * FPS)
    flicker = np.ones(n, dtype=np.float32)
    for start in rng.choice(n - 6, 9, replace=False):
        flicker[start:start + rng.integers(2, 6)] = rng.uniform(0.15, 0.6)

    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if music:
        cmd += ["-i", music, "-map", "0:v", "-map", "1:a", "-shortest", "-c:a", "aac", "-b:a", "160k",
                "-af", f"afade=t=in:d=1,afade=t=out:st={SECS - 1.5}:d=1.5"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for i in range(n):
        t = i / FPS
        p = t / SECS
        zoom = 1.0 + 0.06 * p
        dt = t - SCARE if SCARE >= 0 else -1.0
        shake = (0, 0)
        if 0 <= dt < 0.45:
            zoom += 0.05 * (1 - dt / 0.45)
            amp = 18 * (1 - dt / 0.45)
            shake = (rng.uniform(-amp, amp), rng.uniform(-amp, amp))
        cw, ch = W / zoom * (bw / W) / 1.15 * 1.0, H / zoom * (bh / H) / 1.15
        cx, cy = bw / 2 + shake[0], bh / 2 + 0.02 * bh * p + shake[1]
        x0, y0 = int(cx - cw / 2), int(cy - ch / 2)
        crop = Image.fromarray((base[y0:y0 + int(ch), x0:x0 + int(cw)] * 255).astype(np.uint8))
        frame = np.asarray(crop.resize((W, H), Image.BILINEAR), dtype=np.float32) / 255

        g = np.asarray(Image.fromarray((glow[..., 0] * 255).astype(np.uint8))
                       .crop((x0, y0, x0 + int(cw), y0 + int(ch))).resize((W, H)), dtype=np.float32)[..., None] / 255
        frame = frame * (1 - 0.55 * g * (1 - flicker[i])) * (0.94 + 0.06 * flicker[i])

        far = np.roll(fog_far, -int(t * 40), axis=1)[:, :W]
        near = np.roll(fog_near, -int(t * 95), axis=1)[:, :W]
        fog = np.clip(0.13 * far + 0.09 * near * (0.8 + 0.2 * np.sin(t * 0.9)), 0, 1)
        frame = 1 - (1 - frame) * (1 - fog * tint)  # screen blend

        if 0 <= dt < 0.12:
            frame = np.clip(frame + 0.55 * (1 - dt / 0.12), 0, 1)
        frame *= vignette
        frame += rng.normal(0, 0.022, (H, W, 1)).astype(np.float32)
        ff.stdin.write((np.clip(frame, 0, 1) * 255).astype(np.uint8).tobytes())
    ff.stdin.close()
    ff.wait()


if __name__ == "__main__":
    main()
