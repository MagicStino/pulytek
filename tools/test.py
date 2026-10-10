#!/usr/bin/env python3
"""Offline DSP and native VST host verification with address/undefined sanitizers."""
import subprocess,sys,json
from pathlib import Path
from fetch_deps import fetch
from patch_wrapper import patch
ROOT=Path(__file__).resolve().parents[1]
def run(*args):subprocess.run(list(map(str,args)),check=True)
def main():
    dep=fetch();out=ROOT/'build/tests';out.mkdir(parents=True,exist_ok=True)
    run(sys.executable,dep/'tools/gen_vst.py',ROOT/'vst/vst.json','--params-h')
    flags=['-g','-O1','-fsanitize=address,undefined','-fno-omit-frame-pointer','-I'+str(ROOT/'src'),'-I'+str(dep/'wrapper'),'-I'+str(ROOT/'vst/build')]
    for src,name in [(ROOT/'src/engine.cpp','engine'),(ROOT/'src/upstream/EQP1A.cpp','circuit'),(ROOT/'tests/core_test.cpp','core_test')]:
        run('c++',*flags,'-std=c++17','-c',src,'-o',out/(name+'.o'))
    run('c++',*flags,out/'engine.o',out/'circuit.o',out/'core_test.o','-lpthread','-lm','-o',out/'core_test');run(out/'core_test')
    run('c++',*flags,'-std=c++17',ROOT/'tests/tube_test.cpp','-o',out/'tube_test');run(out/'tube_test')
    for src,name in [(patch(dep,out/'vst2_wrap.c'),'wrapper'),(dep/'tools/host_test.c','host')]:
        run('cc',*flags,'-std=gnu11','-c',src,'-o',out/(name+'.o'))
    run('c++',*flags,out/'engine.o',out/'circuit.o',out/'wrapper.o',out/'host.o','-lpthread','-lm','-o',out/'host_test');run(out/'host_test')
    params=json.loads((ROOT/'vst/params.json').read_text())['params']
    assert len(params)==35 and len({x['key'] for x in params})==35
    manifest=json.loads((ROOT/'openplugin.json').read_text());assert manifest['repo']=='MagicStino/pulytek' and manifest['kind']=='effect'
if __name__=='__main__':main()
