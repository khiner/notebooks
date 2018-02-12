#include <iostream>
#include <iomanip>

using std::cout; using std::endl; using std::setw;

int main() {
    int maxValue = 100;

    for (int i = 0; i <= maxValue; i++) {
        cout << setw(4) << i << " " << setw(6) << i * i << endl;
    }

    return 0;
}
