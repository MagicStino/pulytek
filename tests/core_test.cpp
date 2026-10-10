// SPDX-License-Identifier: GPL-3.0-only
#include "core.h"
extern "C" {
#include "engine.h"
}
#include <cassert>
#include <cstring>
#include <iostream>
#include <random>
#include <chrono>
static double response(PulyTekCore& c,double frequency,bool side=false){
    c.apply();double power=0;const int n=int(c.sampleRate);
    for(int i=0;i<n;++i){double x=.01*std::sin(6.283185307179586*frequency*i/c.sampleRate);auto y=c.processStereo(x,side?-x:x);if(i>n/2)power+=y[0]*y[0];}
    return std::sqrt(power/(n/2))/.007071067811865;
}
int main(){
    std::mt19937 rng(7);std::uniform_real_distribution<double> noise(-.1,.1);
    PulyTekCore flat,eq;
    eq.set(3,7);double f=response(flat,60), boosted=response(eq,60);
    assert(boosted>f*1.4); // the real WDF low boost changes bass response
    for(double sr:{44100.,48000.,96000.}){
        PulyTekCore a,b;a.prepare(sr);b.prepare(sr);b.set(12,1);b.apply();
        for(int i=0;i<4096;++i){double l=noise(rng),r=noise(rng);auto x=a.processStereo(l,r),y=b.processStereo(l,r);assert(std::abs(x[0]-y[0])<1e-10);assert(std::abs(x[1]-y[1])<1e-10);}
        b.set(13,0);b.apply();for(int i=0;i<256;++i){auto y=b.processStereo(noise(rng),noise(rng));assert(y[0]==y[1]);}
    }
    {PulyTekCore a,b;b.set(12,1);b.set(13,200);b.apply();for(int i=0;i<4096;++i){double l=noise(rng),r=noise(rng);auto x=a.processStereo(l,r),y=b.processStereo(l,r);assert(std::abs((x[0]+x[1])-(y[0]+y[1]))<1e-10);assert(std::abs((y[0]-y[1])-2*(x[0]-x[1]))<1e-10);}}
    {PulyTekCore a,b;b.set(12,1);b.set(16,10);b.apply();for(int i=0;i<4096;++i){double x=noise(rng);auto y=a.processStereo(x,x),z=b.processStereo(x,x);assert(std::abs(y[0]-z[0])<1e-10);}}
    for(int band=0;band<4;++band){PulyTekCore a,b;b.set(12,1);b.set(16+band*3,6);double freq=b.values[15+band*3];assert(response(b,freq,true)>response(a,freq,true)*1.5);}
    for(int choice=0;choice<6;++choice){PulyTekCore a,b;b.set(27,1);b.set(28,float(choice));assert(response(b,21000)>response(a,21000)*1.1);}
    {PulyTekCore a,b;b.set(10,1);b.set(11,0);b.apply();for(int i=0;i<8192;++i){double x=noise(rng);auto y=a.processStereo(x,x),z=b.processStereo(x,x);assert(y==z);}}
    {PulyTekCore a,b;b.set(10,1);b.set(11,100);b.apply();double delta=0;for(int i=0;i<8192;++i){double x=.6*std::sin(.1*i);auto y=a.processStereo(x,x),z=b.processStereo(x,x);delta+=std::abs(y[0]-z[0]);}assert(delta>1);}
    {PulyTekCore a;a.set(9,1);a.apply();auto y=a.processStereo(2.5,-1.7);assert(y[0]==2.5&&y[1]==-1.7);}
    {PulyTekCore a;a.set(9,1);a.apply();for(int i=0;i<44100*3;++i){double x=std::pow(10.,-18./20)*std::sqrt(2.)*std::sin(.1*i);a.processStereo(x,x);a.tick(1);}assert(std::abs(a.meter[0]-87)<=1);assert(a.revision>0);}
    // Extreme combinations, non-finite controls, reset and independent channels.
    for(double sr:{22050.,44100.,48000.,96000.})for(int extreme=0;extreme<2;++extreme){
        PulyTekCore a;a.prepare(sr);for(int i=0;i<a.count;++i){auto [mn,mx]=a.range(i);a.set(i,extreme?mx:mn);}a.set(9,0);a.apply();
        for(int i=0;i<8192;++i){auto y=a.processStereo(noise(rng),0);assert(std::isfinite(y[0])&&std::isfinite(y[1]));assert(std::abs(y[0])<100);}
        auto before=a.values;a.set(3,NAN);a.set(4,INFINITY);assert(a.values==before);a.prepare(sr);
    }
    {PulyTekCore a;for(int i=0;i<1024;++i){auto y=a.processStereo(noise(rng),0);assert(y[1]==0);}}
    const mpc_engine_t* api=mpc_engine();void* a=api->create(nullptr);void* b=api->create(nullptr);assert(a&&b);
    for(int i=0;i<PulyTekCore::count;++i){auto [mn,mx]=PulyTekCore::range(i);char text[64];std::snprintf(text,sizeof text,"%.9g",(mn+mx)/2);api->set_param(a,PulyTekCore::keys[i],text);}
    char state[2048], restored[2048];assert(api->get_param(a,"state",state,sizeof state)>0);api->set_param(b,"state",state);api->get_param(b,"state",restored,sizeof restored);assert(!std::strcmp(state,restored));
    for(const char* bad:{"PulyTek1 nan","PulyTek1 0 0","bad","PulyTek1 0 0 garbage"}){api->set_param(b,"state",bad);api->get_param(b,"state",restored,sizeof restored);assert(!std::strcmp(state,restored));}
    api->destroy(a);api->destroy(b);
    PulyTekCore cpu;cpu.set(10,1);cpu.set(12,1);cpu.set(27,1);cpu.apply();auto start=std::chrono::steady_clock::now();
    for(int i=0;i<441000;++i)cpu.processStereo(.1,.03);
    std::cout<<"DSP checks passed; 10 seconds audio processed in "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<" desktop seconds (not a Force CPU benchmark).\n";
}
