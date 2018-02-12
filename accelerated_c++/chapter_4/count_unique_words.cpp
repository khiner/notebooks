#include "read_into_vector.h"
#include <algorithm>

using std::vector; using std::cin; using std::cout; using std::string; using std::endl;

int main() {
    vector<string> vec;
    readIntoVector(cin, vec);

    sort(vec.begin(), vec.end()); // sort words lexicographically

    cout << endl;

    if (vec.size() == 0) {
        cout << "No input." << endl;
        return 1;
    }

    int repetitionCount;
    for (int i = 0; i < vec.size(); i++) {
        string& prevWord = vec[i];

        repetitionCount = 1;
        while (i + 1 < vec.size() && vec[i + 1] == prevWord) {
            repetitionCount++;
            i++;
        }

        cout << prevWord << " occurred " << repetitionCount << " times." << endl;
    }

    return 0;
}
