#!/usr/bin/env python3
"""Use firmware-native Roboto for quieter live labels and values; artwork uses bundled serif."""
import json,sys
from pathlib import Path
p=Path(sys.argv[1])/'Plugin Skins/TUI.json'
d=json.loads(p.read_text())
def walk(v):
    if isinstance(v,dict):
        if v.get('type')=='Label' and isinstance(v.get('data'),dict):
            data=v['data'];f=data.get('textStyle',{}).get('font')
            if f:f['name']='Roboto';f['style']='Regular';f['height']=22 if data.get('type')=='Value' else 15
        for child in v.values():walk(child)
    elif isinstance(v,list):
        for child in v:walk(child)
# Native generated toggles focus on tap by default. Make every switch tap-toggle.
for definition in d['pageData']['componentDefinitions']['localComponentDefinitions']:
    if definition['key'].startswith('shToggle'):
        for action in definition['value']['actions']:
            if action.get('onAction') == 'Mouse Down':
                action['handler'] = 'Toggle Switch'
        # POWER is the inverse of the existing bypass parameter, without a new state key.
        if '_40x40' in definition['key']:
            for component in definition['value']['componentsData']:
                data = component['componentData'].get('data', {})
                if 'onImage' in data:
                    data['onImage'], data['offImage'] = data['offImage'], data['onImage']
walk(d);p.write_text(json.dumps(d,indent=2)+'\n')
