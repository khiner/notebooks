#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <ctime>

using std::cout;
using std::domain_error;
using std::endl;
using std::rand;
using std::srand;
using std::time;

// For simplicity, assume RAND_MAX = 4 and n = 13. We want a result in the range [0, 13) = [0, 12].
// Then the result will be the sum of four uniform samples:
//   * three in the range [0, 4) = [0, 3], and
//   * one in the range [0, 13 % 4 + nDraws) = [0, 1 + 4) = [0, 4) = [0, 4]. Thus, the total range will be [0, 3 * 3 + 4] = [0, 13]
int nrand(int n) {
    if (n <= 0 || n > INT_MAX) {
        throw domain_error("Argument to nrand is out of range");
    }

    // Break up rand generation into sums of uniform random samples in range [0, min(n, RAND_MAX)).
    int numDraws = n == INT_MAX ? 1 : 1 + n / RAND_MAX;

    int r;
    int drawNum = 0;
    for (drawNum = 0; drawNum < numDraws; drawNum++) {
        // n for this draw is either the full range [0, RAND_MAX) or [0, n % RAND_MAX) if this is the last draw.
        // + nDraws is needed because each draw is right-exclusive in its range.
        int drawN = drawNum == numDraws - 1 && n != RAND_MAX ? (n % RAND_MAX) + numDraws : RAND_MAX;
        int draw;
        do {
            draw = (rand() / (RAND_MAX / drawN));
        } while (draw >= drawN);

        r += draw;
    }
    return r;
}

int main() {
    srand(time(0));
    rand();
    cout << nrand(INT_MAX);
    return 0;
}
