#!/usr/bin/env python3
"""Build the Force/MPC native ARMv7 VST2 plugin (or a host test library)."""
import argparse, json, os, subprocess, sys
from pathlib import Path
from fetch_deps import fetch
from patch_wrapper import patch
ROOT=Path(__file__).resolve().parents[1]
def run(*args,**kwargs): subprocess.run(list(map(str,args)),check=True,**kwargs)
def build(target,zig=None,skin=True):
    dep=fetch(); out=ROOT/'build'/target; out.mkdir(parents=True,exist_ok=True)
    os.environ['ZIG_GLOBAL_CACHE_DIR']=str(ROOT/'build/zig-cache')
    os.environ['ZIG_LOCAL_CACHE_DIR']=str(ROOT/'build/zig-local-cache')
    if target=='armv7':
        zig=zig or 'zig'
        version=subprocess.check_output([zig,'version'],text=True).strip()
        if version!='0.15.2': raise SystemExit('Use pinned Zig 0.15.2')
        cc=[zig,'cc']; cxx=[zig,'c++']
        arch=['-target','arm-linux-gnueabihf.2.31','-mcpu=cortex_a17']
    else: cc=['cc'];cxx=['c++'];arch=[]
    # Params and the full skin share one manifest; indices must match.
    run(sys.executable,dep/'tools/gen_vst.py',ROOT/'vst/vst.json','--params-h')
    flags=arch+['-O2','-fPIC','-fvisibility=hidden','-ffile-prefix-map='+str(ROOT)+'=.','-I'+str(ROOT/'vst/build'),'-I'+str(dep/'wrapper'),'-I'+str(ROOT/'src')]
    for source,name in [(ROOT/'src/engine.cpp','engine'),(ROOT/'src/upstream/EQP1A.cpp','circuit')]:
        run(*cxx,*flags,'-std=c++17','-c',source,'-o',out/(name+'.o'))
    run(*cc,*flags,'-std=gnu11','-c',patch(dep,out/'vst2_wrap.c'),'-o',out/'wrapper.o')
    run(*cxx,*arch,'-shared','-s',out/'engine.o',out/'circuit.o',out/'wrapper.o','-lm','-lpthread','-Wl,--no-undefined','-o',out/'pulytek.so')
    if target=='armv7': run(sys.executable,ROOT/'tools/validate_elf.py',out/'pulytek.so')
    if skin:
        run(sys.executable,ROOT/'tools/make_art.py')
        env=dict(os.environ,SHADOW_SKIN_MPC_OS='2')
        run(sys.executable,dep/'tools/gen_vst.py',ROOT/'vst/vst.json',env=env)
        run(sys.executable,ROOT/'tools/render_preview.py')
    return out/'pulytek.so'
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__); a.add_argument('--target',choices=['host','armv7'],default='armv7'); a.add_argument('--zig');a.add_argument('--no-skin',action='store_true');args=a.parse_args()
    print(build(args.target,args.zig,not args.no_skin))
