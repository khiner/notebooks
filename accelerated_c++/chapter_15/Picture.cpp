#include "Picture.h"
#include "../chapter_14/Str.h"

#include <iostream>

using std::cout;
using std::endl;
using std::ostream;

void String_Pic::display(ostream& os, ht_sz row, bool do_pad) const {
    wd_sz start = 0;

    if (row < height()) {
        os << data[row];
        start = data[row].size();
    }

    if (do_pad) {
        pad(os, start, width());
    }
}

void VCat_Pic::display(ostream& os, ht_sz row, bool do_pad) const {
    wd_sz w = 0;
    if (row < top->height()) {
        top->display(os, row, do_pad);
        w = top->width();
    } else if (row < height()) {
        bottom->display(os, row - top->height(), do_pad);
        w = bottom->width();
    }
    if (do_pad) {
        pad(os, w, width());
    }
}

void HCat_Pic::display(ostream& os, ht_sz row, bool do_pad) const {
    if (left->height() < right->height()) {
        ht_sz half_height_diff = (right->height() - left->height()) / 2;
        if (row < half_height_diff || row >= right->height() - half_height_diff) {
            pad(os, 0, left->width());            
        } else {
            left->display(os, row - half_height_diff, do_pad || row - half_height_diff < right->height());
        }
    } else {
        left->display(os, row, do_pad || row < right->height());
    }

    if (left->height() > right->height()) {
        ht_sz half_height_diff = (left->height() - right->height()) / 2;
        if (row < half_height_diff || row >= left->height() - half_height_diff) {
            pad(os, 0, right->width());            
        } else {
            right->display(os, row - half_height_diff, do_pad);
        }
    } else {
        right->display(os, row, do_pad);
    }
}

void Frame_Pic::display(ostream& os, ht_sz row, bool do_pad) const {
    if (row >= height()) {
        if (do_pad) {
            pad(os, 0, width());
        }
    } else {
        if (row == 0 || row == height() - 1) {
            os << corner_char << Str(width() - 2, top_bottom_char) << corner_char;
        } else if (row == 1 || row == height() - 2) {
            os << sides_char;
            pad(os, 1, width() - 1);
            os << sides_char;
        } else {
            os << sides_char << ' ';
            p->display(os, row - 2, true);
            os << ' ' << sides_char;
        }
    }
}

Picture frame(const Picture& pic, const char corner_char, const char top_bottom_char, const char sides_char) {
    return new Frame_Pic(pic.p, corner_char, top_bottom_char, sides_char);
}

const Picture& reframe(const Picture& pic, const char corner_char, const char top_bottom_char, const char sides_char) {
    pic.p->reframe(corner_char, top_bottom_char, sides_char);
    return pic;
}

Picture hcat(const Picture& l, const Picture& r) {
    return new HCat_Pic(l.p, r.p);
}

Picture vcat(const Picture& t, const Picture& b) {
    return new VCat_Pic(t.p, b.p);
}

std::ostream& operator<<(std::ostream& os, const Picture& picture) {
    const Pic_base::ht_sz ht = picture.p->height();
    for (Pic_base::ht_sz i = 0; i != ht; ++i) {
        picture.p->display(os, i, false);
        os << endl;
    }
    return os;
}
