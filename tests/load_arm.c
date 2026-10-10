/* SPDX-License-Identifier: GPL-3.0-only
 * ARM dlopen + audio smoke test. Run under QEMU against the device rootfs. */
#include <stdint.h>
#include <dlfcn.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <assert.h>
typedef struct AEffect AEffect;
typedef intptr_t (*cb)(AEffect*,int32_t,int32_t,intptr_t,void*,float);
struct AEffect {int32_t magic;intptr_t(*d)(AEffect*,int32_t,int32_t,intptr_t,void*,float);void*p;void(*setP)(AEffect*,int32_t,float);float(*getP)(AEffect*,int32_t);int32_t np,npar,ni,no,flags;intptr_t r1,r2;int32_t a,b,c;float io;void*obj,*user;int32_t uid,ver;void(*pr)(AEffect*,float**,float**,int32_t);void*pdr;char f[56];};
static intptr_t host(AEffect*e,int32_t op,int32_t i,intptr_t v,void*p,float o){return op==1?2400:0;}
int main(int argc,char**argv){assert(argc==2);void*h=dlopen(argv[1],RTLD_NOW);if(!h){puts(dlerror());return 1;}
    AEffect*(*entry)(cb)=dlsym(h,"VSTPluginMain");assert(entry);AEffect* a=entry(host);assert(a&&a->npar==35&&a->ni==2&&a->no==2);
    a->d(a,0,0,0,0,0);a->d(a,10,0,0,0,48000);a->d(a,11,0,128,0,0);
    float l[257],r[257],ol[257],orr[257];float*in[]={l,r},*out[]={ol,orr};
    for(int i=0;i<257;++i){l[i]=.05f*sinf(.1f*i);r[i]=-.02f*cosf(.03f*i);}
    a->setP(a,9,1);a->pr(a,in,out,257);assert(!memcmp(l,ol,sizeof l)&&!memcmp(r,orr,sizeof r));
    a->setP(a,9,0);a->setP(a,10,1);a->setP(a,12,1);a->setP(a,27,1);
    for(int k=0;k<64;++k){a->pr(a,in,out,257);for(int i=0;i<257;++i)assert(isfinite(ol[i])&&isfinite(orr[i]));}
    void*state=0;intptr_t n=a->d(a,23,0,0,&state,0);assert(n>10&&state);a->d(a,24,0,n,state,0);
    a->d(a,12,0,0,0,0);a->d(a,1,0,0,0,0);dlclose(h);puts("ARM load, 48 kHz, 257-frame float audio, bypass, processing and state passed");return 0;
}
