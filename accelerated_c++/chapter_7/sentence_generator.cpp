#include "../chapter_5/split.h"

#include <cstdlib>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using std::cin;
using std::cout;
using std::domain_error;
using std::endl;
using std::istream;
using std::getline;
using std::logic_error;
using std::map;
using std::rand;
using std::string;
using std::vector;

typedef vector<string> Rule;
typedef vector<Rule> Rule_collection;
typedef map<string, Rule_collection> Grammar;

Grammar read_grammar(istream& in) {
    Grammar ret;
    string line;

    while (getline(in, line)) {
        vector<string> entry = split(line);

        if (!entry.empty()) {
            ret[entry[0]].push_back(Rule(entry.begin() + 1, entry.end()));
        }
    }
    return ret;
}

bool bracketed(const string& s) {
    return s.size() > 1 && s[0] == '<' && s[s.size() - 1] == '>';
}

int nrand(int n) {
    if (n <= 0 || n > RAND_MAX) {
        throw domain_error("Argument to nrand is out of range");
    }

    const int bucket_size = RAND_MAX / n;
    int r;

    do {
        r = rand() / bucket_size;
    } while (r >= n);

    return r;
}

void gen_aux(const Grammar& g, const string& word, vector<string>& ret) {
    if (!bracketed(word)) {
        ret.push_back(word);
    } else {
        Grammar::const_iterator it = g.find(word);
        if (it == g.end()) {
            throw logic_error("empty rule");
        }

        const Rule_collection& c = it->second;
        const Rule& r = c[nrand(c.size())];

        for (Rule::const_iterator i = r.begin(); i != r.end(); ++i) {
            gen_aux(g, *i, ret);
        }
    }
}

vector<string> gen_sentence(const Grammar& g) {
    vector<string> ret;
    gen_aux(g, "<sentence>", ret);
    return ret;
}

int main() {
    vector<string> sentence = gen_sentence(read_grammar(cin));

    vector<string>::const_iterator it = sentence.begin();
    if (!sentence.empty()) {
        cout << *it;
        ++it;
    }

    while (it != sentence.end()) {
        cout << " " << *it;
        ++it;
    }

    cout << endl;
    return 0;
}
