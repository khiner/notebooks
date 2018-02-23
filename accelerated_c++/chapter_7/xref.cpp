#include "../chapter_5/split.h"
#include "../chapter_6/find_urls.h"

#include <iostream>
#include <map>
#include <string>
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::istream;
using std::getline;
using std::map;
using std::string;
using std::vector;


// returns the iterator at the first position in `ints` where `i` is found,
// or `ints.end()` if `i` is not found.
vector<int>::const_iterator find(const vector<int>& ints, int i) {
    for (vector<int>::const_iterator it = ints.begin(); it != ints.end(); ++it) {
        if (*it == i) {
            return it;
        }
    }
    return ints.end();
}

map<string, vector<int> > xref(istream& in,
                               vector<string> find_words(const string&) = split) {
    string line;
    map<string, vector<int> > ret;

    int line_number = 0;
    while (getline(in, line)) {
        ++line_number;

        vector<string> words = find_words(line);

        for (vector<string>::const_iterator it = words.begin(); it != words.end(); ++it) {
            vector<int>& line_numbers = ret[*it];
            if (find(line_numbers, line_number) == line_numbers.end()) {
                line_numbers.push_back(line_number);
            }
        }
    }
    return ret;
}

int main() {
    static int numbers_per_line = 20;
    string occurs_on_line_message;
    map<string, vector<int> > ret = xref(cin, find_urls);

    for (map<string, vector<int> >::const_iterator it = ret.begin(); it != ret.end(); ++it) {
        occurs_on_line_message = string(" occurs on line") + (it->second.size() > 1 ? "s: " : ": ");
        cout << it->first << occurs_on_line_message;

        vector<int>::const_iterator line_it = it->second.begin();
        int printed_numbers = 0;
        while (line_it != it->second.end()) {
            cout << *line_it;
            if (line_it != it->second.end() - 1) {
                cout  << ", ";
            }
            if (++printed_numbers % (numbers_per_line - 1) == 0) {
                cout << endl << string(occurs_on_line_message.size() + 1, ' ');
            }

            ++line_it;
        }

        cout << endl;
    }

    return 0;
}
