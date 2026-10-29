# बेलघाटी हॉल्ट के 7 नियम — handoff notes (2026-10-28)

Original Hindi railway horror story, ~20 min, 77 scenes, 8 chapters. Built on the
`youtube-longform` pipeline (copied from projects/night-shift-rules).
Edit the story in `make_story.py`, then `python3 make_story.py` rewrites scenes.json + SCRIPT.md.

## Status
- 2026-10-29: owner found formal Hindi "boring, 80's" → narration rewritten in modern Hinglish
  (Devanagari, English words transliterated), Roman-Hinglish title/chapters/description,
  "RULE N" cards (make_cards.py mixes Noto Serif + Noto Serif Devanagari per run).
- Voice: Indic Parler-TTS works (HF access granted). Owner wants a heavy, soft voice; testing
  Rohit vs Aman with a casual "telling friends a scary story" description. ~8x realtime on CPU.
- Owner rejected the cartoon look: STYLE is now realistic digital painting at a railway station
  (old cartoon stills kept in images_cartoon/). Narration no longer *says* ठक/टप/खट — scenes carry
  an `sfx` list mixed at build time. Voice: Aman. Owner wants ~6 real motion clips at the big
  scares from their ElevenLabs credits (check one clip's cost first; free plan may be non-commercial).
- Background tasks cap at 2 h: images run in two chunks (flux_batch.py takes asset paths).
- 122 FLUX stills + 11 Hindi text cards (`CARD:` shots, rendered locally, never by an image model).

## Free production path (owner has no card: Modal is out)
- **Stills:** FLUX.2 klein-4B on CPU in a scratch venv (diffusers 0.41, transformers 5.17,
  torch 2.6 from PyPI; download.pytorch.org and jsdelivr are blocked by the proxy).
  Encode prompt → free text encoder → load transformer (15 GB RAM won't hold both).
  1024x576, 4 steps ≈ 85 s/image; Ken Burns in build.py upscales. Weights ~16 GB: watch disk.
  Check every still for gibberish lettering despite "no text"; regenerate only that one.
- **Hindi cards:** `apt-get install fonts-noto-core` → NotoSerifDevanagari-Bold.ttf; PIL has
  raqm, so conjuncts/matras shape correctly (tested).
- **Voice:** owner rejected Kokoro Hindi (hm_omega / hm_psi). Use AI4Bharat Indic Parler-TTS
  (Apache-2.0, gated "auto" → needs `HF_TOKEN` env + terms accepted). Test 3 scenes first,
  send the owner a sample before the full run. Numbers are spelled out in the narration.
- **Music:** acemusic network secret was not being injected (401 "Missing authentication
  token"); owner may leave it empty. Fallback: synthesize a dark ambient drone locally.
- `config.json` still has the English project's voice/captions settings: set captions
  `language` to `hi` and the voice note to the Hindi TTS before building.

## Research behind the story (vidIQ, Oct 2026)
Railway/station night stories are the fastest-breaking Hindi horror setting (e.g. "वीरानगढ़
स्टेशन का भूतिया वड़ा पाव वाला" 66x, "The Last Train" 99x). Plain everyday Hindi, short
dialogue, no intro, sticky last line. Don't title fiction as "सच्ची घटना".
