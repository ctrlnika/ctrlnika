"""Build option 03's self-contained README artwork.
Usage: python scripts/build-sections.py /path/to/font-directory
Requires fonttools; fonts: Fraunces.ttf, HankenGrotesk.ttf, JetBrainsMono.ttf.
Text is outlined because GitHub image rendering cannot load web fonts.
Edit the map in assets/connections-source.svg; retain its SVG text for editing.
"""
from pathlib import Path
from html import escape
import sys, xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont
root=Path(__file__).resolve().parents[1];fontdir=Path(sys.argv[1])
fonts={}
for name in ['Fraunces','HankenGrotesk','JetBrainsMono']:
 f=TTFont(fontdir/(name+'.ttf'))
 axes={'wght':400}
 if name=='Fraunces':axes.update(opsz=48,SOFT=0,WONK=1)
 fonts[name]=instantiateVariableFont(f,axes,inplace=False)
C='#21182f'; L='#77539c'; O='#ed8650'
def text(s,x,y,size=18,color=C,font='HankenGrotesk',anchor='start'):
 f=fonts[font];g=f.getGlyphSet();cm=f.getBestCmap();sc=size/f['head'].unitsPerEm
 width=sum(f['hmtx'][cm.get(ord(ch),'space')][0] for ch in s)*sc
 if anchor=='middle':x-=width/2
 if anchor=='end':x-=width
 ds=[]
 for ch in s:
  name=cm.get(ord(ch),'space');pen=SVGPathPen(g);g[name].draw(TransformPen(pen,(sc,0,0,-sc,x,y)));ds.append(pen.getCommands());x+=f['hmtx'][name][0]*sc
 return '<path fill="'+color+'" d="'+''.join(ds)+'"/>'
def svg(body,w,h,title,desc):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><desc>{escape(desc)}</desc><rect width="{w}" height="{h}" fill="#fffdfa"/>'+body+'</svg>'
def heading(label,title):return text(label,0,24,12,L,'JetBrainsMono')+text(title,0,80,45,C,'Fraunces')
source=ET.fromstring((root/'assets/connections-source.svg').read_text());ns='{http://www.w3.org/2000/svg}'
for n in list(source):
 if n.tag==ns+'text':
  p=ET.fromstring(text(n.text or '',float(n.get('x')),float(n.get('y')),float(n.get('font-size','17')),n.get('fill',C),anchor=n.get('text-anchor','start')))
  i=list(source).index(n);source.remove(n);source.insert(i,p)
ET.register_namespace('','http://www.w3.org/2000/svg')
mapbody=''.join(ET.tostring(n,encoding='unicode') for n in source)
s=heading('01 / DIFFERENT LINES. SAME CURIOSITY.','A little context')
s+=text('Explore widely. Specialise deeply. Following the connections between creative practice,',0,120,19)
s+=text('computing and the questions that stay with me.',0,149,19)
s+='<rect x=".5" y="180.5" width="1119" height="659" rx="7" fill="#fffdfa" stroke="#d9cfe3"/>'
s+=text('CTRLNIKA / CONNECTIONS',24,211,12,L,'JetBrainsMono')
s+='<g transform="translate(0 228)">'+mapbody+'</g>'
for x,col,label in [(24,O,'Creative practice'),(310,'#a78ad2','Computing'),(560,'#57416f','Research & impact')]:
 s+=f'<path d="M{x} 810h30" stroke="{col}" stroke-width="5"/>'+text(label,x+42,815,13,C,'JetBrainsMono')
s+='<circle cx="910" cy="810" r="7" fill="#fffdfa" stroke="#21182f" stroke-width="2"/>'+text('Shared interests',927,815,12,C,'JetBrainsMono')
(root/'assets/connections.svg').write_text(svg(s,1120,860,'A little context — connections map','Creative practice: art, music, piano and violin, culture and memory, design, PERSAHOLIC. Computing: computer science, neurotech, bioinformatics, Neural Nets. Research and impact: psychology, research, safer AI, Parachute, civic technology, Stalled London. Interchanges: creative computing; mind and technology.'))
(root/'assets/projects-heading.svg').write_text(svg(heading('02 / SELECTED EXPLORATIONS','A few stops along the way'),1120,104,'A few stops along the way','Selected projects'))
arts=[ '<path d="M5 70H90M12 65V28H32V65M38 65V12H63V65M68 65V35H86V65M40 12L51 3L62 12M15 36H28M15 44H28M15 52H28M44 24H57M44 34H57M44 44H57M72 43H82M72 52H82M5 20H90M76 5V65M76 5L40 20"/>', '<path d="M47 66C10 76 3 42 20 32C10 9 38 2 48 16C62 0 89 13 81 32C100 47 79 73 60 65M48 16V65M20 32L34 39L26 54M48 29L67 23L75 41L60 49L68 61M34 39L48 29L60 49L48 60"/><circle cx="34" cy="39" r="3"/><circle cx="67" cy="23" r="3"/>', '<path d="M8 30C15-5 79-5 87 30M8 30Q20 20 32 30Q45 20 58 30Q74 20 87 30M32 30Q29 6 47 3Q65 8 58 30M8 30L47 70L87 30M32 30L47 70L58 30M47 70V77"/>' ]
projects=[('stalled-london','Stalled London','01 / CIVIC TECHNOLOGY',['Making London’s stalled housing','developments visible.']),('neural-nets','Neural Nets','02 / NEUROTECH',['Exploring neurotech, BCIs','and bioinformatics.']),('parachute','Parachute','03 / AI SAFETY',['An AI safety gateway.','Work in progress.'])]
for i,(slug,name,label,lines) in enumerate(projects):
 s='<rect x=".5" y=".5" width="359" height="249" rx="6" fill="#f2edf9" stroke="#ded2ec"/>'
 s+=text(label,20,29,10,L,'JetBrainsMono')+text(name,20,71,29,C,'Fraunces')
 for j,line in enumerate(lines):s+=text(line,20,104+25*j,16)
 s+='<g transform="translate(247 145)" fill="none" stroke="#77549d" stroke-width="1.3">'+arts[i]+'</g>'
 s+=text('View project',20,224,14,L)+text('→',118,224,20,O)
 (root/f'assets/{slug}.svg').write_text(svg(s,360,250,name,' '.join(lines)))
s=heading('03 / WHAT I BUILD WITH','My tech stack')
groups=[('01 / LANGUAGES','{ }',['Python','TypeScript','JavaScript','HTML','CSS','C++','Java','SQL'],'#f0e9f8'),('02 / FRAMEWORKS','<>',['React','React Native'],'#f9eee5'),('03 / TOOLS','//',['Git','VS Code','IntelliJ','Excel','Access','Microsoft 365'],'#ece6f0')]
for i,(label,mark,items,bg) in enumerate(groups):
 y=112+i*78;s+=f'<rect x="0" y="{y}" width="1120" height="66" rx="5" fill="{bg}"/>'
 s+=text(label,18,y+39,11,L,'JetBrainsMono')+text(mark,184,y+42,24,O if i==1 else L,'JetBrainsMono')
 s+=f'<path d="M232 {y+14}v38" stroke="#d4c6e2"/>'
 x=252
 for item in items:
  width=sum(fonts['HankenGrotesk']['hmtx'][fonts['HankenGrotesk'].getBestCmap().get(ord(ch),'space')][0] for ch in item)*15/fonts['HankenGrotesk']['head'].unitsPerEm+20
  s+=f'<rect x="{x}" y="{y+17}" width="{width}" height="32" rx="3" fill="#fffdfa" stroke="#ddd1e9"/>'+text(item,x+10,y+39,15)
  x+=width+8
(root/'assets/tech-stack.svg').write_text(svg(s,1120,348,'My tech stack','Languages: Python, TypeScript, JavaScript, HTML, CSS, C++, Java, SQL. Frameworks: React, React Native. Tools: Git, Visual Studio Code, IntelliJ, Excel, Access, Microsoft 365.'))
print('Built connections, project heading, three project cards and compact tech-stack rows.')
