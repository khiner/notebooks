#include "read_into_vector.h"

using std::vector; using std::cin; using std::cout; using std::string; using std::endl;

int main() {
    vector<string> vec;
    readIntoVector(cin, vec);

    cout << endl << "Word count: " << vec.size() << endl;

    return 0;
}
