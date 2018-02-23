#include "Student_info.h"
#include "grade.h"

using std::istream; using std::vector; using std::cout;

bool compare(const Student_info& x, const Student_info& y) {
    return x.name < y.name;
}

istream& read(istream& is, Student_info& s) {
    is >> s.name >> s.midterm >> s.final;

    if (s.name.empty()) {
        return is;
    }

    read_hw(is, s.homework);
    return is;
}

istream& read_hw(istream& in, vector<double>& hw) {
    if (in) {
        hw.clear();

        double x;
        while (in >> x) {
            hw.push_back(x);
        }

        in.clear();
    }
    return in;
}
