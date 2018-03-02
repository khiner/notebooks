#include "split.h"

#include <iostream>
#include <string>
#include "../Vec.h"

using std::string; using std::cin; using std::cout; using std::endl;
using std::getline; using std::max;

string::size_type width(const Vec<string>& v) {
    string::size_type maxlen = 0;
    for (Vec<string>::const_iterator it = v.begin(); it != v.end(); it++) {
        maxlen = max(maxlen, it->size());
    }
    return maxlen;
}

Vec<string> frame(const Vec<string>& v) {
    Vec<string> ret;
    string::size_type maxlen = width(v);
    string border(maxlen + 4, '*');

    ret.push_back(border);

    for (Vec<string>::const_iterator it = v.begin(); it != v.end(); ++it) {
        ret.push_back("* " + *it + string(maxlen - it->size(), ' ') + " *");
    }

    ret.push_back(border);
    return ret;
}

Vec<string> vcat(const Vec<string>& top,
                    const Vec<string>& bottom) {
    Vec<string> ret = top;

    for (Vec<string>::const_iterator it = bottom.begin(); it != bottom.end(); ++it) {
        ret.push_back(*it);
    }

    return ret;
}

Vec<string> hcat(const Vec<string>& left,
                    const Vec<string>& right) {
    Vec<string> ret;

    string::size_type width1 = width(left) + 1;
    Vec<string>::size_type i = 0, j = 0;

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
        Vec<string> v = split(s);

        Vec<string> framed = frame(v);
        Vec<string> f1 = Vec<string>(framed.begin(), framed.begin() + 2);
        Vec<string> f2 = Vec<string>(framed.begin() + 2, framed.end());
        cout << "Size 1: " << f1.size() << ";" << endl;

        Vec<string> hcatted = hcat(f1, f2);
        for (Vec<string>::iterator it = hcatted.begin(); it != hcatted.end(); ++it) {
            cout << *it << endl;
        }
    }

    return 0;
}
