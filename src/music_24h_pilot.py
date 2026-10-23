"""Animated BRYAN.STL pilot. No still-image slideshow or third-party media."""
from __future__ import annotations

import argparse
import math
import os
import subprocess
import wave
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS = 30
DURATION = 15
W, H = 540, 960
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "musica-24h"
VIOLET = (150, 105, 255)
CYAN = (63, 207, 247)
WHITE = (243, 243, 249)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def smooth(a, b, x):
    q = max(0.0, min(1.0, (x-a)/(b-a)))
    return q*q*(3-2*q)


@lru_cache(maxsize=1)
def background():
    y, x = np.ogrid[:H, :W]
    radial = np.clip(1 - ((x-W*.5)/(W*.8))**2 - ((y-H*.46)/(H*.8))**2, 0, 1)
    arr = np.empty((H, W, 3), dtype=np.uint8)
    arr[:, :, 0] = 5 + radial*9
    arr[:, :, 1] = 7 + radial*8
    arr[:, :, 2] = 17 + radial*20
    return Image.fromarray(arr, "RGB")


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def centered(draw, text, y, size=24, fill=WHITE, bold=False):
    f = font(size, bold)
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((W-(box[2]-box[0]))/2, y), text, font=f, fill=fill)


def label(draw, t, lines):
    """Short, time-directed editorial captions within social safe area."""
    for i, (line, bold) in enumerate(lines):
        centered(draw, line, 126+i*40, 25 if bold else 23,
                 WHITE if bold else (166, 169, 189), bold)


def header(draw, num, title):
    draw.text((44, 58), "B R Y A N  /  S T L", font=font(12, True), fill=(181, 175, 218))
    draw.rounded_rectangle((43, 88, 112, 90), radius=1, fill=VIOLET)
    draw.text((457, 57), num, font=font(15), fill=(142, 144, 169))
    draw.text((42, 885), "@bryan.stl", font=font(15), fill=(192, 187, 211))
    draw.text((42, 912), title, font=font(10), fill=(103, 105, 136))


def particles(draw, t, n=50, muted=False):
    for i in range(n):
        x = 30 + (i*97.71 + 9*math.sin(t*.8+i*.34)) % 480
        y = 245 + (i*199.13 + (0 if muted else t*17)) % 570
        r = 1 if i % 4 else 2
        c = (55, 55, 88) if muted else (79, 54, 135)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=c)


def speaker(im, t):
    d = ImageDraw.Draw(im)
    header(d, "01 / 03", "UNA PREGUNTA")
    label(d, t, [("¿Y si la música", False), ("desapareciera", True), ("durante 24 horas?", False)])
    active = t < 3.15
    beat = max(0.0, 1-(t % .52)/.52)**3 if active else 0
    pulse = 1 + .04*beat + .025*math.sin(2*math.pi*5*t)*active
    cx, cy, rx, ry = 270, 508, 185*pulse, 216*pulse
    glow = Image.new("RGBA", (W, H))
    g = ImageDraw.Draw(glow)
    for j in range(7, 0, -1):
        a = 10+j*9 if active else 7
        rr = rx + j*16
        g.ellipse((cx-rr, cy-rr*1.12, cx+rr, cy+rr*1.12), outline=(*VIOLET, a), width=3)
    glow = glow.filter(ImageFilter.GaussianBlur(15))
    im.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(im)
    # The projected ellipses form a deep, cylindrical speaker rather than a flat icon.
    for depth in range(17, -1, -1):
        off = depth*1.2
        shade = 17 + (17-depth)*2
        d.ellipse((cx-rx+off, cy-ry+off*.5, cx+rx+off, cy+ry+off*.5),
                  fill=(shade, shade+2, shade+13))
    d.ellipse((cx-rx, cy-ry, cx+rx, cy+ry), outline=(104, 98, 132), width=4)
    for k in range(5):
        rr = rx*(.89-k*.105)
        color = (28+k*3, 26+k*3, 48+k*5)
        d.ellipse((cx-rr, cy-rr*1.16, cx+rr, cy+rr*1.16), fill=color,
                  outline=(72+k*6, 59+k*5, 104+k*5), width=3)
    rr = 83*pulse
    d.ellipse((cx-rr, cy-rr*1.16, cx+rr, cy+rr*1.16), fill=(20, 22, 39),
              outline=VIOLET if active else (73, 76, 91), width=5)
    d.arc((cx-rr+9, cy-rr*1.16+9, cx+rr-9, cy+rr*1.16-9), 192, 330,
          fill=(213, 189, 255) if active else (77, 83, 101), width=4)
    for phase in (0, 1, 2):
        r = 228 + phase*28 + 10*math.sin(t*3)
        c = VIOLET if active else (53, 57, 76)
        d.arc((cx-r, cy-r*1.12, cx+r, cy+r*1.12), 20, 160, fill=c, width=2)
    # Energy line has a coherent travel direction and collapses at the cut.
    amp = 35 * (1-smooth(3.07, 3.18, t))
    pts = [(x, 810 + amp*math.sin((x-t*190)*.062)*(.35+.65*math.sin(x*.023)**2))
           for x in range(40, 500, 3)]
    d.line(pts, fill=CYAN if active else (80, 82, 100), width=3, joint="curve")
    d.text((42, 843), "SEÑAL", font=font(12, True), fill=(108, 109, 134))
    d.text((443, 843), "00:03", font=font(12), fill=(108, 109, 134))
    particles(d, t, 18, muted=not active)


def phone(im, t):
    d = ImageDraw.Draw(im)
    header(d, "02 / 03", "UNA CANCIÓN QUE NO SUENA")
    if t < 5.2:
        label(d, t, [("Tu teléfono", False), ("funciona.", True)])
    elif t < 7.25:
        label(d, t, [("Le das play.", True), ("La canción avanza…", False)])
    else:
        label(d, t, [("pero no suena.", True)])
    local = t-3.45
    tilt = 5*math.sin(local*.7)
    shift = 9*math.sin(local*.9)
    px, py = 270+shift, 498
    glow = Image.new("RGBA", (W, H))
    g = ImageDraw.Draw(glow)
    g.rounded_rectangle((px-173, py-285, px+173, py+280), radius=52, outline=(*VIOLET, 130), width=7)
    glow = glow.filter(ImageFilter.GaussianBlur(25))
    im.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(im)
    # Offset hull, specular edging and parallax elements give the interface depth.
    d.rounded_rectangle((px-158+tilt, py-272, px+160+tilt, py+287), radius=42,
                        fill=(29, 31, 55), outline=(79, 76, 104), width=4)
    d.rounded_rectangle((px-165, py-283, px+150, py+273), radius=41,
                        fill=(9, 12, 27), outline=(148, 142, 184), width=5)
    d.rounded_rectangle((px-151, py-266, px+136, py+257), radius=32, fill=(14, 18, 39))
    d.rounded_rectangle((px-45, py-262, px+26, py-246), radius=8, fill=(2, 3, 9))
    # Album artwork is code-drawn, not a static image pasted over the phone.
    ax, ay = px-111, py-191
    d.rounded_rectangle((ax, ay, ax+205, ay+203), radius=20, fill=(33, 25, 63))
    for j in range(36):
        r = (j*27 + local*27) % 220
        x = ax+104 + r*math.cos(j*2.4)*.48
        y = ay+100 + r*math.sin(j*2.4)*.48
        d.ellipse((x-2, y-2, x+2, y+2), fill=(102+j*2, 78+j, 166+j))
    d.ellipse((ax+65, ay+57, ax+145, ay+137), outline=(192, 160, 245), width=5)
    d.text((ax, ay+225), "24 HORAS", font=font(20, True), fill=WHITE)
    d.text((ax, ay+255), "Sin música", font=font(15), fill=(147, 144, 173))
    progress = max(0, min(1, (t-5.75)/5.5))
    d.rounded_rectangle((ax, ay+314, ax+205, ay+319), radius=2, fill=(66, 68, 88))
    d.rounded_rectangle((ax, ay+314, ax+max(3, 205*progress), ay+319), radius=2, fill=CYAN)
    d.text((ax, ay+330), f"0:{int(progress*23):02d}", font=font(12), fill=(161, 163, 182))
    playing = t >= 5.75
    if playing:
        d.rounded_rectangle((px-11, py+179, px-4, py+213), radius=2, fill=WHITE)
        d.rounded_rectangle((px+5, py+179, px+12, py+213), radius=2, fill=WHITE)
    else:
        d.polygon([(px-8, py+175), (px+19, py+195), (px-8, py+215)], fill=WHITE)
    # Animated cursor/fingertip approaches and taps the play button.
    if 5.2 <= t <= 6.1:
        u = smooth(5.2, 5.75, t)
        fx = 392-(392-px)*u
        fy = 825-(825-(py+201))*u
        d.ellipse((fx-27, fy-27, fx+27, fy+27), fill=(218, 177, 155), outline=(255, 214, 189), width=3)
        if t >= 5.7:
            rr = 12+80*smooth(5.7, 6.05, t)
            d.ellipse((px-rr, py+197-rr, px+rr, py+197+rr), outline=(80, 200, 235), width=2)
    if t >= 7.2:
        d.rounded_rectangle((61, 789, 479, 849), radius=17, fill=(24, 26, 49), outline=(72, 66, 100))
        centered(d, "LA PISTA AVANZA  ·  0 AUDIO", 811, 14, (172, 160, 210), True)


def club(im, t):
    d = ImageDraw.Draw(im)
    header(d, "03 / 03", "EL DROP QUE NUNCA LLEGA")
    if t < 11.2:
        label(d, t, [("En un club,", False), ("siguen las luces…", True)])
    elif t < 13.0:
        label(d, t, [("y las voces.", False)])
    else:
        label(d, t, [("Falta el beat.", True)])
    phase = t-8.45
    van_x, van_y = 270+18*math.sin(phase*.45), 459
    d.polygon([(0, 830), (W, 830), (350, van_y), (190, van_y)], fill=(18, 19, 34))
    for i in range(7):
        q = i/6
        y = van_y + (850-van_y)*q*q
        d.line((0, y, W, y), fill=(42+int(q*18), 36+int(q*10), 69+int(q*20)), width=2)
    for x in (-320, -200, -100, 0, 100, 200, 320):
        d.line((van_x, van_y, van_x+x, 835), fill=(40, 35, 69), width=2)
    # Moving beams travel through space; their source positions are stable.
    beams = Image.new("RGBA", (W, H))
    g = ImageDraw.Draw(beams)
    for k, ox in enumerate((83, 172, 365, 457)):
        sweep = math.sin(phase*1.27 + k*1.36)
        target = van_x + sweep*270
        g.polygon([(ox-5, 261), (ox+5, 261), (target+112, 752), (target-112, 752)],
                  fill=(*((85, 70, 165) if k%2 else (40, 125, 182)), 34))
    beams = beams.filter(ImageFilter.GaussianBlur(13))
    im.paste(beams, (0, 0), beams)
    d = ImageDraw.Draw(im)
    for k, ox in enumerate((83, 172, 365, 457)):
        d.ellipse((ox-8, 253, ox+8, 269), fill=CYAN if k%2 else VIOLET)
    # Geometric stage architecture and fixed silent cabinets.
    d.rectangle((139, 347, 401, 520), fill=(20, 18, 38), outline=(80, 75, 111), width=3)
    d.rectangle((172, 375, 368, 470), fill=(21, 22, 52))
    for i in range(12):
        h = 8 + 18*(1+math.sin(phase*2 + i*.6))/2
        d.rectangle((184+i*15, 433-h, 192+i*15, 435), fill=(90, 75, 159))
    for sx in (93, 408):
        d.rounded_rectangle((sx, 387, sx+38, 541), radius=4, fill=(19, 20, 32), outline=(83, 81, 103), width=3)
        for sy, rr in ((420, 13), (497, 20)):
            d.ellipse((sx+19-rr, sy-rr, sx+19+rr, sy+rr), outline=(73, 75, 93), width=3)
    # Individually animated faceless silhouettes, not still cutouts.
    for i in range(13):
        x = 17 + i*43 + 4*math.sin(phase*1.8+i)
        depth = .77 + .23*((i*5)%8)/8
        y = 653 + 23*math.sin(phase*1.6+i*.73)
        r = 13*depth
        d.ellipse((x-r, y-r-49, x+r, y+r-49), fill=(3, 5, 13))
        d.ellipse((x-24*depth, y-49, x+24*depth, y+68), fill=(3, 5, 13))
        if i in (2, 6, 10):
            arm = 20*math.sin(phase*1.5+i)
            d.line((x+14, y-20, x+39, y-50-arm), fill=(4, 5, 14), width=10)
    # Final missing beat becomes a quiet empty circle.
    if t >= 12.85:
        k = smooth(12.85, 13.35, t)
        d.ellipse((270-54*k, 776-54*k, 270+54*k, 776+54*k), outline=(90, 83, 137), width=3)
        d.line((243, 776, 297, 776), fill=(192, 184, 219), width=3)
    particles(d, t, 13, muted=True)


def render_frame(t: float, w: int = W, h: int = H) -> Image.Image:
    im = background().copy()
    if t < 3.45:
        speaker(im, t)
    elif t < 8.45:
        phone(im, t)
    else:
        club(im, t)
    return im if (w, h) == (W, H) else im.resize((w, h), Image.Resampling.LANCZOS)


def audio_samples(start: float, duration: float, sr: int = 48000) -> np.ndarray:
    t = start + np.arange(round(duration*sr))/sr
    p = np.mod(t, .48)
    kick = np.sin(2*np.pi*(54*p - 19*p*p))*np.exp(-30*p)
    hat = np.sin(2*np.pi*5000*t)*np.exp(-70*np.mod(t, .24))
    lead = np.sin(2*np.pi*110*t) * (.5 + .5*np.sin(2*np.pi*.34*t))
    pre = (.40*kick + .032*hat + .065*lead)*(t < 3.15)
    ambience = (.0025*np.sin(2*np.pi*73*t) + .0014*np.sin(2*np.pi*127.3*t))*(t >= 3.15)
    click = .075*np.sin(2*np.pi*950*t)*np.exp(-85*np.maximum(0, t-5.75))*(t >= 5.75)
    return np.asarray(pre + ambience + click, dtype=np.float32)


def write_wav(path: Path, arr: np.ndarray, sr=48000):
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes((np.clip(arr, -.99, .99)*32767).astype("<i2").tobytes())


def provisional_voice(out: Path) -> Path:
    """Local no-cost scratch narration; English flite phonemes are not a final LATAM voice."""
    sr = 48000
    result = np.zeros(DURATION*sr, np.float32)
    parts = [
        (0.12, 3.15, "Y si la musica desapareciera durante veinticuatro horas?"),
        (3.58, 4.72, "Tu telefono funciona. Le das play. La cancion avanza, pero no suena."),
        (8.65, 5.50, "En un club, siguen las luces y las voces. Falta el beat."),
    ]
    for i, (start, target, phrase) in enumerate(parts):
        source = out/f"voice-part-{i}.txt"
        source.write_text(phrase, encoding="utf-8")
        wav = out/f"voice-part-{i}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
                        f"flite=textfile={source}:voice=slt", "-ar", str(sr),
                        "-ac", "1", str(wav)], check=True)
        with wave.open(str(wav), "rb") as f:
            samples = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(np.float32)/32768
        # This is a temp guide track: modest speed changes keep each clause in its scene.
        length = int(target*sr)
        indices = np.linspace(0, len(samples)-1, length)
        fitted = np.interp(indices, np.arange(len(samples)), samples)
        edge = min(700, length//5)
        fitted[:edge] *= np.linspace(0, 1, edge)
        fitted[-edge:] *= np.linspace(1, 0, edge)
        pos = int(start*sr)
        result[pos:pos+length] += fitted.astype(np.float32)*.72
    path = out/"voice-guide.wav"
    write_wav(path, result, sr)
    return path


def render(out=OUT):
    out.mkdir(parents=True, exist_ok=True)
    soundtrack = audio_samples(0, DURATION)
    guide = provisional_voice(out)
    with wave.open(str(guide), "rb") as f:
        narration = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(np.float32)/32768
    write_wav(out/"soundscape.wav", np.clip(soundtrack*.48 + narration, -.95, .95))
    raw = out/"animation-540x960.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-i", str(out/"soundscape.wav"),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "ultrafast",
           "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
           "-t", str(DURATION), "-movflags", "+faststart", str(raw)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    stills = []
    try:
        for i in range(FPS*DURATION):
            im = render_frame(i/FPS)
            if i in (0, 55, 95, 150, 195, 255, 330, 405):
                stills.append(im.resize((270, 480)))
            p.stdin.write(im.tobytes())
        p.stdin.close()
    except BrokenPipeError as exc:
        raise RuntimeError("FFmpeg stopped before receiving all frames") from exc
    if p.wait():
        raise RuntimeError("FFmpeg encode failed")
    sheet = Image.new("RGB", (1080, 960), (0, 0, 0))
    for i, im in enumerate(stills):
        sheet.paste(im, (i%4*270, i//4*480))
    sheet.save(out/"contact-sheet.jpg", quality=92)
    return raw


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    if args.render:
        print(render())
