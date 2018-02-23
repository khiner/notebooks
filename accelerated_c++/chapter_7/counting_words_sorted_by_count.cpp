#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::map;
using std::sort;
using std::string;
using std::vector;

int main() {
    string s;
    map<string, int> counters;

    while (cin >> s) {
        ++counters[s];
    }
    vector<int> counts;
    for (map<string, int>::const_iterator it = counters.begin(); it != counters.end(); ++it) {
        counts.push_back(it->second);
    }
    sort(counts.begin(), counts.end());

    for (vector<int>::const_iterator count_it = counts.begin(); count_it != counts.end(); ++count_it) {
        for (map<string, int>::const_iterator counter_it = counters.begin(); counter_it != counters.end(); ++counter_it) {
            if (counter_it->second == *count_it) {
                cout << counter_it->first << '\t' << counter_it->second << endl;
                break;
            }
        }
    }

    return 0;
}
