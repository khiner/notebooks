#include "split.h"

#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using std::cout; using std::endl; using std::max; using std::setw;
using std::sort; using std::string; using std::vector;

struct IndexPermutation {
    string index;
    string phrase;
};

bool comparePermutations(const IndexPermutation& x, const IndexPermutation& y) {
    return x.phrase < y.phrase;
}

string::size_type indexWidth(const vector<IndexPermutation>& v) {
    string::size_type maxlen = 0;
    for (vector<IndexPermutation>::const_iterator it = v.begin(); it != v.end(); it++) {
        maxlen = max(maxlen, it->index.size());
    }
    return maxlen;
}

vector<IndexPermutation> permutationsForLine(const string& line) {
    vector<string> words = split(line);

    vector<IndexPermutation> allPermutations;
    for (int pivotIndex = 0; pivotIndex != words.size(); pivotIndex++) {
        IndexPermutation indexPermutation;
        indexPermutation.index = "";
        indexPermutation.phrase = "";

        for (int i = 0; i < words.size(); i++) {
            if (i < pivotIndex) {
                indexPermutation.index += words[i] + " ";
            } else {
                indexPermutation.phrase += words[i] + " ";
            }
        }
        allPermutations.push_back(indexPermutation);
    }

    return allPermutations;
}

int main() {
    vector<string> lines;
    lines.push_back("the quick brown fox");
    lines.push_back("jumped over the fence");

    vector<IndexPermutation> allPermutations;
    for (vector<string>::const_iterator it = lines.begin(); it != lines.end(); it++) {
        vector<IndexPermutation> linePermutations = permutationsForLine(*it);
        allPermutations.insert(allPermutations.end(), linePermutations.begin(), linePermutations.end());
    }

    sort(allPermutations.begin(), allPermutations.end(), comparePermutations);

    string::size_type width = indexWidth(allPermutations);
    for (vector<IndexPermutation>::const_iterator it = allPermutations.begin(); it < allPermutations.end(); it++) {
        cout << string(width - it->index.size(), ' ') << it->index << "    " << it->phrase << endl;
    }
    return 0;
}