#include <iostream>
#include <RtWvOut.h>
#include <FileWvOut.h>
#include "Chapter1LabEffect.h"
#include "Rev.h"
#include "RevLP.h"
#include "FDNJot4.h"
#include "Stk.h"

int main() {
    stk::Stk::setSampleRate(44100.0);
    //stk::RtWvOut dac(1);
    stk::FileWvOut out("FDNJot4IR.wav", 1, stk::FileWrite::FILE_WAV);

    FDNJot4 fdnJot4(1, 1687, 1601, 2053, 2251);

    std::cout << "Response: " << '\n';
    for (auto i = 0; i < 4 * 44100; i++) {
        const stk::StkFloat response = fdnJot4.tick(i == 0 ? 1 : 0); // impulse response
        std::cout << response << '\n';
        //dac.tick(response);
        out.tick(response);
    }

    return 0;
}
