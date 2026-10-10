cmake_minimum_required(VERSION 3.22)
project(PulyTek VERSION 0.1.0 LANGUAGES C CXX)
set(CMAKE_CXX_STANDARD 17)
include(FetchContent)
# Optional Linux VST3 target. Force/MPC uses build.sh, not this target.
FetchContent_Declare(JUCE GIT_REPOSITORY https://github.com/juce-framework/JUCE.git
    GIT_TAG 4f43011b96eb0636104cb3e433894cda98243626)
FetchContent_MakeAvailable(JUCE)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
execute_process(COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tools/vst3_params.py
    ${CMAKE_CURRENT_BINARY_DIR}/parameter_layout.h COMMAND_ERROR_IS_FATAL ANY)
juce_add_plugin(PulyTek COMPANY_NAME MagicStino PLUGIN_MANUFACTURER_CODE MgSt PLUGIN_CODE EqF1
    FORMATS VST3 PRODUCT_NAME PulyTek IS_SYNTH FALSE NEEDS_MIDI_INPUT FALSE NEEDS_MIDI_OUTPUT FALSE
    VST3_CATEGORIES Fx EQ COPY_PLUGIN_AFTER_BUILD FALSE)
target_sources(PulyTek PRIVATE linux-vst3/processor.cpp src/upstream/EQP1A.cpp)
target_include_directories(PulyTek PRIVATE src ${CMAKE_CURRENT_BINARY_DIR})
target_compile_definitions(PulyTek PUBLIC JUCE_WEB_BROWSER=0 JUCE_USE_CURL=0 JUCE_VST3_CAN_REPLACE_VST2=0)
target_link_libraries(PulyTek PRIVATE juce::juce_audio_utils PUBLIC juce::juce_recommended_config_flags)
