#!/usr/bin/env python3
"""Turn the Indic Parler-TTS takes (audio/vo_wav/<id>.wav) into what build.py reads:

  audio/scenes/<id>_<slug>.mp3   loudness-matched narration (-16 LUFS, music headroom)
  vo_durations.json              real per-scene durations that anchor the timeline
  captions/words_<id>.json       word timing for captions.srt, spread over each take by
                                 character length (no Hindi forced aligner runs here)

Run from the project dir: python3 prep_audio.py
"""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).parent


def duration(path: Path) -> float:
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", str(path)])
    return float(out)


def main() -> None:
    scenes = json.loads((HERE / "scenes.json").read_text())["scenes"]
    (HERE / "audio" / "scenes").mkdir(parents=True, exist_ok=True)
    (HERE / "captions").mkdir(exist_ok=True)
    durations = {}
    for s in scenes:
        wav = HERE / "audio" / "vo_wav" / f"{s['id']}.wav"
        mp3 = HERE / "audio" / "scenes" / f"{s['id']}_{s['slug']}.mp3"
        if not wav.exists():
            print(f"missing narration: {wav.name}")
            continue
        if not mp3.exists() or mp3.stat().st_mtime < wav.stat().st_mtime:
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav),
                            "-af", "silenceremove=start_periods=1:start_threshold=-50dB,"
                                   "areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                                   "loudnorm=I=-16:TP=-1.5",
                            "-ar", "48000", "-b:a", "192k", str(mp3)], check=True)
        dur = duration(mp3)
        durations[s["id"]] = round(dur, 3)

        words = s["text"].split()
        weights = [len(w) + 1 for w in words]
        total, t, out = sum(weights), 0.0, []
        for w, wt in zip(words, weights):
            step = dur * wt / total
            out.append({"w": w, "s": round(t, 3), "e": round(t + step * 0.92, 3)})
            t += step
        (HERE / "captions" / f"words_{s['id']}.json").write_text(json.dumps(out, ensure_ascii=False))
    (HERE / "vo_durations.json").write_text(json.dumps(durations, indent=1))
    print(f"{len(durations)} scenes, {sum(durations.values()) / 60:.1f} min of narration")


if __name__ == "__main__":
    main()
