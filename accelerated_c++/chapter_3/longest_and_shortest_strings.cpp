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

    string::size_type longestStringLength = 0;
    string::size_type shortestStringLength = 0; // max value hasn't been introduced yet, otherwise that would be more idiomatic

    string word;
    while (cin >> word) {
        string::size_type size = word.size();
        if (size > longestStringLength) {
            longestStringLength = size;
        } 
        if (size < shortestStringLength || shortestStringLength == 0) {
            shortestStringLength = size;
        }
    }

    cout << "Longest string length: " << longestStringLength << ". Shortest string length: " << shortestStringLength << endl;

    return 0;
}
