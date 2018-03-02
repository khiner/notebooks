#include "Str.h"
#include <iostream>
#include <vector>


using std::cin; using std::cout; using std::endl;
using std::vector; using std::getline; using std::max;

// inlining to avoid dupe declarations and still allow Jupyter to access all definitions in header
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

Str::size_type width(const vector<Str>& v) {
    Str::size_type maxlen = 0;
    for (vector<Str>::const_iterator it = v.begin(); it != v.end(); it++) {
        maxlen = max(maxlen, it->size());
    }
    return maxlen;
}

vector<Str> frame(const vector<Str>& v) {
    vector<Str> ret;
    Str::size_type maxlen = width(v);
    Str border(maxlen + 4, '*');

    ret.push_back(border);

    for (vector<Str>::const_iterator it = v.begin(); it != v.end(); ++it) {
        ret.push_back("* " + *it + Str(maxlen - it->size(), ' ') + " *");
    }

    ret.push_back(border);
    return ret;
}

vector<Str> vcat(const vector<Str>& top,
                    const vector<Str>& bottom) {
    vector<Str> ret = top;
    ret.insert(ret.end(), bottom.begin(), bottom.end());
    return ret;
}

vector<Str> hcat(const vector<Str>& left,
                    const vector<Str>& right) {
    vector<Str> ret;

    Str::size_type width1 = width(left) + 1;
    vector<Str>::size_type i = 0, j = 0;

    while (i != left.size() || j != right.size()) {
        Str s;

        if (i != left.size()) {
            s = left[i++];
        }

        s += Str(width1 - s.size(), ' ');

        if (j != right.size()) {
            s += right[j++];
        }

        ret.push_back(s);
    }

    return ret;
}

int main() {
    Str s;
    while (getline(cin, s)) {
        vector<Str> v = split(s);

        vector<Str> framed = frame(v);
        vector<Str> f1 = vector<Str>(framed.begin(), framed.begin() + 2);
        vector<Str> f2 = vector<Str>(framed.begin() + 2, framed.end());
        cout << "Size 1: " << f1.size() << ";" << endl;

        vector<Str> hcatted = hcat(f1, f2);
        for (vector<Str>::iterator it = hcatted.begin(); it != hcatted.end(); ++it) {
            cout << *it << endl;
        }
    }

    return 0;
}
