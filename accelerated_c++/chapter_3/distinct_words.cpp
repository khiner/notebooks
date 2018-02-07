#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <string>
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::find;
using std::string;
using std::vector;

int main() {
    cout << "Please enter some words, and enter ctrl+d when done." << endl;

    vector<string> distinctWords;
    string word;
    while (cin >> word) {
        if (find(distinctWords.begin(), distinctWords.end(), word) == distinctWords.end()) {
            distinctWords.push_back(word);
        }
    }

    cout << "Distinct words: " << distinctWords.size() << endl;

    return 0;
}
