// SPDX-License-Identifier: GPL-3.0-only
#include "core.h"
extern "C" {
#include "engine.h"
}
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <cerrno>
static void* create(const char*){try{return new PulyTekCore;}catch(...){return nullptr;}}
static void destroy(void* p){delete static_cast<PulyTekCore*>(p);}
static void midi(void*,const uint8_t*,int){}
static void set(void* p,const char* key,const char* value){
    auto& s=*static_cast<PulyTekCore*>(p);
    if(!std::strcmp(key,"state")){
        if(std::strncmp(value,"PulyTek1 ",9))return;
        std::array<float,PulyTekCore::count> vals{};const char* at=value+9;
        for(auto& v:vals){char* end=nullptr;errno=0;v=std::strtof(at,&end);if(end==at||errno==ERANGE||!std::isfinite(v))return;at=end;}
        if(*at!=0)return;
        for(int i=0;i<s.count;++i)s.set(i,vals[i]);return;
    }
    for(int i=0;i<s.count;++i)if(!std::strcmp(key,s.keys[i])){
        char* end=nullptr;errno=0;float v=std::strtof(value,&end);
        if(end!=value&&*end==0&&errno!=ERANGE)s.set(i,v);return;
    }
}
static int get(void* p,const char* key,char* b,int len){
    auto& s=*static_cast<PulyTekCore*>(p);
    if(!std::strcmp(key,"state")){
        int at=std::snprintf(b,len,"PulyTek1");
        for(auto v:s.values){if(at<0||at>=len)return 0;at+=std::snprintf(b+at,len-at," %.9g",v);}return at<len?at:0;
    }
    if(!std::strcmp(key,"display_rev"))return std::snprintf(b,len,"%u",s.revision);
    if(!std::strcmp(key,"meter_l"))return std::snprintf(b,len,"%d",s.meter[0]);
    if(!std::strcmp(key,"meter_r"))return std::snprintf(b,len,"%d",s.meter[1]);
    for(int i=0;i<s.count;++i)if(!std::strcmp(key,s.keys[i]))return std::snprintf(b,len,"%.9g",s.values[i]);return 0;
}
static void render(void*,int16_t* out,int n){std::fill(out,out+n*2,0);}
static void process(void* p,const int16_t* in,int16_t* out,int n){
    auto& s=*static_cast<PulyTekCore*>(p);s.apply();
    for(int i=0;i<n;++i){auto v=s.processStereo(in[2*i]/32768.0,in[2*i+1]/32768.0);
        for(int ch=0;ch<2;++ch)out[2*i+ch]=int16_t(std::lrint(std::clamp(v[ch]*32768,-32768.0,32767.0)));}s.tick(n);
}
// The generated local wrapper extension uses floats directly, preserving EQ headroom.
extern "C" void mpc_process_float(void* p,float** in,float** out,int n,int accumulate){
    auto& s=*static_cast<PulyTekCore*>(p);s.apply();
    for(int i=0;i<n;++i){double l=in&&in[0]?in[0][i]:0,r=in&&in[1]?in[1][i]:0;
        auto v=s.processStereo(l,r);
        for(int ch=0;ch<2;++ch){if(accumulate)out[ch][i]+=float(v[ch]);else out[ch][i]=float(v[ch]);}}s.tick(n);
}
extern "C" void mpc_set_sample_rate(void* p,float sr){auto& s=*static_cast<PulyTekCore*>(p);if(sr!=s.sampleRate)s.prepare(sr);}
extern "C" void mpc_reset(void* p){auto& s=*static_cast<PulyTekCore*>(p);s.prepare(s.sampleRate);}
extern "C" const mpc_engine_t* mpc_engine(){static const mpc_engine_t api{create,destroy,midi,set,get,render,process};return &api;}
