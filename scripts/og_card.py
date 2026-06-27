# -*- coding: utf-8 -*-
"""
Generate Telegram/Open-Graph price-bar cards for METAL instruments, matching the
EGX-stock card design (og/<slug>.png, 1200x630). Data is read from the single
source assets/data.js (the METALS object), so adding a new metal there and running
this script is all that is needed:

    python3 scripts/og_card.py            # regenerate og/<slug>.png for every metal

Fonts (IBM Plex Mono + IBM Plex Sans Arabic, which also carries Latin glyphs) are
fetched from the google/fonts mirror into a local cache on first run.
"""
import os, sys, re, json, tempfile, subprocess, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data.js")
OUT  = os.path.join(ROOT, "og")

from PIL import Image, ImageDraw, ImageFont

BG=(28,58,54); GOLD=(192,164,95); BRASS=(137,111,54); WHITE=(255,255,255); SAGE=(159,176,172)
# Canonical sizes, fitted once to og/phdc.png so metal cards sit consistently beside the EGX set.
SZ=dict(word=35, head=59, tick=20, sub=20, med=22, pct=15, lat=15, leg=21, cap=17)

FD = os.path.join(tempfile.gettempdir(), "testahil_og_fonts")
_BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl"
_FONTS = {
    "IBMPlexMono-Medium.ttf":      f"{_BASE}/ibmplexmono/IBMPlexMono-Medium.ttf",
    "IBMPlexMono-Bold.ttf":        f"{_BASE}/ibmplexmono/IBMPlexMono-Bold.ttf",
    "IBMPlexSansArabic-Bold.ttf":  f"{_BASE}/ibmplexsansarabic/IBMPlexSansArabic-Bold.ttf",
    "IBMPlexSansArabic-Regular.ttf": f"{_BASE}/ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf",
}
MONO="IBMPlexMono-Medium.ttf"; MONOB="IBMPlexMono-Bold.ttf"
SB="IBMPlexSansArabic-Bold.ttf"; SR="IBMPlexSansArabic-Regular.ttf"

def ensure_fonts():
    os.makedirs(FD, exist_ok=True)
    for fn, url in _FONTS.items():
        p = os.path.join(FD, fn)
        if os.path.exists(p) and os.path.getsize(p) > 10000:
            continue
        urllib.request.urlretrieve(url, p)
        if os.path.getsize(p) < 10000:
            raise RuntimeError(f"font download failed: {fn}")

def F(file, size):
    return ImageFont.truetype(os.path.join(FD, file), size, layout_engine=ImageFont.Layout.RAQM)

def fmt_metal(v):
    return f"{round(v):,}"

def card(out, headline, ticker, unit, p5, p25, p50, p75, p95, latest, spotDate, fmt=fmt_metal):
    S=2; W,H=1200*S,630*S
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    f=lambda file,s: F(file, s*S)
    def t(x,y,s,fnt,fill,a="lm"): d.text((x*S,y*S), s, font=fnt, fill=fill, anchor=a)
    L=70
    t(L,76,"testahil",f(MONO,SZ["word"]),WHITE)
    ww=d.textlength("testahil",font=f(MONO,SZ["word"]))/S
    t(L+ww+20,75,"?",f(MONOB,SZ["word"]),GOLD)
    t(L,108,"is it worth it?",f(SR,18),SAGE)
    t(L,190,headline,f(SB,SZ["head"]),WHITE)
    t(L,242,ticker,f(MONO,SZ["tick"]),GOLD)
    t(L,286,f"3-month price distribution \u00b7 50,000 simulations \u00b7 {unit}",f(SR,SZ["sub"]),SAGE)
    x0,x1=128,1070; top,bot=360,393; cy=(top+bot)//2; rng=p95-p5
    pos=lambda v: x0+(v-p5)/rng*(x1-x0)
    p25x,p75x,medx,latx=pos(p25),pos(p75),pos(p50),pos(latest); r=(bot-top)/2
    d.rounded_rectangle([x0*S,top*S,x1*S,bot*S],radius=r*S,fill=GOLD)
    d.rectangle([p25x*S,top*S,p75x*S,bot*S],fill=BRASS)
    d.line([(medx*S,top*S),(medx*S,bot*S)],fill=WHITE,width=3*S)
    dr=r-2; d.ellipse([(latx-dr)*S,(cy-dr)*S,(latx+dr)*S,(cy+dr)*S],fill=WHITE)
    t(x0-14,cy,fmt(p5),f(MONO,SZ["pct"]),GOLD,"rm")
    t(x1+14,cy,fmt(p95),f(MONO,SZ["pct"]),GOLD,"lm")
    t(p25x,342,fmt(p25),f(MONO,SZ["pct"]),GOLD,"mm")
    t(p75x,342,fmt(p75),f(MONO,SZ["pct"]),GOLD,"mm")
    t(medx,330,f"median {fmt(p50)}",f(MONO,SZ["med"]),WHITE,"mm")
    m=re.search(r"(\d{1,2}\s+[A-Za-z]{3})",spotDate or ""); ds=m.group(1) if m else (spotDate or "")
    t(latx,431,f"{ds} \u00b7 {fmt(latest)} (latest)",f(MONO,SZ["lat"]),WHITE,"mm")
    t(L,490,"Each bar = the 5th\u201395th percentile of 50,000 simulated 3-month prices.",f(SB,SZ["leg"]),WHITE)
    t(L,519,"Darker middle = central 50% \u00b7 white line = median \u00b7 white dot = latest price.",f(SR,SZ["cap"]),SAGE)
    d.line([(L*S,558*S),((1200-L)*S,558*S)],fill=SAGE,width=1*S)
    t(L,590,"testahil.com",f(MONOB,SZ["lat"]),WHITE)
    t(1200-L,590,"Educational analysis \u00b7 not investment advice",f(SR,SZ["cap"]),SAGE,"rm")
    im.resize((1200,630),Image.LANCZOS).save(out)
    print("wrote", os.path.relpath(out, ROOT))

def load_metals():
    js = 'const fs=require("fs");eval(fs.readFileSync(process.argv[1],"utf8")+"\\n;process.stdout.write(JSON.stringify(typeof METALS!==\\"undefined\\"?METALS:{}))");'
    out = subprocess.check_output(["node","-e",js,DATA]).decode("utf-8")
    return json.loads(out)

def main():
    ensure_fonts()
    metals = load_metals()
    if not metals:
        print("no METALS found in data.js"); return
    os.makedirs(OUT, exist_ok=True)
    for key, m in metals.items():
        t60 = (m.get("dist") or {}).get("t60") or {}
        slug = str(m.get("slug") or key).lower()
        card(os.path.join(OUT, f"{slug}.png"),
             headline=m.get("name") or key,
             ticker=m.get("code") or key,
             unit=m.get("ccy") or "USD",
             p5=t60["p5"], p25=t60["p25"], p50=t60["p50"], p75=t60["p75"], p95=t60["p95"],
             latest=m.get("spot"), spotDate=m.get("spotDate") or "")

if __name__ == "__main__":
    main()
