// SPDX-License-Identifier: GPL-3.0-only
#include "tube.h"
#include <cassert>
#include <iostream>
#include <vector>
constexpr double pi=3.14159265358979323846;
static double amplitude(const std::vector<double>& a,double freq,double sr){double re=0,im=0;for(size_t i=0;i<a.size();++i){double phase=2*pi*freq*i/sr;re+=a[i]*std::cos(phase);im-=a[i]*std::sin(phase);}return 2*std::hypot(re,im)/a.size();}
static std::vector<double> tone(double sr,double freq,double level,double drive,double warmth){TubeStage t;t.prepare(sr);t.configure(sr,drive,warmth);std::vector<double> out;for(int i=0;i<int(sr)*2;++i){double y=t.process(level*std::sin(2*pi*freq*i/sr));assert(std::isfinite(y));if(i>=int(sr))out.push_back(y);}return out;}
int main(){
    for(double sr:{44100.,48000.,96000.}){
        double bass0=amplitude(tone(sr,180,.001,0,0),180,sr),bass1=amplitude(tone(sr,180,.001,0,100),180,sr);
        double top0=amplitude(tone(sr,12000,.001,0,0),12000,sr),top1=amplitude(tone(sr,12000,.001,0,100),12000,sr);
        assert(bass1/bass0>1.25&&bass1/bass0<1.4);assert(top1/top0<.73&&top1/top0>.6);
        auto clean=tone(sr,1000,.3,0,50),driven=tone(sr,1000,.3,100,50);
        double h2=amplitude(driven,2000,sr),h3=amplitude(driven,3000,sr);
        assert(h2>.001&&h3>.001);assert(amplitude(driven,1000,sr)<amplitude(clean,1000,sr));
        double mean=0;for(double x:driven)mean+=x;assert(std::abs(mean/driven.size())<1e-5);
        std::cout<<"Tube "<<sr<<" Hz: warmth 180 Hz "<<20*std::log10(bass1/bass0)<<" dB, 12 kHz "<<20*std::log10(top1/top0)<<" dB; driven H2/H3 "<<h2<<" / "<<h3<<"\n";
    }
    // Compare the first nonlinear stage to an un-antialiased version at a folded harmonic.
    TubeStage::Triode aa;std::vector<double> a,b;double sr=48000,freq=10000,drive=6,bias=.25,t=std::tanh(bias);
    for(int i=0;i<96000;++i){double x=.5*std::sin(2*pi*freq*i/sr),y=aa.process(x,drive,bias);if(i>=48000){a.push_back(y);b.push_back((std::tanh(drive*x+bias)-t)/(drive*(1-t*t)));}}
    double aliasA=amplitude(a,18000,sr),aliasB=amplitude(b,18000,sr);
    assert(aliasA<aliasB*.6);
    std::cout<<"ADAA folded third harmonic improvement: "<<20*std::log10(aliasB/aliasA)<<" dB (one fixed test, not a zero-aliasing claim)\n";
    TubeStage stage;stage.prepare(48000);stage.configure(48000,100,100);
    for(int i=0;i<48000;++i)stage.process(.5);for(int i=0;i<48000;++i)assert(std::isfinite(stage.process(0)));
    assert(std::abs(stage.process(0))<1e-6);
}
