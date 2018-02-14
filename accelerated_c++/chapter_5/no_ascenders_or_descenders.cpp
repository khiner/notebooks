#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using std::cin; using std::cout; using std::isupper;
using std::endl; using std::string; using std::vector;

bool hasAscendersOrDescenders(const string& s) {
    for (string::size_type i = 0; i < s.size(); i++) {
        char c = s[i];
        if (c == 'b' || c == 'd' || c == 'f' || c == 'h' ||
            c == 'k' || c == 'l' || c == 't' || c == 'g' ||
            c == 'j' || c == 'p' || c == 'q' || c == 'y') {
            return true;
        }
    }
    return false;
}

string findLongest(const vector<string>& v) {
    string::size_type maxLength = 0;
    string maxLengthString;
    for (vector<string>::const_iterator iter = v.begin(); iter < v.end(); iter++) {
        if (iter->size() > maxLength) {
            maxLength = iter->size();
            maxLengthString = *iter;
        }
    }

    return maxLengthString;
}

int main() {
    string s;

    vector<string> noAscendersOrDescenders;

    while (cin >> s) {
        if (!hasAscendersOrDescenders(s)) {
            noAscendersOrDescenders.push_back(s);
        }
    }

    cout << endl << "Longest word with no ascenders or descenders:" << endl << findLongest(noAscendersOrDescenders) << endl;

    return 0;
}
