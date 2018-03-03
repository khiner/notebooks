std::ostream& operator<<(std::ostream& os, const Str& s) {
    std::ostream_iterator<char> iter(os);
    for (Str::const_iterator i = s.begin(); i != s.end(); ++i) {
        *iter++ = *i;
    }
    return os;
}

Str operator+(const Str& s, const Str& t) {
    Str r = s;
    r += t;
    return r;
}
