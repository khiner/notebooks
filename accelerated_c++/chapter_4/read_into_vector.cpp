#include "read_into_vector.h"
#include <string>

using std::istream; using std::vector; using std::string;

istream& readIntoVector(istream& is, vector<string>& vec) {
    if (is) {
        is.clear();
        string str;
        while (is >> str) {
            // intentionally not clearing vec
            vec.push_back(str);
        }
    }

    return is;
}
