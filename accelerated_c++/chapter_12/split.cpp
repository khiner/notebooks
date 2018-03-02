#include "split.h"

#include <cctype>

using std::vector;

vector<Str> split(const Str& s) {
    vector<Str> ret;
    typedef Str::size_type Str_size;
    Str_size i = 0;

    while (i != s.size()) {
        while (i != s.size() && isspace(s[i])) {
            ++i;
        }

        Str_size j = i;

        while (j != s.size() && !isspace(s[j])) {
            ++j;
        }

        if (i != j) {
            ret.push_back(s.substr(i, j - i));
            i = j;
        }
    }

    return ret;
}
