// SPDX-License-Identifier: GPL-3.0-only
#pragma once
#include "biquad.h"
#include <cmath>
#include <algorithm>

// Original amp-inspired colour stage, not an identified tube circuit model.
// Two asymmetric stages use first-order antiderivative antialiasing (ADAA).
// The primitive of tanh is log(cosh); stable evaluation avoids overflow.
struct TubeStage {
    struct Triode {
        double previous=0;
        static double logCosh(double x){double a=std::abs(x);return a+std::log1p(std::exp(-2*a))-std::log(2.0);}
        double process(double x,double drive,double bias) {
            const double t=std::tanh(bias),normal=drive*(1-t*t);
            double delta=x-previous,y;
            if(std::abs(delta)<1e-7)
                y=(std::tanh(drive*(x+previous)*.5+bias)-t)/normal;
            else
                y=((logCosh(drive*x+bias)-logCosh(drive*previous+bias))/(drive*delta)-t)/normal;
            previous=x;return y;
        }
    } stage[2];
    Biquad body,top;
    double drive=1,colour=0,envelope=0,attack=0,release=0,dcCoeff=0,dcIn=0,dcOut=0;
    double targetDrive=1,targetColour=0,smooth=0;
    void prepare(double sr){
        *this=TubeStage{};
        attack=std::exp(-1/(sr*.008));release=std::exp(-1/(sr*.120));
        dcCoeff=std::exp(-6.283185307179586*10/sr);smooth=std::exp(-1/(sr*.020));
        configure(sr,25,50);drive=targetDrive;colour=targetColour;
    }
    void configure(double sr,double drivePercent,double warmthPercent){
        // 0..18 dB drive; broad 180 Hz body and a gentle 4.5 kHz darkening.
        targetDrive=std::pow(10,drivePercent*.18/20);targetColour=warmthPercent*.01;
        body.peak(sr,180,2.5*targetColour,.55);
        top.shelf(sr,4500,-3.5*targetColour);
    }
    double process(double x){
        drive=smooth*drive+(1-smooth)*targetDrive;
        colour=smooth*colour+(1-smooth)*targetColour;
        double wet=body.process(x);
        double level=std::abs(wet),coeff=level>envelope?attack:release;
        envelope=coeff*envelope+(1-coeff)*level;
        // Slow bias modulation gives level-dependent compression; bounded at high levels.
        const double sag=1/(1+.35*colour*std::min(envelope,4.0));
        wet=stage[0].process(wet,drive,.12+.18*colour);
        wet=stage[1].process(wet,1+.35*(drive-1),-.06-.09*colour)*sag;
        wet=top.process(wet);
        double dc=wet-dcIn+dcCoeff*dcOut;dcIn=wet;dcOut=dc;
        return dc;
    }
};
