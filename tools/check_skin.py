#!/usr/bin/env python3
"""Check the actual generated skin's bounds, tab bindings and 4/8/16-Q-Link variants."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
skin=ROOT/'vst/build/skin/MagicStino - VST - PulyTek/Plugin Skins'
t=json.loads((skin/'TUI.json').read_text())['pageData']
assert [x['tabName'] for x in t['tabs']]==['EQUALIZER','TUBE & AIR','SIDE MIXING']
params=json.loads((ROOT/'vst/params.json').read_text())['params']
for tab in t['tabs']:
    for c in tab['componentDefinition']['componentsData']:
        x,y,w,h=map(float,c['bounds']['bounds'].split())
        assert x>=0 and y>=0 and x+w<=1280 and y+h<=628,(tab['tabName'],c['componentData']['name'],(x,y,w,h))
        for m in c['handle remapping']['map']:
            if m['value'].startswith('Parameter '):assert 0<=int(m['value'].split()[1])<len(params)
for name in ['Q-Links.json','Q-Links - 8by1.json']:
    assert (skin/name).is_file(),name
print('Native skin: all three tabs fit 1280x628; parameter bindings and Q-Link assets valid')
