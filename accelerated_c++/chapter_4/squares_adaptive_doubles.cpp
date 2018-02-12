#include <iostream>
#include <iomanip>
#include <cmath>

using std::cout; using std::endl; using std::setw; using std::setprecision;

// e.g. stringLengthOfInt(9999) => 4
// e.g. stringLengthOfInt(10000) => 5
int stringLengthOfInt(int i) {
    return (int) log10(i) + 1;
}

int main() {
    double maxValue = 100.0;

    int maxValueStringLength = stringLengthOfInt(maxValue * maxValue) + 2;
    int maxValueSquaredStringLength = stringLengthOfInt(maxValue * maxValue) + 2;

    for (double i = 0; i <= maxValue; i += 0.1) {
        cout << setprecision(maxValueStringLength) << setw(maxValueStringLength + 1) << i << " "
             << setprecision(maxValueSquaredStringLength) << setw(maxValueSquaredStringLength) << i * i << endl;
    }

    return 0;
}
