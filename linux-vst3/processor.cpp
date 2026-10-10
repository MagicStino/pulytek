// SPDX-License-Identifier: GPL-3.0-only
#include <juce_audio_utils/juce_audio_utils.h>
#include "core.h"
#include "parameter_layout.h"
class Processor final:public juce::AudioProcessor {
    PulyTekCore core;
    int currentProgram=0;
    juce::AudioProcessorValueTreeState state;
public:
    Processor():AudioProcessor(BusesProperties().withInput("Input",juce::AudioChannelSet::stereo(),true).withOutput("Output",juce::AudioChannelSet::stereo(),true)),state(*this,nullptr,"PulyTek",layout()){}
    const juce::String getName()const override{return "PulyTek";}
    bool acceptsMidi()const override{return false;}bool producesMidi()const override{return false;}
    double getTailLengthSeconds()const override{return 0;}
    int getNumPrograms()override{return int(std::size(factoryPresets));}int getCurrentProgram()override{return currentProgram;}
    void setCurrentProgram(int n)override{
        if(n<0||n>=getNumPrograms())return;
        currentProgram=n;
        for(int i=0;i<core.count;++i){auto* p=state.getParameter(core.keys[i]);p->setValueNotifyingHost(p->convertTo0to1(factoryPresets[n].values[i]));}
    }
    const juce::String getProgramName(int n)override{return n>=0&&n<getNumPrograms()?factoryPresets[n].name:juce::String{};};void changeProgramName(int,const juce::String&)override{}
    void prepareToPlay(double sr,int)override{core.prepare(sr);}
    void releaseResources()override{}
    bool isBusesLayoutSupported(const BusesLayout& l)const override{return l.getMainInputChannelSet()==juce::AudioChannelSet::stereo()&&l.getMainOutputChannelSet()==juce::AudioChannelSet::stereo();}
    void processBlock(juce::AudioBuffer<float>& b,juce::MidiBuffer&)override{
        juce::ScopedNoDenormals guard;
        core.set(31,state.getRawParameterValue("air_drive")->load());
        for(int i=0;i<core.count;++i)core.set(i,state.getRawParameterValue(core.keys[i])->load());core.apply();
        for(int i=0;i<b.getNumSamples();++i){auto y=core.processStereo(b.getSample(0,i),b.getSample(1,i));b.setSample(0,i,float(y[0]));b.setSample(1,i,float(y[1]));}core.tick(b.getNumSamples());
    }
    bool hasEditor()const override{return true;}
    juce::AudioProcessorEditor* createEditor()override{return new juce::GenericAudioProcessorEditor(*this);}
    void getStateInformation(juce::MemoryBlock& b)override{auto xml=state.copyState().createXml();copyXmlToBinary(*xml,b);}
    void setStateInformation(const void* d,int n)override{auto xml=getXmlFromBinary(d,n);if(xml&&xml->hasTagName(state.state.getType()))state.replaceState(juce::ValueTree::fromXml(*xml));}
};
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter(){return new Processor;}
