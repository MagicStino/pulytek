// SPDX-License-Identifier: GPL-3.0-only
#pragma once
#include <cmath>
#include <algorithm>
struct Biquad {
    double b0=1,b1=0,b2=0,a1=0,a2=0,z1=0,z2=0;
    void reset(){z1=z2=0;}
    double process(double x) {
        double y=b0*x+z1;z1=b1*x-a1*y+z2;z2=b2*x-a2*y;
        if(std::abs(z1)<1e-30)z1=0; if(std::abs(z2)<1e-30)z2=0;
        return y;
    }
    void peak(double sr,double freq,double gain,double q) {
        double A=std::pow(10,gain/40), w=6.283185307179586*std::clamp(freq,20.0,sr*.475)/sr;
        double c=std::cos(w), alpha=std::sin(w)/(2*q), a0=1+alpha/A;
        b0=(1+alpha*A)/a0;b1=-2*c/a0;b2=(1-alpha*A)/a0;a1=b1;a2=(1-alpha/A)/a0;
    }
    void shelf(double sr,double freq,double gain) {
        double A=std::pow(10,gain/40),w=6.283185307179586*std::clamp(freq,20.0,sr*.475)/sr;
        double c=std::cos(w),s=std::sin(w),alpha=s/std::sqrt(2.0), beta=2*std::sqrt(A)*alpha;
        double a0=(A+1)-(A-1)*c+beta;
        b0=A*((A+1)+(A-1)*c+beta)/a0; b1=-2*A*((A-1)+(A+1)*c)/a0;
        b2=A*((A+1)+(A-1)*c-beta)/a0;a1=2*((A-1)-(A+1)*c)/a0;a2=((A+1)-(A-1)*c-beta)/a0;
    }
};
