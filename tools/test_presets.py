#!/usr/bin/env python3
"""Validate complete recalls and render every program at supported rates."""
import json, math, subprocess
from collections import Counter
from pathlib import Path
root=Path(__file__).resolve().parents[1]
params=json.loads((root/'vst/params.json').read_text())['params'][:-2]
bank=json.loads((root/'vst/presets.json').read_text())['presets']
counts=Counter(p['category'] for p in bank if p['category']!='Init')
assert len(counts)>=8 and min(counts.values())>=6
assert len({p['name'] for p in bank})==len(bank)
rows=[]
for preset in bank:
 values=preset['values'];assert set(values)=={p['key'] for p in params}
 assert list(values).index('air_drive')<list(values).index('air')
 assert len(preset['name'])<=24
 for p in params:
  v=values[p['key']];assert math.isfinite(v)
  if 'options' in p:assert isinstance(v,int) and 0<=v<len(p['options'])
  else:assert p['min']<=v<=p['max']
 rows.append('{'+','.join(str(float(values[p['key']]))+'f' for p in params)+'}')
out=root/'build/tests';out.mkdir(parents=True,exist_ok=True)
source='''#include "core.h"
#include <cassert>
#include <cstdio>
static float presets[][32]={ROWS};
int main(){
 for(double sr:{44100.,48000.,96000.}){
  PulyTekCore core;core.prepare(sr);
  for(int n=0;n<49;++n){
   // Start from deliberately conflicting settings to expose partial recalls.
   core.set(31,0);core.set(12,1);core.set(13,190);core.set(10,1);
   core.set(31,presets[n][31]);
   for(int i=0;i<32;++i)core.set(i,presets[n][i]);core.apply();
   for(int i=0;i<32;++i)assert(std::abs(core.values[i]-presets[n][i])<1e-5);
   double peak=0,energy=0;
   for(int i=0;i<int(sr*.4);++i){
    double t=i/sr;
    double l=.06*(std::sin(6.283185307*60*t)+std::sin(6.283185307*997*t)+std::sin(6.283185307*11003*t));
    double r=.06*(std::sin(6.283185307*80*t)+std::sin(6.283185307*997*t)+std::sin(6.283185307*7001*t));
    auto y=core.processStereo(l,r);
    for(auto v:y){assert(std::isfinite(v));peak=std::max(peak,std::abs(v));energy+=v*v;}
   }
   assert(peak<1);assert(energy>0);
   printf("%g,%d,%.6f\\n",sr,n,peak);
  }
 }
}
'''.replace('ROWS',','.join(rows))
(out/'presets_test.cpp').write_text(source)
subprocess.run(['c++','-std=c++17','-O2','-I'+str(root/'src'),str(out/'presets_test.cpp'),str(root/'src/upstream/EQP1A.cpp'),'-o',str(out/'presets_test')],check=True)
with (out/'preset-headroom.csv').open('w') as report:
 report.write('sample_rate,preset_index,peak_for_test_multitone\n')
 subprocess.run([str(out/'presets_test')],stdout=report,check=True)
print(f'{len(bank)} presets: complete recall, finite output and test-signal headroom at 44.1/48/96 kHz passed')
