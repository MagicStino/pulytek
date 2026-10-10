#!/usr/bin/env python3
"""Verify package checksums and exercise the real installer against temporary settings only."""
import hashlib,json,os,subprocess,tempfile,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    catalog=json.loads((ROOT/'dist/openplugin.json').read_text())
    archive=ROOT/'dist'/catalog['packages'][0]['url'].rsplit('/',1)[-1]
    assert archive.stat().st_size==catalog['packages'][0]['size']
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==catalog['packages'][0]['sha256']
    with tempfile.TemporaryDirectory(prefix='pulytek-package-') as tmp:
        tmp=Path(tmp)
        with zipfile.ZipFile(archive) as z:
            assert all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist())
            z.extractall(tmp/'unpacked')
        root=next((tmp/'unpacked').iterdir())
        manifest=json.loads((root/'mpc-plugin.json').read_text())
        assert manifest['id']=='pulytek' and manifest['kind']=='effect' and manifest['arch']=='armv7' and manifest['layout']=='portable' and manifest['source_repo']=='MagicStino/pulytek'
        for line in (root/'SHA256SUMS').read_text().splitlines():
            sha,name=line.split('  ',1);assert hashlib.sha256((root/name).read_bytes()).hexdigest()==sha,name
        assert list(root.glob('portable/*/source/PulyTek-source.tar.gz'))
        settings=tmp/'MPC.settings';settings.write_text('<PROPERTIES>\n<VALUE name="pluginList-arm">\n<KNOWNPLUGINS>\n</KNOWNPLUGINS>\n</VALUE>\n</PROPERTIES>\n')
        synths=tmp/'Synths';log=tmp/'services.log'
        env=dict(os.environ,MPC_INSTALL_TEST='1',MPC_SETTINGS=str(settings),MPC_TEST_LOG=str(log),MPC_LEGACY_ROOT=str(tmp))
        subprocess.run(['sh','install.sh','-y','-t',str(synths)],cwd=root,env=env,check=True)
        ET.parse(settings);assert 'PulyTek' in settings.read_text();assert (synths/'MagicStino - VST - PulyTek/pulytek.so').exists()
        subprocess.run(['sh','uninstall.sh','-y','-t',str(synths)],cwd=root,env=env,check=True)
        ET.parse(settings);assert 'PulyTek' not in settings.read_text();assert not (synths/'MagicStino - VST - PulyTek/pulytek.so').exists()
        assert log.read_text().splitlines()==['stop','start','stop','start']
    print('Portable manifest, checksums, settings backup/registration, install/uninstall passed in a temporary fixture')
if __name__=='__main__':main()
