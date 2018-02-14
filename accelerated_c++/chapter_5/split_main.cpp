#include "split.h"

#include <iostream>
#include <string>
#include <vector>

using std::string; using std::cin; using std::cout; using std::endl;
using std::vector; using std::getline;

int main() {
    string s;
    while (getline(cin, s)) {
        vector<string> v = split(s);

        for (vector<string>::iterator it = v.begin(); it != v.end(); ++it) {
            cout << *it << endl;
        }
    }

    return 0;
}