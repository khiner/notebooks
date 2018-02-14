#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using std::cin; using std::cout; using std::isupper;
using std::endl; using std::string; using std::vector;

bool containsUppercaseLetter(const string& s) {
    for (string::const_iterator iter = s.begin(); iter < s.end(); iter++) {
        if (isupper(*iter)) {
            return true;
        }
    }
    return false;
}

int main() {
    string s;

    vector<string> wordsNotContianingUppercase;
    vector<string> wordsContianingUppercase;

    while (cin >> s) {
        if (containsUppercaseLetter(s)) {
            wordsContianingUppercase.push_back(s);
        } else {
            wordsNotContianingUppercase.push_back(s);
        }
    }

    for (vector<string>::const_iterator iter = wordsNotContianingUppercase.begin(); iter < wordsNotContianingUppercase.end(); iter++) {
        cout << *iter << endl;
    }
    for (vector<string>::const_iterator iter = wordsContianingUppercase.begin(); iter < wordsContianingUppercase.end(); iter++) {
        cout << *iter << endl;
    }
    return 0;
}
