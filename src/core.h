// SPDX-License-Identifier: GPL-3.0-only
#pragma once
#include "upstream/EQP1A.h"
#include "biquad.h"
#include "tube.h"
#include <array>
#include <cmath>
#include <algorithm>

struct PulyTekCore {
    static constexpr int count=33;
    // Saved state keys are stable. VST parameter order is vst/params.json.
    static constexpr const char* keys[count]={
      "lo_freq","hi_freq","cut_freq","lo_boost","lo_cut","hi_boost","bandwidth","hi_cut","output","bypass","tube","tube_mix",
      "side_on","width","side_gain","s1_freq","s1_gain","s1_q","s2_freq","s2_gain","s2_q","s3_freq","s3_gain","s3_q","s4_freq","s4_gain","s4_q","air","air_freq","tube_drive","tube_warmth","air_drive","air_mix"};
    std::array<float,count> values {{0,3,2,0,0,0,5,0,0,0,0,50,0,100,0,150,0,.707f,800,0,.707f,3000,0,.707f,10000,0,.707f,0,3,25,50,50,100}};
    std::unique_ptr<EQP1A> left,right;
    Biquad side[4],air[2];
    TubeStage tubeStage[2];
    double sampleRate=44100,dcIn[2]{},dcOut[2]{},rms[2]{};
    int meter[2]{},meterClock=0;
    unsigned revision=0;
    bool dirty=true;
    double gain=1,sideGain=1,dcCoeff=0,vuCoeff=0;
    PulyTekCore(){prepare(44100);}
    static std::pair<float,float> range(int i) {
        if(i==0)return {0,3};if(i==1)return {0,6};if(i==2)return {0,2};
        if(i==8)return {-20,20};if(i==9||i==10||i==12||i==27)return {0,1};
        if(i==11||i==29||i==30||i==31||i==32)return {0,100};if(i==13)return {0,200};if(i==14)return {-24,12};if(i==28)return {0,5};
        if(i>=15 && i<=26){if((i-15)%3==0)return {20,20000};if((i-15)%3==1)return {-12,12};return {.2f,10};}
        return {0,10};
    }
    void prepare(double sr) {
        if(!std::isfinite(sr)||sr<8000||sr>192000)return;
        sampleRate=sr;dcCoeff=std::exp(-6.283185307179586*10/sr);vuCoeff=std::exp(-1/(sr*.3));
        left=std::make_unique<EQP1A>();right=std::make_unique<EQP1A>();left->prepare(sr);right->prepare(sr);
        for(auto& b:side)b.reset();for(auto& b:air)b.reset();
        for(auto& t:tubeStage)t.prepare(sr);
        std::fill(std::begin(dcIn),std::end(dcIn),0);std::fill(std::begin(dcOut),std::end(dcOut),0);
        std::fill(std::begin(rms),std::end(rms),0);meter[0]=meter[1]=meterClock=0;dirty=true;apply();
    }
    void set(int i,float v) {
        if(i<0||i>=count||!std::isfinite(v))return;
        auto [min,max]=range(i);v=std::clamp(v,min,max);
        if(i<=2||i==9||i==10||i==12||i==27||i==28)v=std::round(v);
        if(values[i]!=v){
            if(i==12)for(auto& b:side)b.reset();
            if(i==27)for(auto& b:air)b.reset();
            if(i==10)for(auto& t:tubeStage)t.prepare(sampleRate);
            values[i]=v;dirty=true;
        }
    }
    void apply() {
        if(!dirty)return;
        auto pot=[](float v){return std::clamp(v*.1f,.00001f,.99999f);};
        for(auto* eq:{left.get(),right.get()})eq->setParams(pot(values[3]),pot(values[4]),pot(values[5]),pot(values[7]),pot(values[6]),int(values[0]),int(values[1]),int(values[2]));
        gain=std::pow(10,double(values[8])/20);sideGain=std::pow(10,double(values[14])/20);
        for(int i=0;i<4;++i)side[i].peak(sampleRate,values[15+i*3],values[16+i*3],values[17+i*3]);
        constexpr double frequencies[]={5000,8000,10000,12000,16000,20000};
        for(auto& b:air)b.shelf(sampleRate,frequencies[int(values[28])],values[31]*.06);
        for(auto& t:tubeStage)t.configure(sampleRate,values[29],values[30]);
        dirty=false;
    }
    std::array<double,2> processStereo(double l,double r) {
        std::array<double,2> out {{l,r}};
        if(values[9]<.5f) {
            out={{left->processSample(l),right->processSample(r)}};
            if(values[12]>.5f){
                double mid=(out[0]+out[1])*.5,s=(out[0]-out[1])*.5;
                for(auto& b:side)s=b.process(s);
                s*=sideGain*(values[13]*.01);out={{mid+s,mid-s}};
            }
            for(int ch=0;ch<2;++ch){
                if(values[27]>.5f){double wet=air[ch].process(out[ch]);out[ch]+=(wet-out[ch])*(values[32]*.01);}
                if(values[10]>.5f){
                    double wet=tubeStage[ch].process(out[ch]);
                    out[ch]+=(wet-out[ch])*(values[11]*.01);
                }
                out[ch]*=gain;
            }
        }
        for(int ch=0;ch<2;++ch){
            if(!std::isfinite(out[ch]))out[ch]=0;
            rms[ch]=vuCoeff*rms[ch]+(1-vuCoeff)*out[ch]*out[ch];
        }
        return out;
    }
    void tick(int frames) {
        meterClock+=frames;
        if(meterClock>=int(sampleRate/10)){
            meterClock%=int(sampleRate/10);bool changed=false;
            for(int ch=0;ch<2;++ch){double vu=10*std::log10(std::max(rms[ch],1e-12))+18;
                int v=int(std::round(std::clamp((vu+20)/23,0.0,1.0)*100));changed|=v!=meter[ch];meter[ch]=v;}
            if(changed)++revision;
        }
    }
};
