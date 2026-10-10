// SPDX-License-Identifier: GPL-3.0-only
// Reuse the pinned host ABI and parameter manifest, without changing upstream.
#define main upstream_host_main
#include "host_test.c"
#undef main
#include <assert.h>
static int redraws, meter_events;
static intptr_t meter_host(AEffect *e,int32_t op,int32_t i,intptr_t v,void *p,float o) {
    if(op==42)redraws++;
    if(op==0 && i>=32)meter_events++;
    return host(e,op,i,v,p,o);
}
int main(void) {
    AEffect *a=VSTPluginMain(meter_host);assert(a);
    float inL[128],inR[128],outL[128],outR[128];
    float *in[]={inL,inR},*out[]={outL,outR};
    run(a,100);redraws=meter_events=0;
    for(int k=0;k<1500;k++) {
        for(int i=0;i<128;i++)inL[i]=inR[i]=.3f*sinf((k*128+i)*.1f)*(k%300<150?1.f:.1f);
        a->pr(a,in,out,128);
    }
    assert(meter_events>10);assert(redraws==0);
    a->d(a,2,0,1,0,0);run(a,100);
    assert(a->d(a,3,0,0,0,0)==1);assert(redraws>0);
    a->d(a,1,0,0,0,0);
    puts("VU host notifications: needles update without rebuilding PRESET; preset selection still redraws");
    return 0;
}
