#include <iostream>
#include <RtWvOut.h>
#include <FileWvIn.h>
#include <FileWvOut.h>
#include "Chapter1LabEffect.h"
#include "Rev.h"
#include "RevLP.h"
#include "FDNJot4.h"
#include "FDNJot4LP.h"
#include "Stk.h"

int main() {
    stk::Stk::setSampleRate(44100.0);
    //stk::RtWvOut dac(1);
    stk::FileWvOut out("FDNJot4IR-speech-male.wav", 1, stk::FileWrite::FILE_WAV);

    stk::FileWvIn in("speech-male.wav");
    FDNJot4 fdnJot4(1.0, 1687, 1601, 2053, 2251);

    std::cout << "Response: " << '\n';
    for (auto i = 0; i < 8 * stk::Stk::sampleRate(); i++) {
        //auto inSample = i == 0 ? 1 : 0; // impulse response
        auto inSample = in.tick(0);
        const stk::StkFloat response = fdnJot4.tick(inSample * 0.10);
        //dac.tick(response);
        out.tick(response);
    }

    out.closeFile();

    return 0;
}
