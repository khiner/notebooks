#ifndef REVLP_H
#define REVLP_H

#include <Effect.h>
#include <BiQuad.h>

// This is for the Allpass Lab problem 2 in chapter 2
class RevLP : public stk::Effect {
    stk::StkFloat g; // lattice filter coefficient
    stk::StkFloat a; // feedback LP coefficient
    stk::StkFloat vp = 0, v = 0, y = 0; // state-variables
    stk::StkFloat lpyp = 0; // y(n-1) state variable for feedback LP component

public:
    RevLP(const stk::StkFloat g, const stk::StkFloat a): g(g), a(a) {
    }

    inline stk::StkFloat tick(const stk::StkFloat x)  {
        // lattice filter section
        v = x - g * vp;
        y = g * v + vp;

        // feedback LP section
        vp = (1 - a) * v + a * lpyp;
        lpyp = vp;

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

#endif //REVLP_H
