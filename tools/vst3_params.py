#!/usr/bin/env python3
"""Generate optional JUCE parameter definitions from the native manifest."""
import json,sys
from pathlib import Path
p=json.loads((Path(__file__).resolve().parents[1]/'vst/params.json').read_text())['params'][:-2]
lines=['static juce::AudioProcessorValueTreeState::ParameterLayout layout(){','juce::AudioProcessorValueTreeState::ParameterLayout p;']
for v in p:
 key=json.dumps(v['key']);name=json.dumps(v['name']);pid='juce::ParameterID{'+key+',1}'
 if v.get('options'):
  opts=','.join(json.dumps(o) for o in v['options']);lines.append(f'p.add(std::make_unique<juce::AudioParameterChoice>({pid},{name},juce::StringArray{{{opts}}},{v["default"]}));')
 else:
  lines.append(f'p.add(std::make_unique<juce::AudioParameterFloat>({pid},{name},juce::NormalisableRange<float>{{{float(v["min"])}f,{float(v["max"])}f}},{float(v["default"])}f));')
lines+=['return p;','}'];Path(sys.argv[1]).write_text('\n'.join(lines)+'\n')
bank=json.loads((Path(__file__).resolve().parents[1]/'vst/presets.json').read_text())['presets']
lines=['struct FactoryPreset { const char* name; float values[32]; };','static const FactoryPreset factoryPresets[]={']
for preset in bank:
 lines.append('{'+json.dumps(preset['name'])+', {'+','.join(str(float(preset['values'][v['key']]))+'f' for v in p)+'}},')
lines.append('};')
with Path(sys.argv[1]).open('a') as out:out.write('\n'.join(lines)+'\n')
