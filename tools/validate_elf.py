#!/usr/bin/env python3
"""Refuse the wrong ABI, unresolved C++ runtimes, or newer glibc dependencies."""
import re, subprocess, sys, json
from pathlib import Path
p=Path(sys.argv[1]);read=lambda *args:subprocess.check_output(['readelf',*args,str(p)],text=True)
h=read('-h');a=read('-A');v=read('--version-info');d=read('-d');symbols=read('--dyn-syms','-W')
assert 'ELF32' in h and re.search(r'Machine:\s+ARM\b',h), 'Expected ELF32 ARM'
assert 'hard-float ABI' in h and 'VFP registers' in a, 'Expected ARM hard-float ABI'
assert 'VSTPluginMain' in symbols, 'Missing VSTPluginMain'
versions=[tuple(map(int,s.split('.'))) for s in re.findall(r'GLIBC_([0-9.]+)',v)]
assert not versions or max(versions)<=(2,31), 'glibc newer than 2.31'
assert not re.search(r'GLIBCXX_|CXXABI_',v), 'C++ runtime must be linked statically'
needed=re.findall(r'Shared library: \[(.*?)\]',d)
assert set(needed)<= {'libc.so.6','libm.so.6','libpthread.so.0','libdl.so.2','librt.so.1','ld-linux-armhf.so.3'}, needed
report={'elf':'ELF32 ARM EABI5 hard-float','max_glibc':'.'.join(map(str,max(versions))) if versions else None,'needed':needed,'VSTPluginMain':True,'hardware_tested':False}
p.with_suffix('.validation.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report))
