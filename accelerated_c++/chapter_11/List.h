#ifndef GUARD_List
#define GUARD_List

#include <cstddef>
#include <iostream>

template <class T> class Node_t {
public:
    Node_t() {
    }

    Node_t(const T& val) {
        value = val;
        next = NULL;
    }

    Node_t(const T& val, const Node_t& n) {
        value = val;
        next = &n;
    }

    Node_t& operator++() {
        value = next->value;
        next = next->next;
        return *this;
    }

    Node_t& operator+(const int p) {
        Node_t* curr = this;
        for (int i = 0; i < p; i++) {
            if (curr->next == NULL) 
                return NULL;
            curr = curr->next;
        }

        return curr;
    }

    size_t operator-(const Node_t<T>& other) {
        Node_t<T>* curr = &other;
        int count;
        while(curr != *this) {
            curr = curr->next;
            ++count;
        }

        return count;
    }

    T operator*() {
        return value;
    }

    void set_next(Node_t<T>* n) {
        next = n;
    }

    Node_t* get_next() {
        return next;
    }

private:
    T value;
    Node_t<T>* next;
};

template <class T> class List {
public:
    typedef Node_t<T> iterator;
    typedef const Node_t<T> const_iterator;
    typedef size_t size_type;
    typedef T value_type;
    typedef T& reference;
    typedef const T& const_reference;

    List(): head(NULL), tail(NULL) { }
    explicit List(size_type n, const T& t = T()) { create(n, t); }
    List(const List& v) { create(v.begin(), v.end()); }
    List(const_iterator b, const_iterator e) { create(b, e); }
    List& operator=(const List& rhs) {
        if (&rhs != this) {
            create(rhs.begin(), rhs.end());
        }
        return *this;
    }

    ~List() { uncreate(); }

    void push_back(const T& t) {
        Node_t<T> new_tail = iterator(t);
        if (head && tail) {
            tail->set_next(&new_tail);
            tail = &new_tail;
        } else {
            head = tail = &new_tail;
        }
    }

    size_type size() const { return *tail - *head; }

    iterator begin() { return *head; }
    const_iterator begin() const { return *head; }
    iterator end() { return *tail + 1; }
    const_iterator end() const { return *tail + 1; }

    iterator& erase(const iterator& erase_i) {
        if (&erase_i == head) {
            if (head == tail) {
                uncreate();
                return;
            } else {
                (*head)++;
                return;
            }
        }

        iterator* prev = head;
        while (prev->get_next() != &erase_i) {
            (*prev)++;
        }
        prev->set_next(erase_i.get_next());

        return prev;
    }

    void clear() {
        uncreate();
    }

    bool empty() { return end() == begin(); }

    void print_all() {
        for (const_iterator i = begin(); i != end(); ++i) {
            std::cout << *i << std::endl;
        }
    }

private:
    iterator* head;
    iterator* tail;

    void create(const T& val) {
        Node_t<T> new_head = iterator(val);
        head = &new_head;
        tail = head;
    }

    void create(size_type n, const T& val) {
        create(val);

        iterator* prev = head;
        for (size_type i = 1; i < n; i++) {
            Node_t<T> new_tail = iterator(val);
            tail = &new_tail;
            prev->set_next(tail);
            prev = tail;
        }
    }

    void create(const_iterator i, const_iterator j) {
        create(*i);

        if (i == j)
            return;

        iterator *prev = head;
        for (const_iterator it = i + 1; it != j; it++) {
            tail = iterator(*it);
            prev->set_next(tail);
            prev = tail;
        }
    }

    void uncreate() {
        head = NULL;
        tail = NULL;
    }
};

#endif
