#include <iostream>
#include "Chapter1LabEffect.h"

int main() {
    Chapter1LabEffect chapter1LabEffect;

    const stk::StkFloat impulse[10] = {1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    for (const stk::StkFloat sample : impulse) {
        stk::StkFloat massVelocity = chapter1LabEffect.tick(sample);
        std::cout << "Mass velocity: " << massVelocity << '\n';
    }
    return 0;
}
