#include <iostream>
#include <RtWvOut.h>
#include <FileWvOut.h>
#include "Chapter1LabEffect.h"
#include "Rev.h"
#include "RevLP.h"
#include "FDNJot4LP.h"
#include "Stk.h"

int main() {
    stk::Stk::setSampleRate(44100.0);
    //stk::RtWvOut dac(1);
    stk::FileWvOut out("FDNJot4LPIR.wav", 1, stk::FileWrite::FILE_WAV);

    FDNJot4LP fdnJot4LP(1, 1687, 1601, 2053, 2251);

    std::cout << "Response: " << '\n';
    for (auto i = 0; i < 8 * stk::Stk::sampleRate(); i++) {
        const stk::StkFloat response = fdnJot4LP.tick(i == 0 ? 1 : 0); // impulse response
        //dac.tick(response);
        out.tick(response);
    }

    out.closeFile();

    return 0;
}
