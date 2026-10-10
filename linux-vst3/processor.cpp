// SPDX-License-Identifier: GPL-3.0-only
#include <juce_audio_utils/juce_audio_utils.h>
#include "core.h"
#include "parameter_layout.h"
class Processor final:public juce::AudioProcessor {
    PulyTekCore core;
    juce::AudioProcessorValueTreeState state;
public:
    Processor():AudioProcessor(BusesProperties().withInput("Input",juce::AudioChannelSet::stereo(),true).withOutput("Output",juce::AudioChannelSet::stereo(),true)),state(*this,nullptr,"PulyTek",layout()){}
    const juce::String getName()const override{return "PulyTek";}
    bool acceptsMidi()const override{return false;}bool producesMidi()const override{return false;}
    double getTailLengthSeconds()const override{return 0;}
    int getNumPrograms()override{return 1;}int getCurrentProgram()override{return 0;}void setCurrentProgram(int)override{}
    const juce::String getProgramName(int)override{return {};};void changeProgramName(int,const juce::String&)override{}
    void prepareToPlay(double sr,int)override{core.prepare(sr);}
    void releaseResources()override{}
    bool isBusesLayoutSupported(const BusesLayout& l)const override{return l.getMainInputChannelSet()==juce::AudioChannelSet::stereo()&&l.getMainOutputChannelSet()==juce::AudioChannelSet::stereo();}
    void processBlock(juce::AudioBuffer<float>& b,juce::MidiBuffer&)override{
        juce::ScopedNoDenormals guard;
        for(int i=0;i<core.count;++i)core.set(i,state.getRawParameterValue(core.keys[i])->load());core.apply();
        for(int i=0;i<b.getNumSamples();++i){auto y=core.processStereo(b.getSample(0,i),b.getSample(1,i));b.setSample(0,i,float(y[0]));b.setSample(1,i,float(y[1]));}core.tick(b.getNumSamples());
    }
    bool hasEditor()const override{return true;}
    juce::AudioProcessorEditor* createEditor()override{return new juce::GenericAudioProcessorEditor(*this);}
    void getStateInformation(juce::MemoryBlock& b)override{auto xml=state.copyState().createXml();copyXmlToBinary(*xml,b);}
    void setStateInformation(const void* d,int n)override{auto xml=getXmlFromBinary(d,n);if(xml&&xml->hasTagName(state.state.getType()))state.replaceState(juce::ValueTree::fromXml(*xml));}
};
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter(){return new Processor;}
