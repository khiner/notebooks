#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using std::cin; using std::cout; using std::isupper;
using std::endl; using std::string; using std::vector;

bool isPalindrome(const string& s) {
    for (string::size_type i = 0; i < s.size() / 2; i++) {
        if (s[i] != s[s.size() - i - 1]) {
            return false;
        }
    }
    return true;
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

    vector<string> palindromes;

    while (cin >> s) {
        if (isPalindrome(s)) {
            palindromes.push_back(s);
        }
    }

    cout << "All palindromes:" << endl << endl;

    for (vector<string>::const_iterator iter = palindromes.begin(); iter < palindromes.end(); iter++) {
        cout << *iter << endl;
    }

    cout << endl << "Longest palindrome:" << endl << findLongest(palindromes) << endl;

    return 0;
}
