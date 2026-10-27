"""Generate the profile's self-contained SVG; requires fonttools (development only).
Usage: python scripts/build-banner.py /path/to/font-directory
The directory must contain JetBrainsMono.ttf and Fraunces.ttf.
"""
from pathlib import Path
import sys
from html import escape
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

fonts=Path(sys.argv[1]); root=Path(__file__).resolve().parents[1]
mono=instantiateVariableFont(TTFont(fonts/'JetBrainsMono.ttf'),{'wght':400}); serif=instantiateVariableFont(TTFont(fonts/'Fraunces.ttf'),{'wght':400,'opsz':48,'SOFT':0,'WONK':1})
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="650" viewBox="0 0 920 650" role="img" aria-labelledby="title description"><title id="title">ctrlnika: Different lines. Same curiosity.</title><desc id="description">Nika Jahankhah. Iranian and Pakistani roots. Born and raised in London. Interests: art, music, psychology, computer science and neurotech. Piano and violin. Building PERSAHOLIC. Explore widely. Specialise deeply. BSc (Hons) Computer Science at City St George’s, University of London.</desc><rect x=".5" y=".5" width="919" height="649" rx="9" fill="#20182f" stroke="#49385e"/>']
def path(d,c,width=1):parts.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{width}"/>')
def text(s,x,y,size=13,color='#f0ebfb',font=mono):
    glyphs=font.getGlyphSet(); cmap=font.getBestCmap(); scale=size/font['head'].unitsPerEm; ds=[]
    for ch in s:
        name=cmap.get(ord(ch),'space'); pen=SVGPathPen(glyphs);glyphs[name].draw(TransformPen(pen,(scale,0,0,-scale,x,y)));ds.append(pen.getCommands());x+=font['hmtx'][name][0]*scale
    parts.append(f'<path fill="{color}" d="'+''.join(ds)+'"/>');return x
path('M0 44H920','#49385e')
for x,c in [(26,'#f18a57'),(41,'#bca4f4'),(56,'#76628f')]:parts.append(f'<circle cx="{x}" cy="22" r="4" fill="{c}"/>')
text('nika@london: ~ / connections',80,26,11,'#c8b7e5');text('main',849,26,10,'#a999bc')
text('>',32,84,14,'#f18a57');text('whoami',55,84,12,'#c8b7e5')
x=text('ctrl',32,162,66);x=text('nika',x,162,66,'#c6aff4');text('_',x,162,66,'#f18a57')
text('Different lines. Same curiosity.',32,207,29,'#f0ebfb',serif)
path('M32 239H888','#49385e');text('about_nika.py',32,262,10,'#a999bc');text('PYTHON',847,262,10,'#a999bc')
lines=[('name','"Nika Jahankhah"'),('username','"ctrlnika"'),('roots','("Iranian", "Pakistani")'),('home','"London, born and raised"'),('university','"City St George’s, University of London"'),('degree','"BSc (Hons) Computer Science"'),('interests','['),(None,'    "art", "music", "psychology",'),(None,'    "computer science", "neurotech",'),(None,']'),('instruments','["piano", "violin"]'),('building','"PERSAHOLIC"'),('approach','"Explore widely. Specialise deeply."')]
import tokenize,io
for i,(name,value) in enumerate(lines):
    y=294+i*24;x=32
    if name:x=text(name,x,y,13,'#f18a57');x=text(' = ',x,y)
    # Tokenise each value, preserving string and punctuation colours.
    import re
    for token in re.findall(r'"[^\"]*"|[^\"]+',value):x=text(token,x,y,13,'#c6aff4' if token.startswith('"') else '#f0ebfb')
path('M32 610H888','#49385e');text('LONDON, BORN & RAISED',32,634,9,'#c6b9d7');parts.append('<circle cx="757" cy="631" r="3" fill="#f18a57"/>');text('STILL EXPLORING',768,634,8,'#c6b9d7')
parts.append('</svg>');(root/'assets/london-terminal.svg').write_text(''.join(parts))
