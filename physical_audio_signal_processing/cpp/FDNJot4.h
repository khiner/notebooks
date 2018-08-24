#ifndef FDNJOT4_H
#define FDNJOT4_H

#include <Effect.h>
#include <Delay.h>

class FDNJot4 : public stk::Effect {
    const stk::StkFloat g;
    const stk::StkFloat b1 = 1, b2 = 1, b3 = 1, b4 = 1;
    const stk::StkFloat c1 = 1, c2 = 1, c3 = 1, c4 = 1;
    stk::Delay d1, d2, d3, d4;
    stk::StkFloat
            x1 = 0, x2 = 0, x3 = 0, x4 = 0, // scratch variables
            d1Out = 0, d2Out = 0, d3Out = 0, d4Out = 0; // scratch variables

public:
    FDNJot4(const stk::StkFloat g,
            const unsigned long M1,
            const unsigned long M2,
            const unsigned long M3,
            const unsigned long M4)
            : g(g) {
        d1 = stk::Delay(M1, M1);
        d2 = stk::Delay(M2, M2);
        d3 = stk::Delay(M3, M3);
        d4 = stk::Delay(M4, M4);
    }

    inline stk::StkFloat tick(const stk::StkFloat u) {
        d1Out = d1.nextOut();
        d2Out = d2.nextOut();
        d3Out = d3.nextOut();
        d4Out = d4.nextOut();

        x1 = u * b1 + computeAForRow(0, d1Out, d2Out, d3Out, d4Out);
        x2 = u * b2 + computeAForRow(1, d1Out, d2Out, d3Out, d4Out);;
        x3 = u * b3 + computeAForRow(2, d1Out, d2Out, d3Out, d4Out);
        x4 = u * b4 + computeAForRow(3, d1Out, d2Out, d3Out, d4Out);;

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
private:

    // Calculate one row-multiply for our specific FDN "A" matrix
    // (more efficient than implementing the matrix directly).
    inline stk::StkFloat computeAForRow(const unsigned int rowIndex,
                                        const stk::StkFloat i1,
                                        const stk::StkFloat i2,
                                        const stk::StkFloat i3,
                                        const stk::StkFloat i4) const {
        if (rowIndex == 0) {
            return g * (0.5 * i1 - 0.5 * i2 - 0.5 * i3 - 0.5 * i4);
        } else if (rowIndex == 1) {
            return g * (-0.5 * i1 + 0.5 * i2 - 0.5 * i3 - 0.5 * i4);
        } else if (rowIndex == 2) {
            return g * (-0.5 * i1 - 0.5 * i2 + 0.5 * i3 - 0.5 * i4);
        } else {
            return g * (-0.5 * i1 - 0.5 * i2 - 0.5 * i3 + 0.5 * i4);
        }
    }
};

#endif //FDNJOT4_H
