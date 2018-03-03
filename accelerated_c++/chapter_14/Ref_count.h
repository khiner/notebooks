#ifndef GUARD_Ref_count_h
#define GUARD_Ref_count_h

#include <stdexcept>

class Ref_count {
public:
    bool make_unique() {
        if (*refptr != 1) {
            --*refptr;
            refptr = new size_t(1);
            return true;
        }
        return false;
    }

    Ref_count(): refptr(new size_t(1)) { }
    Ref_count(const Ref_count& r): refptr(r.refptr) { ++*refptr; }

    operator bool() const {
        return refptr;
    }

    const Ref_count& operator++() const {
        ++*refptr;
        return *this;
    }

    Ref_count& operator++() {
        ++*refptr;
        return *this;
    }

    Ref_count& operator--() {
        if (--*refptr == 0) {
            delete refptr;
        }
        return *this;
    }

    std::size_t& operator*() const {
        if (refptr)
            return *refptr;
        throw std::runtime_error("unbound");
    }

    std::size_t* operator->() const {
        if (refptr)
            return refptr;
        throw std::runtime_error("unbound");
    }

    bool dead() {
        return !refptr;
    }

private:
    std::size_t* refptr;
};

#endif
