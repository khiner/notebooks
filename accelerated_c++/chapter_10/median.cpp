#include <algorithm>
#include <stdexcept>
#include <vector>

using std::domain_error; using std::sort; using std::vector;

template <class T> T median(T* begin, T* end) {
    if (begin == end) {
        throw std::domain_error("median of an empty range");
    }

    size_t size = end - begin;
    T* cpy = new T[size];
    std::copy(begin, end, cpy); // don't change the original array
    std::sort(cpy, cpy + size);

    size_t mid = size / 2;
    T med = size % 2 == 0 ? (cpy[mid] + cpy[mid - 1]) / 2 : cpy[mid];
    delete[] cpy;
    return med;
}
