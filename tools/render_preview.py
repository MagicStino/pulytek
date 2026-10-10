#!/usr/bin/env python3
"""Composite the generated native skin at manifest defaults (not a hardware capture)."""
import json,sys,re
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.deps/mpc-vst-plugins/tools'))
import studio

def main():
    skin=ROOT/'vst/build/skin/MagicStino - VST - PulyTek/Plugin Skins'
    t=json.loads((skin/'TUI.json').read_text())['pageData']
    defs={d['key']:d['value'] for d in t['componentDefinitions']['localComponentDefinitions']}
    params=json.loads((ROOT/'vst/params.json').read_text())['params']
    bounds=lambda b:list(map(lambda x:int(float(x)),b['bounds'].split()))
    fontPath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    for n,tab in enumerate(t['tabs']):
        im=Image.open(skin/f'sh_bg_{n}.png').convert('RGBA');dr=ImageDraw.Draw(im)
        comps=studio.tab_components(tab,defs)
        for c in comps:
            cd=c['componentData'];definition=defs.get(cd['type'])
            if not definition:continue
            maps={m['key']:m['value'] for m in c['handle remapping']['map']}
            match=re.fullmatch(r'Parameter (\d+)',maps.get('Data',''))
            if not match:continue
            p=params[int(match[1])];v=p.get('default',0);options=p.get('options',[])
            norm=v/(len(options)-1) if len(options)>1 else (v-p.get('min',0))/(p.get('max',1)-p.get('min',0))
            x,y,w,h=bounds(c['bounds'])
            for sub in definition['componentsData']:
                sd=sub['componentData'];sx,sy,sw,sh=bounds(sub['bounds']);data=sd['data']
                if sd['type']=='Knob' and data.get('filmStrip'):
                    strip=Image.open(skin/data['filmStrip']).convert('RGBA');nf=data['numFrames'];fh=strip.height//nf;k=round(norm*(nf-1));img=strip.crop((0,k*fh,strip.width,(k+1)*fh));im.alpha_composite(img,(x+sx,y+sy))
                elif sd['type']=='Button':
                    # Option segments select the manifest default; switches follow their state.
                    selected=int(v)==int(data.get('buttonId',1))
                    path=data.get('onImage' if selected else 'offImage')
                    if path and (skin/path).exists():im.alpha_composite(Image.open(skin/path).convert('RGBA'),(x+sx,y+sy))
                elif sd['type']=='Label':
                    kind=data.get('type');text=cd.get('name','') if kind=='Name' else (options[int(v)] if options else f'{v:g}'+(' '+p['unit'] if p.get('unit') else ''))
                    ts=data['textStyle'];font=ImageFont.truetype(fontPath,max(10,round(ts['font']['height'])));color='#'+ts.get('colour','fff8f5e7')[-6:]
                    dr.text((x+sx+sw/2,y+sy+sh/2),text,font=font,fill=color,anchor='mm')
        im.convert('RGB').save(ROOT/f'docs/preview_{n}.png')
if __name__=='__main__':main()
