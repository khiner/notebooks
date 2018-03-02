#ifndef GUARD_Vec
#define GUARD_Vec

#include <algorithm>
#include <iostream>
#include <memory>
#include <stdexcept>

template <class T> class Vec {
public:
    typedef T* iterator;
    typedef const T* const_iterator;
    typedef size_t size_type;
    typedef T value_type;
    typedef T& reference;
    typedef const T& const_reference;

    Vec() { create(); }
    explicit Vec(size_type n, const T& t = T()) { create(n, t); }
    Vec(const Vec& v) { create(v.begin(), v.end()); }
    Vec(const_iterator b, const_iterator e) { create(b, e); }
    Vec& operator=(const Vec& rhs) {
        if (&rhs != this) {
            uncreate();
            create(rhs.begin(), rhs.end());
        }
        return *this;
    }

    ~Vec() { uncreate(); }

    T& operator[](size_type i) { return data[i]; }
    const T& operator[](size_type i) const { return data[i]; }

    void push_back(const T& t) {
        if (avail == limit)
            grow();
        unchecked_append(t);
    }

    size_type size() const { return avail - data; }

    iterator begin() { return data; }
    const_iterator begin() const { return data; }
    iterator end() { return avail; }
    const_iterator end() const { return avail; }

    iterator erase(iterator erase_i) {
        if (empty() || erase_i >= avail || erase_i < data)
            throw std::domain_error("trying to erase a nonexistent element");

        iterator it = erase_i;
        while (it != avail) {
            alloc.destroy(it);
            if (it + 1 != avail)
                std::uninitialized_copy(it + 1, it + 2, it);
            it++;
        }
        --avail;

        return erase_i;
    }

    template <class In> void insert (iterator position, In b, In e) {
        size_type sz = e - b;
        size_type raw_position = position - begin(); // push_back will change the location of `begin()`
        for (In i = b; i != e; ++i) {
            push_back(*i);
        }

        Vec cpy = Vec(begin() + raw_position, end() - sz);
        for (size_type i = 0; i < sz; ++i) {
            *(begin() + raw_position + i) = *(b + i);
        }
        std::copy(cpy.begin(), cpy.end(), begin() + raw_position + sz);
    }

    void clear() {
        uncreate();
    }

    bool empty() { return end() == begin(); }

    // assuming this vec is large enough
    void assign(const const_iterator arr, const size_type sz) {
        iterator b = begin();
        for (const_iterator i = arr; i != arr + sz; ++i) {
            *b++ = *i;
        }
    }

    void print_all() {
        for (const_iterator i = begin(); i != end(); ++i) {
            std::cout << *i << std::endl;
        }
    }

private:
    iterator data;
    iterator avail;
    iterator limit;

    std::allocator<T> alloc;

    void create() {
        data = avail = limit = 0;
    }

    void create(size_type n, const T& val) {
        data = alloc.allocate(n);
        limit = avail = data + n;
        std::uninitialized_fill(data, limit, val);
    }
    void create(const_iterator i, const_iterator j) {
        data = alloc.allocate(j - i);
        limit = avail = std::uninitialized_copy(i, j, data);
    }

    void uncreate() {
        if (data) {
            iterator it = avail;
            while (it != data) {
                alloc.destroy(--it);
            }
            alloc.deallocate(data, limit - data);
        }
        data = limit = avail = 0;
    }

    void grow() {
        size_type new_size = std::max(2 * (limit - data), ptrdiff_t(1));

        iterator new_data = alloc.allocate(new_size);
        iterator new_avail = std::uninitialized_copy(data, avail, new_data);

        uncreate();

        data = new_data;
        avail = new_avail;
        limit = data + new_size;
    }

    void unchecked_append(const T& val) {
        alloc.construct(avail++, val);
    }

    void swap(iterator a, iterator b) {
        T tmp = *a;
        *a = *b;
        *b = tmp;
    }
};

#endif
