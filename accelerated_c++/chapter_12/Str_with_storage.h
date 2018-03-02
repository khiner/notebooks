#ifndef GUARD_Str_with_storage_h
#define GUARD_Str__with_storage_h

#include "../chapter_11/Vec.h"
#include <algorithm>
#include <iostream>
#include <iterator>
#include <cctype>
#include <vector>

class Str_with_storage {
    friend std::istream& operator>>(std::istream& is, Str_with_storage& s) {
        delete[] s.data;

        char c;
        while (is.get(c) && std::isspace(c));

        std::vector<char> buffer;
        if (is) {
            do buffer.push_back(c);
            while (is.get(c) && !isspace(c));

            if (is)
                is.unget();
        }
        s.s = buffer.size();
        s.data = new char[s.s];
        std::copy(buffer.begin(), buffer.end(), s.data);
        return is;
    }

public:
    Str_with_storage& operator+=(const Str_with_storage& str) {
        char* oldData = new char[s];
        std::copy(data, data + s, oldData);
        delete[] data;
        data = new char[s + str.size()];
        std::copy(oldData, oldData + s, data);
        std::copy(str.data, str.data + str.size(), data + s);
        s+= str.size();
        delete[] oldData;
        return *this;
    }

    typedef size_t size_type;

    Str_with_storage() { }
    Str_with_storage(size_type n, char c) {
        s = n;
        data = new char[n];
    }
    Str_with_storage(const char* cp) {
        s = std::strlen(cp);
        data = new char[s];
        std::copy(cp, cp + std::strlen(cp), data);
    }
    template <class In> Str_with_storage(In b, In e) {
        s = e - b;
        data = new char[s];
        std::copy(b, e, data);
    }
    ~Str_with_storage() {
        delete[] data;
    }

    char& operator[](size_type i) { return data[i]; }
    const char& operator[](size_type i) const { return data[i]; }
    size_type size() const { return s; }

private:
    char* data;
    size_type s;
};

std::ostream& operator<<(std::ostream& os, const Str_with_storage& s) {
    for (Str_with_storage::size_type i = 0; i != s.size(); ++i) {
        os << s[i];
    }
    return os;
}

Str_with_storage operator+(const Str_with_storage& s, const Str_with_storage& t) {
    Str_with_storage r = s;
    r += t;
    return r;
}

#endif
