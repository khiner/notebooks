#include <iostream>
#include <iomanip>
#include <cmath>

using std::cout; using std::endl; using std::setw;

// e.g. stringLengthOfInt(9999) => 4
// e.g. stringLengthOfInt(10000) => 5
int stringLengthOfInt(int i) {
    return (int) log10(i) + 1;
}

int main() {
    int maxValue = 1000;
    int maxValueStringLength = stringLengthOfInt(maxValue);
    int maxValueSquaredStringLength = stringLengthOfInt(maxValue * maxValue);

    for (int i = 0; i <= maxValue; i++) {
        cout << setw(maxValueStringLength + 1) << i << " " << setw(maxValueSquaredStringLength) << i * i << endl;
    }

    return 0;
}
