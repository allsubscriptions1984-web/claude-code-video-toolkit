#!/usr/bin/env python3
"""Time each scene's caption words to the real narration with faster-whisper.

Whisper hears where the speech actually is (pauses included); the script's own words are
then laid onto that timeline by character position, so captions spell the script exactly
but move with the voice. Overwrites captions/words_<id>.json (what build.py reads).

Usage: python -I align_captions.py PROJECT_DIR   (a Python with faster-whisper installed)
"""
import bisect
import json
import sys
import time
from pathlib import Path

from faster_whisper import WhisperModel

proj = Path(sys.argv[1])
scenes = json.loads((proj / "scenes.json").read_text())["scenes"]
model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)

for s in scenes:
    mp3 = proj / "audio" / "scenes" / f"{s['id']}_{s['slug']}.mp3"
    t0 = time.time()
    segments, _ = model.transcribe(str(mp3), language="hi", word_timestamps=True,
                                   vad_filter=False, beam_size=1)
    heard = [w for seg in segments for w in (seg.words or []) if w.word.strip()]
    if not heard:
        print(f"{s['id']}: nothing heard, keeping old timing")
        continue
    # whisper timeline: cumulative character fraction -> time
    lens = [max(1, len(w.word.strip())) for w in heard]
    total = sum(lens)
    fracs, times, acc = [0.0], [heard[0].start], 0
    for w, n in zip(heard, lens):
        acc += n
        fracs.append(acc / total)
        times.append(w.end)

    def at(f: float) -> float:
        i = min(max(bisect.bisect_left(fracs, f), 1), len(fracs) - 1)
        f0, f1, t_0, t_1 = fracs[i - 1], fracs[i], times[i - 1], times[i]
        return t_0 + (t_1 - t_0) * ((f - f0) / (f1 - f0) if f1 > f0 else 0)

    words = s["text"].split()
    wl = [len(w) + 1 for w in words]
    wt, pos, out = sum(wl), 0, []
    for w, n in zip(words, wl):
        start, end = at(pos / wt), at((pos + n) / wt)
        out.append({"w": w, "s": round(start, 3), "e": round(max(start + 0.05, end - 0.04), 3)})
        pos += n
    (proj / "captions" / f"words_{s['id']}.json").write_text(json.dumps(out, ensure_ascii=False))
    print(f"{s['id']}: {len(heard)} heard words -> {len(words)} script words "
          f"({heard[0].start:.2f}-{heard[-1].end:.2f}s) in {time.time() - t0:.0f}s", flush=True)
print("done")
