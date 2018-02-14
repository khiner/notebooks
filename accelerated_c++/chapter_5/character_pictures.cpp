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

vector<string> vcat(const vector<string>& top,
                    const vector<string>& bottom) {
    vector<string> ret = top;
    ret.insert(ret.end(), bottom.begin(), bottom.end());
    return ret;
}

vector<string> hcat(const vector<string>& left,
                    const vector<string>& right) {
    vector<string> ret;

    string::size_type width1 = width(left) + 1;
    vector<string>::size_type i = 0, j = 0;

    while (i != left.size() || j != right.size()) {
        string s;

        if (i != left.size()) {
            s = left[i++];
        }

        s += string(width1 - s.size(), ' ');

        if (j != right.size()) {
            s += right[j++];
        }

        ret.push_back(s);
    }

    return ret;
}

int main() {
    string s;
    while (getline(cin, s)) {
        vector<string> v = split(s);

        vector<string> framed = frame(v);
        vector<string> f1 = vector<string>(framed.begin(), framed.begin() + 2);
        vector<string> f2 = vector<string>(framed.begin() + 2, framed.end());
        cout << "Size 1: " << f1.size() << ";" << endl;

        vector<string> hcatted = hcat(f1, f2);
        for (vector<string>::iterator it = hcatted.begin(); it != hcatted.end(); ++it) {
            cout << *it << endl;
        }
    }

    return 0;
}
