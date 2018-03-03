#ifndef GUARD_Picture_h
#define GUARD_Picture_h

#include "../chapter_14/Ptr.h"
#include "../chapter_14/Str.h"
#include "../chapter_11/Vec.h"

#include<algorithm>
#include<iostream>

class Picture;

class Pic_base {
    friend std::ostream& operator<<(std::ostream&, const Picture&);
    friend const Picture& reframe(const Picture&, const char, const char, const char);
    friend class Frame_Pic;
    friend class HCat_Pic;
    friend class VCat_Pic;
    friend class String_Pic;

    typedef Vec<Str>::size_type ht_sz;
    typedef Str::size_type wd_sz;

    virtual wd_sz width() const = 0;
    virtual ht_sz height() const = 0;
    virtual void display(std::ostream&, ht_sz, bool) const = 0;
    virtual void reframe(const char corner_char, const char top_bottom_char, const char sides_char) { } // only Frame_Pic actually implements.

public:
    virtual ~Pic_base() { }

protected:
    static void pad(std::ostream& os, wd_sz beg, wd_sz end) {
        while (beg++ != end) {
            os << " ";
        }
    }
};

class String_Pic: public Pic_base {
    friend class Picture;
    Vec<Str> data;
    String_Pic(const Vec<Str>& v): data(v) { }

    ht_sz height() const {
        return data.size();
    }

    wd_sz width() const {
        wd_sz n = 0;
        for (ht_sz i = 0; i != data.size(); ++i) {
            n = std::max(n, data[i].size());
        }
        return n;
    }

    void display(std::ostream&, ht_sz, bool) const;
};

class VCat_Pic: public Pic_base {
    friend Picture vcat(const Picture&, const Picture&);
    Ptr<Pic_base> top, bottom;
    VCat_Pic(const Ptr<Pic_base>& t, const Ptr<Pic_base>& b): top(t), bottom(b) { }

    wd_sz width() const {
        return std::max(top->width(), bottom->width());
    }
     ht_sz height() const {
        return top->height() + bottom->height();
    }

    void display(std::ostream&, ht_sz, bool) const;

    void reframe(const char corner_char, const char top_bottom_char, const char sides_char) {
        top->reframe(corner_char, top_bottom_char, sides_char);
        bottom->reframe(corner_char, top_bottom_char, sides_char);
    }
};

class HCat_Pic: public Pic_base {
    friend Picture hcat(const Picture&, const Picture&);
    Ptr<Pic_base> left, right;
    HCat_Pic(const Ptr<Pic_base>& l, const Ptr<Pic_base>& r): left(l), right(r) { }

    wd_sz width() const {
        return left->width() + right->width();
    }
    ht_sz height() const {
        return std::max(left->height(), right->height());
    }

    void display(std::ostream&, ht_sz, bool) const;

    void reframe(const char corner_char, const char top_bottom_char, const char sides_char) {
        left->reframe(corner_char, top_bottom_char, sides_char);
        right->reframe(corner_char, top_bottom_char, sides_char);
    }
};

class Frame_Pic: public Pic_base {
    friend Picture frame(const Picture&, const char, const char, const char);

    Ptr<Pic_base> p;
    char corner_char, top_bottom_char, sides_char;

    Frame_Pic(const Ptr<Pic_base>& pic,
              const char corner,
              const char top_bottom,
              const char sides): p(pic), corner_char(corner), top_bottom_char(top_bottom), sides_char(sides) { }

    wd_sz width() const {
        return p->width() + 4;
    }
    ht_sz height() const {
        return p->height() + 4;
    }

    void display(std::ostream&, ht_sz, bool) const;

    void reframe(const char corner_char, const char top_bottom_char, const char sides_char) {
        this->corner_char = corner_char;
        this->top_bottom_char = top_bottom_char;
        this->sides_char = sides_char;
        p->reframe(corner_char, top_bottom_char, sides_char);
    }
};

class Picture {
    friend std::ostream& operator<<(std::ostream&, const Picture&);
    friend Picture frame(const Picture&, const char, const char, const char);
    friend const Picture& reframe(const Picture&, const char, const char, const char);
    friend Picture hcat(const Picture&, const Picture&);
    friend Picture vcat(const Picture&, const Picture&);

public:
    Picture(const Vec<Str>& v = Vec<Str>()): p(new String_Pic(v)) { }

private:
    Picture(Pic_base* ptr): p(ptr) { }
    Ptr<Pic_base> p;
};

Picture frame(const Picture&, const char='*', const char='*', const char='*');
const Picture& reframe(const Picture&, const char='*', const char='*', const char='*');
Picture hcat(const Picture&, const Picture&);
Picture vcat(const Picture&, const Picture&);
std::ostream& operator<<(std::ostream&, const Picture&);

#endif
