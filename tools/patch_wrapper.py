#!/usr/bin/env python3
"""Generate a small local float-audio extension of the pinned MIT VST2 wrapper.
Skin/Q-Link/state logic stays upstream. The dependency checkout is never edited.
"""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
def patch(dep,out):
    source=dep/'wrapper/vst2_wrap.c';text=source.read_text()
    start=text.index('static void run_block(AEffect *e, float **in, float **out, int32_t n, int accumulate)',text.index('#ifdef PLUG_EFFECT\nstatic int16_t f2s'))
    end=text.index('static void processReplacing',start)
    text=text[:start]+'''extern void mpc_process_float(void*,float**,float**,int,int);
extern void mpc_set_sample_rate(void*,float);
extern void mpc_reset(void*);
static void run_block(AEffect *e,float **in,float **out,int32_t n,int accumulate) {
    wrap_t *w=e->object;
    if(n<=0 || !out || !out[0] || !out[1]) return;
    housekeeping(e,n);
    pthread_mutex_lock(&w->lock);
    mpc_process_float(w->dsp,in,out,n,accumulate);
    pthread_mutex_unlock(&w->lock);
}

'''+text[end:]
    original='case effSetSampleRate: case effSetBlockSize: case effMainsChanged: return 1;'
    assert text.count(original)==1
    text=text.replace(original,'''case effSetSampleRate:
        pthread_mutex_lock(&w->lock); mpc_set_sample_rate(w->dsp,o); pthread_mutex_unlock(&w->lock); return 1;
    case effMainsChanged:
        if(v==0) { pthread_mutex_lock(&w->lock); mpc_reset(w->dsp); pthread_mutex_unlock(&w->lock); } return 1;
    case effSetBlockSize: return 1;''')
    out.write_text('/* PulyTek local float-audio extension; upstream MIT license in licenses/. */\n'+text)
    return out
