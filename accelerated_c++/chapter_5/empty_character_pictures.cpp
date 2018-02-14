#include "split.h"

#include <iostream>
#include <string>
#include <vector>

using std::string; using std::cin; using std::cout; using std::endl;
using std::vector; using std::getline; using std::max;

string::size_type width(const vector<string>& v) {
    string::size_type maxlen = 0;
    for (vector<string>::const_iterator it = v.begin(); it != v.end(); it++) {
        maxlen = max(maxlen, it->size());
    }
    return maxlen;
}

vector<string> frame(const vector<string>& v) {
    vector<string> ret;
    string::size_type maxlen = width(v);
    string border(maxlen + 4, '*');

    ret.push_back(border);

    for (vector<string>::const_iterator it = v.begin(); it != v.end(); ++it) {
        ret.push_back("* " + *it + string(maxlen - it->size(), ' ') + " *");
    }

    ret.push_back(border);

    return ret;
}

int main() {
    vector<string> v;
    vector<string> framed = frame(v);

    for (vector<string>::const_iterator it = framed.begin(); it != framed.end(); ++it) {
        cout << *it << endl;
    }
    return 0;
}
