#ifndef CPP_CHAPTER1LABEFFECT_H
#define CPP_CHAPTER1LABEFFECT_H

#include <Effect.h>
#include <BiQuad.h>

class Chapter1LabEffect : public stk::Effect {
    stk::BiQuad biQuad;

    double T = 0.1;
    double mass = 1.0;
    double k = 100 * stk::PI;

public:
    Chapter1LabEffect() {
        // TODO not confident about these parameters/discrete derivation.
        biQuad.setB0(0);
        biQuad.setB1(T/mass);
        biQuad.setA1(-1);
        biQuad.setA2(T * T * k/mass);
    }

    // Takes force input, returns mass velocity
    inline stk::StkFloat tick(stk::StkFloat force)  {
        return biQuad.tick(force);
    }

    //! Reset and clear all internal state.
    void clear() override {
        biQuad.clear();
    }

    //! Set the mixture of input and "effected" levels in the output (0.0 = input only, 1.0 = effect only).
    void setEffectMix( stk::StkFloat mix ) override {
        // no-op.
    }
};

#endif //CPP_CHAPTER1LABEFFECT_H
