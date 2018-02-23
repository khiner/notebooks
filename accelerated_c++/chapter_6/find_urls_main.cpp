#include "find_urls.h"

#include <iostream>
#include <string>
#include <vector>

using std::cout; using std::endl; using std::vector;
using std::string;


int main() {
    const string s = "blah blah http://localhost:8888/notebooks/accelerated_c%2B%2B/chapter_6/chapter_6.ipynb blah blah https://www.khanacademy.org/math/statistics-probability blahhhhhh";

    const vector<string> urls = find_urls(s);
    for (vector<string>::const_iterator it = urls.begin(); it != urls.end(); ++it) {
        cout << *it << endl;
    }
    return 0;
}
