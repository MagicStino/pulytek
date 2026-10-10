#!/usr/bin/env python3
"""Draw original panel art and a 101-frame vintage VU strip from source geometry."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
ROOT=Path(__file__).resolve().parents[1]

def main():
    art=ROOT/'vst/art';art.mkdir(parents=True,exist_ok=True)
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="620" viewBox="0 0 1280 620">',
    '<defs><linearGradient id="blue" x2="0" y2="1"><stop stop-color="#285474"/><stop offset=".45" stop-color="#214865"/><stop offset="1" stop-color="#163850"/></linearGradient><radialGradient id="lamp"><stop stop-color="#d3ffc1"/><stop offset=".4" stop-color="#6ee668"/><stop offset="1" stop-color="#0d612e"/></radialGradient></defs>',
    '<rect width="1280" height="620" rx="12" fill="url(#blue)"/><rect x="18" y="10" width="1244" height="600" rx="8" fill="none" stroke="#93b2c0" stroke-opacity=".4"/>']
    for x in (30,1250):
        for y in (26,596): svg.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#9aa3a5" stroke="#152e40" stroke-width="3"/><path d="M{x-4} {y-4}l8 8" stroke="#37464e" stroke-width="2"/>')
    (ROOT/'vst/panel_side.svg').write_text(''.join(svg)+ '</svg>\n')
    for x in (470,1000): svg.append(f'<path d="M{x} 222v160" stroke="#adc0c6" opacity=".45"/>')
    for cx in (140,385,630,875,1120):
        cy=372-84
        for k in range(11):
            a=math.radians(-225+k*27); x1=cx+math.cos(a)*59;y1=cy+math.sin(a)*59;x2=cx+math.cos(a)*65;y2=cy+math.sin(a)*65
            svg.append(f'<path d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}" stroke="#eeeeda" stroke-width="1.5"/>')
    svg += ['</svg>']
    (ROOT/'vst/panel.svg').write_text(''.join(svg)+'\n')
    for on in (False,True):
        lines=['<svg xmlns="http://www.w3.org/2000/svg" width="100" height="54" viewBox="0 0 100 54">',
          '<defs><linearGradient id="rim" x2="0" y2="1"><stop stop-color="#b7b6a8"/><stop offset=".5" stop-color="#474b48"/><stop offset="1" stop-color="#8d9188"/></linearGradient><linearGradient id="face" x2="0" y2="1"><stop stop-color="'+('#e1cba0' if on else '#303332')+'"/><stop offset=".55" stop-color="'+('#cfb98d' if on else '#151918')+'"/><stop offset="1" stop-color="'+('#bba172' if on else '#080d10')+'"/></linearGradient></defs>',
          '<rect x="2" y="3" width="96" height="48" rx="8" fill="#0d2638"/>',
          '<rect x="4" y="2" width="92" height="46" rx="7" fill="url(#rim)" stroke="#12222b"/>',
          '<rect x="8" y="6" width="84" height="38" rx="5" fill="url(#face)" stroke="#030b10"/>']
        for x in range(12,91,4):
            lines.append(f'<path d="M{x} 2v3 M{x} 45v3" stroke="#222927" stroke-width="1"/>')
        for y in range(10,44,4):
            lines.append(f'<path d="M4 {y}h3 M93 {y}h3" stroke="#222927" stroke-width="1"/>')
        lines+=['<path d="M12 8h76" stroke="#fff6d7" opacity=".25"/>','</svg>']
        (art/('button_on.svg' if on else 'button_off.svg')).write_text(''.join(lines)+'\n')
    w,h,scale=252,150,3;strip=Image.new('RGB',(w,h*101))
    fontPath='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
    try: font=ImageFont.truetype(fontPath,11*scale);small=ImageFont.truetype(fontPath,8*scale);title=ImageFont.truetype(fontPath,18*scale)
    except OSError: raise SystemExit('Install fonts-dejavu-core for reproducible VU labels')
    for frame in range(101):
        im=Image.new('RGB',(w*scale,h*scale),'#12191c');d=ImageDraw.Draw(im)
        def box(coords,fill,outline=None,width=1): d.rounded_rectangle(tuple(v*scale for v in coords),radius=8*scale,fill=fill,outline=outline,width=width*scale)
        box((4,4,w-4,h-4),'#4a4e4b','#a4a294',2);box((11,11,w-11,h-11),'#efe0ab','#0d1519',3)
        cx,cy=126,140
        # Scale matches the DSP mapping: -20..+3 VU; 0 VU = -9 dBFS RMS.
        def pt(angle,r): a=math.radians(angle);return ((cx+math.cos(a)*r)*scale,(cy+math.sin(a)*r)*scale)
        for vu in range(-20,4):
            angle=-150+math.pow(10,(vu-3)/20)*120;col='#8c251b' if vu>=0 else '#292a22'
            d.line([pt(angle,91),pt(angle,100 if vu in (-20,-10,-7,-5,-3,0,1,2,3) else 95)],fill=col,width=scale)
            if vu in (-20,-10,-7,-5,-3,0,1,2,3):
                x,y=pt(angle,113);d.text((x,y),str(vu),font=small,fill=col,anchor='mm')
        d.text((126*scale,76*scale),'VU',font=title,fill='#292a22',anchor='mm');d.text((126*scale,100*scale),'0 VU = -9 dBFS RMS',font=small,fill='#594d37',anchor='mm')
        angle=-150+frame*1.2;d.line([(cx*scale,cy*scale),pt(angle,96)],fill='#702417',width=2*scale)
        d.ellipse(((cx-7)*scale,(cy-7)*scale,(cx+7)*scale,(cy+7)*scale),fill='#242726',outline='#7b796b',width=scale)
        im=im.resize((w,h),Image.Resampling.LANCZOS);strip.paste(im,(0,frame*h))
    strip.save(art/'vu.png')
if __name__=='__main__':main()
