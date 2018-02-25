#include "../chapter_7/sentence_generator.h"

#include "../chapter_5/split.h"

#include <cstdlib>
#include <iostream>
#include <iterator>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using std::back_inserter;
using std::cin;
using std::cout;
using std::domain_error;
using std::endl;
using std::istream;
using std::getline;
using std::logic_error;
using std::ostream_iterator;
using std::map;
using std::rand;
using std::string;
using std::vector;

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

template <class Out> void gen_aux(const Grammar& g, const string& word, Out out) {
    if (!bracketed(word)) {
        *out++ = word;
    } else {
        Grammar::const_iterator it = g.find(word);
        if (it == g.end()) {
            throw logic_error("empty rule");
        }

        const Rule_collection& c = it->second;
        const Rule& r = c[nrand(c.size())];

        for (Rule::const_iterator i = r.begin(); i != r.end(); ++i) {
            gen_aux(g, *i, out);
        }
    }
}

template <class Out> void gen_sentence(const Grammar& g, Out out) {
    gen_aux(g, "<sentence>", out);
}

int main() {
    ostream_iterator<string> out_str (cout, " ");
    vector<string> out;

    const Grammar g = read_grammar(cin);
    gen_sentence(g, out_str);
    cout << endl;
    return 0;
}
