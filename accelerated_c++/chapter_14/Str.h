#ifndef GUARD_Str_h
#define GUARD_Str_h

#include "Ptr.h"
#include "../chapter_11/Vec.h"
#include <algorithm>
#include <iostream>
#include <iterator>

template <> Vec<char>* clone(const Vec<char>* vp) {
    return new Vec<char>(*vp);
}

class Str {
    friend std::istream& operator>>(std::istream&, Str&);

public:
    typedef Vec<char>::size_type size_type;
    typedef char* iterator;
    typedef const char* const_iterator;

    Str& operator+=(const Str& s) {
        data.make_unique();
        std::copy(s.data->begin(), s.data->end(), std::back_inserter(*data));
        return *this;
    }

    Str(): data(new Vec<char>) { }
    Str(const char* cp): data(new Vec<char>) {
        std::copy(cp, cp + std::strlen(cp), std::back_inserter(*data));
    }
    Str(size_type n, char c): data(new Vec<char>(n, c)) { }
    template <class In> Str(In i, In j): data(new Vec<char>) {
        std::copy(i, j, std::back_inserter(*data));
    }

    Str substr(int i, int j) const {
        Str sub(begin() + i, begin() + i + j);
        return sub;
    }

    char& operator[](size_type i) {
        data.make_unique();
        return (*data)[i];
    }

    const char& operator[](size_type i) const {
        return (*data)[i];
    }

    size_type size() const {
        return data->size();
    }

    iterator begin() {
        return data->begin();
    }

    iterator end() {
        return data->end();
    }

    const_iterator begin() const {
        return data->begin();
    }

    const_iterator end() const {
        return data->end();
    }

private:
    Ptr< Vec<char> > data;
};

std::ostream& operator<<(std::ostream&, const Str&);
Str operator+(const Str&, const Str&);

#endif
