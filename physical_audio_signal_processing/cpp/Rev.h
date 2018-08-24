#ifndef REV_H
#define REV_H

#include <Effect.h>
#include <BiQuad.h>

// This is for the Allpass Lab problem 2 in chapter 2
class Rev : public stk::Effect {
    stk::StkFloat g;
    stk::StkFloat vp = 0, v = 0, y = 0; // state-variables

public:
    explicit Rev(const stk::StkFloat g): g(g) {
    }

    inline stk::StkFloat tick(const stk::StkFloat x)  {
        v = x - g * vp;
        y = g * v + vp;
        vp = v;
        return y;
    }

    //! Reset and clear all internal state.
    void clear() override {
        // no-op.
    }

    //! Set the mixture of input and "effected" levels in the output (0.0 = input only, 1.0 = effect only).
    void setEffectMix( stk::StkFloat mix ) override {
        // no-op.
    }
};

#endif //REV_H
