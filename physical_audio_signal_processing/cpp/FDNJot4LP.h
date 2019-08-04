#ifndef FDNJOT4LP_H
#define FDNJOT4LP_H

#include <Effect.h>
#include <Delay.h>
#include <OnePole.h>

class FDNJot4LP : public stk::Effect {
    const stk::StkFloat g;
    const stk::StkFloat b1 = 1, b2 = 1, b3 = 1, b4 = 1;
    const stk::StkFloat c1 = 1, c2 = 1, c3 = 1, c4 = 1;
    const stk::StkFloat t60DC = 5, t60HalfSamplingRate = 8; // desired decay time for 0 rad/sec & pi rad/sec

    stk::Delay d1, d2, d3, d4;
    stk::StkFloat
            x1 = 0, x2 = 0, x3 = 0, x4 = 0, // scratch variables
            d1Out = 0, d2Out = 0, d3Out = 0, d4Out = 0; // scratch variables
    stk::StkFloat g1 = 0, g2 = 0, g3 = 0, g4 = 0; // gain for each filter
    stk::StkFloat p1 = 0, p2 = 0, p3 = 0, p4 = 0; // poles for each filter
    stk::OnePole f1, f2, f3, f4; // one-pole filter for each delay line

public:
    FDNJot4LP(const stk::StkFloat g,
            const unsigned long M1,
            const unsigned long M2,
            const unsigned long M3,
            const unsigned long M4)
            : g(g) {
        d1 = stk::Delay(M1, M1);
        d2 = stk::Delay(M2, M2);
        d3 = stk::Delay(M3, M3);
        d4 = stk::Delay(M4, M4);

        g1 = calculateFilterGain(t60DC, M1);
        g2 = calculateFilterGain(t60DC, M2);
        g3 = calculateFilterGain(t60DC, M3);
        g4 = calculateFilterGain(t60DC, M4);

        p1 = calculateFilterPole(g1, t60DC, t60HalfSamplingRate);
        p2 = calculateFilterPole(g2, t60DC, t60HalfSamplingRate);
        p3 = calculateFilterPole(g3, t60DC, t60HalfSamplingRate);
        p4 = calculateFilterPole(g4, t60DC, t60HalfSamplingRate);

        f1 = stk::OnePole(p1);
        f2 = stk::OnePole(p2);
        f3 = stk::OnePole(p3);
        f4 = stk::OnePole(p4);
    }

    inline stk::StkFloat tick(const stk::StkFloat u) {
        d1Out = g1 * f1.tick(d1.nextOut());
        d2Out = g2 * f2.tick(d2.nextOut());
        d3Out = g3 * f3.tick(d3.nextOut());
        d4Out = g4 * f4.tick(d4.nextOut());

        x1 = u * b1 + computeAForRow(0, d1Out, d2Out, d3Out, d4Out);
        x2 = u * b2 + computeAForRow(1, d1Out, d2Out, d3Out, d4Out);
        x3 = u * b3 + computeAForRow(2, d1Out, d2Out, d3Out, d4Out);
        x4 = u * b4 + computeAForRow(3, d1Out, d2Out, d3Out, d4Out);

        return c1 * d1.tick(x1) + c2 * d2.tick(x2) + c3 * d3.tick(x3) + c4 * d4.tick(x4);
    }

    //! Reset and clear all internal state.
    void clear() override {
        // no-op.
    }

    //! Set the mixture of input and "effected" levels in the output (0.0 = input only, 1.0 = effect only).
    void setEffectMix( stk::StkFloat mix ) override {
        // no-op.
    }

    static stk::StkFloat calculateFilterGain(const stk::StkFloat t60DC, const unsigned long delaySamples) {
        return pow(10, -3 * (stk::StkFloat(delaySamples) / stk::StkFloat(Stk::sampleRate())) / t60DC);
    }

    static stk::StkFloat calculateFilterPole(stk::StkFloat g, stk::StkFloat t60DC, stk::StkFloat t60HalfSamplingRate) {
        return (log(10) / 4.0) * log10(g) * (1.0 - (1.0 / pow(t60HalfSamplingRate / t60DC, 2)));
    }

private:

    // Calculate one row-multiply for our specific FDN "A" matrix
    // (more efficient than implementing the matrix directly).
    inline stk::StkFloat computeAForRow(const unsigned int rowIndex,
                                        const stk::StkFloat i1,
                                        const stk::StkFloat i2,
                                        const stk::StkFloat i3,
                                        const stk::StkFloat i4) const {
        if (rowIndex == 0) {
            return g * 0.5 * (i1 - i2 - i3 - i4);
        } else if (rowIndex == 1) {
            return g * 0.5 * (-i1 + i2 - i3 - i4);
        } else if (rowIndex == 2) {
            return g * 0.5 * (-i1 - i2 + i3 - i4);
        } else {
            return g * 0.5 * (-i1 - i2 - i3 + i4);
        }
    }
};

#endif //FDNJOT4LP_H
