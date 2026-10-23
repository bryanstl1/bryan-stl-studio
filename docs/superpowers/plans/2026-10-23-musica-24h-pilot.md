# Music 24h Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a reviewable 15-second animated vertical pilot in the existing BRYAN.STL STUDIO repository.

**Architecture:** A deterministic Python renderer draws three animated scenes and synthesizes an original soundscape. FFmpeg encodes frames, mixes provisional narration, and exports MP4. The former renderer is untouched.

**Tech Stack:** Python, NumPy, Pillow, FFmpeg.

**Spec:** `productions/musica-24h/GUION-TECNICO.md` and `productions/musica-24h/METODO-Y-DIRECCION.md`.

## Global Constraints

- 15 seconds, 30 fps, vertical 1080 × 1920 delivery; render may use smaller internal preview resolution but must be labeled.
- No external paid services or borrowed audio.
- Each scene must visibly change inside the shot; do not create a photo slideshow.
- Preserve existing scripts and history.

## Review Focus

- The cut from music to ambience must be audible and clean.
- Motion and captions must remain visible on a phone.
- Encoding metadata must reflect actual resolution and codecs.
- Narration quality must be identified honestly as provisional if locally synthesized.
- Build must not claim Blender or native 1080p shading if unavailable.

### Task 1: Deterministic animation and soundscape

**Files:** Create `src/music_24h_pilot.py`; test `tests/test_music_24h_pilot.py`.

**Interfaces:** `render_frame(t: float, w: int, h: int) -> PIL.Image`, `audio_samples(start: float, duration: float) -> numpy.ndarray`; constants `FPS=30`, `DURATION=15`.

- [x] Write and run failing contract tests for scene motion, sound cut and duration.
- [ ] Implement three animated scenes and original soundscape.
- [ ] Run targeted tests and full repository suite.

### Task 2: Export and inspect

**Files:** Modify `src/music_24h_pilot.py`; create output artifacts in ignored `output/`.

**Interfaces:** CLI `python src/music_24h_pilot.py --render` exports an MP4 and contact sheet.

- [ ] Encode frame stream, soundscape and provisional narration.
- [ ] Check MP4 with `ffprobe`, inspect contact sheet and several frame samples.
- [ ] Document any gaps between prototype and final quality.
