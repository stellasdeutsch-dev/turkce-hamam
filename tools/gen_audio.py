#!/usr/bin/env python3
"""Generate Turkish mp3s (macOS voice Yelda) for every phrase in tools/phrases.json.
Sequential on purpose: parallel `say` drops files. Existing files are skipped.
To use a real voice, record an mp3 with the same file name and put it in assets/audio."""
import os, re, json, subprocess, tempfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def slug(t):
    m = {'ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u','â':'a','î':'i','û':'u'}
    t = ''.join(m.get(c, c) for c in t.lower())
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:60]
out = os.path.join(R, 'assets/audio'); os.makedirs(out, exist_ok=True)
seen, fail = set(), []
for ph in json.load(open(os.path.join(R, 'tools/phrases.json'))):
    s = slug(ph)
    if s in seen: continue
    seen.add(s); f = os.path.join(out, s + '.mp3')
    if os.path.exists(f) and os.path.getsize(f) > 1000: continue
    with tempfile.TemporaryDirectory() as td:
        a = os.path.join(td, 'x.aiff')
        subprocess.run(['say', '-v', 'Yelda', '-r', '165', '-o', a, ph], check=False)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a, '-ac', '1', '-ar', '22050', '-b:a', '48k', f], check=False)
    if not (os.path.exists(f) and os.path.getsize(f) > 1000): fail.append(ph)
print('files:', len(os.listdir(out)), 'failed:', fail)
