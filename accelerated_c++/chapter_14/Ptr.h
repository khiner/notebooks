#ifndef GUARD_Ptr_h
#define GUARD_Ptr_h

#include "Ref_count.h"
#include <stdexcept>

template <class T> class Ptr {
public:
    void make_unique() {
        if (ref_count.make_unique()) {
            p = p ? clone(p) : 0;
        }
    }

    Ptr(): p(0) { }
    Ptr(T* t): p(t) { }
    Ptr(const Ptr& h): p(h.p), ref_count(h.ref_count) { }

    Ptr& operator=(const Ptr& rhs) {
        ++rhs.ref_count;
        if ((--ref_count).dead()) {
            delete p;
        }
        ref_count = rhs.ref_count;
        p = rhs.p;
        return *this;
    }

    ~Ptr() {
        if ((--ref_count).dead()) {
            delete p;
        }
    }

    operator bool() const {
        return p;
    }

    T& operator*() const {
        if (p)
            return *p;
        throw std::runtime_error("unbound Handle");
    }

    T* operator->() const {
        if (p)
            return p;
        throw std::runtime_error("unbound Handle");
    }

private:
    T* p;
    Ref_count ref_count;
};

template <class T> T* clone(const T* tp) {
    return tp->clone();
}

#endif
