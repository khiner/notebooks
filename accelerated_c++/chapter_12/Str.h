#ifndef GUARD_Str_h
#define GUARD_Str_h

#include "../chapter_11/Vec.h"
#include <iostream>
#include <cctype>
#include <cstring>

class Str {
    friend std::istream& operator>>(std::istream& is, Str& s) {
        s.dat.clear();

        char c;
        while (is.get(c) && std::isspace(c));

        if (is) {
            do s.dat.push_back(c);
            while (is.get(c) && !isspace(c));

            if (is)
                is.unget();
        }
        return is;
    }

    friend std::istream& getline(std::istream& is, Str& s) {
        s.dat.clear();

        char c;
        while (is.get(c) && std::isspace(c));

        if (is) {
            do s.dat.push_back(c);
            while (is.get(c) && c != '\n');

            if (is)
                is.unget();
        }
        return is;
    }

public:
    bool operator<(const Str& s) {
        return str_cmp(s) < 0;
    }

    bool operator>(const Str& s) {
        return str_cmp(s) > 0;
    }

    bool operator==(const Str& s) {
        return str_cmp(s) == 0;
    }

    bool operator!=(const Str& s) {
        return !(*this == s);
    }

    Str& operator+=(const Str& s) {
        std::copy(s.dat.begin(), s.dat.end(), std::back_inserter(dat));
        return *this;
    }

    Str& operator+=(const char* p) {
        std::copy(p, p + std::strlen(p), std::back_inserter(dat));
        return *this;
    }

    operator bool() {
        return size() == 0;
    }

    typedef Vec<char>::size_type size_type;
    typedef char* iterator;
    typedef const char* const_iterator;

    Str() { }
    Str(size_type n, char c): dat(n, c) { }
    Str(const char* cp) {
        std::copy(cp, cp + std::strlen(cp), std::back_inserter(dat));
    }
    template <class In> Str(In b, In e) : dat(b, e) { }

    char& operator[](size_type i) { return dat[i]; }
    const char& operator[](size_type i) const { return dat[i]; }
    size_type size() const { return dat.size(); }
    const char* c_str() {
        delete[] c_str_data;
        c_str_data = new char[dat.size() + 1];
        for (size_type i = 0; i != dat.size(); ++i) {
            c_str_data[i] = dat[i];
        }
        c_str_data[dat.size()] = '\0';
        return c_str_data;
    }

    const char* data() {
        return c_str();
    }

    void copy(char* p, size_type n) const {
        std::copy(dat.begin(), dat.begin() + n, p);
    }

    Str substr(int i, int j) const {
        Str sub(begin() + i, begin() + i + j);
        return sub;
    }

    iterator begin() {
        return dat.begin();
    }

    iterator end() {
        return dat.end();
    }

    const_iterator begin() const {
        return dat.begin();
    }

    const_iterator end() const {
        return dat.end();
    }


    template <class In> void insert (iterator position, In b, In e) {
        dat.insert(position, b, e);
    }

private:
    Vec<char> dat;
    char* c_str_data;

    int str_cmp(const Str& s) {
        char* s_copy = new char[s.size() + 1]; // can't use c_str() since it modifies a member
        s.copy(s_copy, s.size());
        s_copy[s.size()] = '\0';
        int ret = std::strcmp(c_str(), s_copy);
        delete[] s_copy;
        return ret;
    }
};

std::ostream& operator<<(std::ostream& os, const Str& s) {
    std::ostream_iterator<char> iter(os);
    for (Str::size_type i = 0; i != s.size(); ++i) {
        *iter++ = s[i];
    }
    return os;
}

Str operator+(const Str& s, const Str& t) {
    Str r = s;
    r += t;
    return r;
}

Str operator+(const Str& s, const char* p) {
    Str r = s;
    r += p;
    return r;
}

#endif
