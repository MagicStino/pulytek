#!/usr/bin/env python3
"""Fetch exact source versions; never execute downloaded repository scripts."""
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fetch():
    spec=json.loads((ROOT/'dependencies.json').read_text())['mpc-vst-plugins']
    dest=ROOT/'.deps/mpc-vst-plugins'
    dest.parent.mkdir(exist_ok=True)
    if not (dest/'.git').exists(): subprocess.run(['git','clone',spec['url'],str(dest)],check=True)
    sha=subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD'],text=True).strip()
    if sha!=spec['commit']:
        if subprocess.check_output(['git','-C',str(dest),'status','--porcelain'],text=True).strip():
            raise SystemExit('Dependency checkout is dirty; refusing to overwrite it')
        subprocess.run(['git','-C',str(dest),'checkout','--detach',spec['commit']],check=True)
    if subprocess.check_output(['git','-C',str(dest),'status','--porcelain'],text=True).strip():
        raise SystemExit('Dependency checkout is dirty')
    return dest
if __name__=='__main__': print(fetch())
