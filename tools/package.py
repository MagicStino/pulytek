#!/usr/bin/env python3
"""Create a portable native package with complete corresponding source and licenses."""
import argparse,gzip,hashlib,io,json,os,re,subprocess,sys,tarfile,tempfile,zipfile,stat
from pathlib import Path
from fetch_deps import fetch
ROOT=Path(__file__).resolve().parents[1]
VERSION='0.1.0-rc5'
def source_snapshot(dep,out):
    data=io.BytesIO()
    with tarfile.open(fileobj=data,mode='w') as t:
        for p in sorted(ROOT.rglob('*')):
            rel=p.relative_to(ROOT)
            if any(x in ('.git','.deps','.venv','build','dist','__pycache__') for x in rel.parts) or not p.is_file():continue
            raw=p.read_bytes();info=tarfile.TarInfo('pulytek/'+str(rel));info.size=len(raw);info.mode=0o755 if os.access(p,os.X_OK) else 0o644;info.mtime=0;t.addfile(info,io.BytesIO(raw))
        archive=subprocess.check_output(['git','-C',str(dep),'archive','HEAD'])
        with tarfile.open(fileobj=io.BytesIO(archive)) as upstream:
            for original in upstream:
                if not original.isfile():continue
                raw=upstream.extractfile(original).read();info=tarfile.TarInfo('mpc-vst-plugins/'+original.name);info.size=len(raw);info.mode=original.mode;info.mtime=0;t.addfile(info,io.BytesIO(raw))
    with out.open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0,filename='') as g:g.write(data.getvalue())
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--version',default=VERSION);a=parser.parse_args()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?',a.version):raise SystemExit('Invalid version')
    dep=fetch();dist=ROOT/'dist';dist.mkdir(exist_ok=True)
    snapshot=dist/'PulyTek-source.tar.gz';source_snapshot(dep,snapshot)
    subprocess.run([sys.executable,str(ROOT/'tools/validate_elf.py'),str(ROOT/'build/armv7/pulytek.so')],check=True)
    subprocess.run([sys.executable,str(dep/'tools/release.py'),'--so',str(ROOT/'build/armv7/pulytek.so'),'--skin',str(ROOT/'vst/build/skin/MagicStino - VST - PulyTek'),'--entry',str(ROOT/'vst/build/pluginlist-entry.xml'),'--version',a.version,'--id','pulytek','--repo','MagicStino/pulytek','--license','GPL-3.0-only','--about','Experimental Pultec-style WDF EQ. Hardware validation pending.','--extra',str(ROOT/'licenses')+':licenses','--extra',str(ROOT/'LICENSE')+':LICENSE','--extra',str(ROOT/'NOTICE.md')+':NOTICE.md','--extra',str(snapshot)+':source/PulyTek-source.tar.gz','-o',str(dist)],check=True)
    archive=dist/f'PulyTek-{a.version}-mpc-armv7.zip'
    with zipfile.ZipFile(archive) as z:files={i.filename:(z.read(i),i.external_attr) for i in z.infolist()}
    top=f'PulyTek-{a.version}/'
    # Replace upstream generic installation prose, including its unrelated hardware-tested claim.
    install=(ROOT/'docs/INSTALL.md').read_text().replace('0.1.0-rc5',a.version)
    files[top+'INSTALL.md']=(install.encode(),(stat.S_IFREG|0o644)<<16)
    files[top+'VALIDATION.json']=((ROOT/'build/armv7/pulytek.validation.json').read_bytes(),(stat.S_IFREG|0o644)<<16)
    sums=''.join(hashlib.sha256(raw).hexdigest()+'  '+name[len(top):]+'\n' for name,(raw,_) in sorted(files.items()) if name!=top+'SHA256SUMS')
    files[top+'SHA256SUMS']=(sums.encode(),(stat.S_IFREG|0o644)<<16)
    with zipfile.ZipFile(archive,'w') as z:
        for name,(raw,mode) in sorted(files.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.create_system=3;info.external_attr=mode;info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,raw)
    digest=hashlib.sha256(archive.read_bytes()).hexdigest();archive.with_suffix('.zip.sha256').write_text(digest+'  '+archive.name+'\n')
    m=json.loads((ROOT/'openplugin.json').read_text());m['packages']=[{'version':a.version,'arch':'armv7','layout':'portable','devices':['force','mpc-gen1'],'size':archive.stat().st_size,'sha256':digest,'url':f'https://github.com/MagicStino/pulytek/releases/download/v{a.version}/{archive.name}'}]
    (dist/'openplugin.json').write_text(json.dumps(m,indent=2)+'\n')
    print(archive,digest)
if __name__=='__main__':main()
