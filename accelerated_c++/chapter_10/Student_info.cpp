#include "Student_info.h"
#include "grade.h"

using std::istream; using std::vector; using std::cout;

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

Student_info::Student_info(): midterm(0), final(0) { }

Student_info::Student_info(istream& is) {
    read(is);
}

double Student_info::grade() const {
    return ::grade(midterm, final, homework);
}

bool Student_info::passed_for_pass_fail() const {
    return ::passed_for_pass_fail(midterm, final);
}

istream& Student_info::read(istream& is) {
    is >> n >> midterm >> final;
    read_hw(is, homework);
    total_grade = valid() ? grade() : 0;

    return is;
}

bool compare(const Student_info& x, const Student_info& y) {
    return x.name() < y.name();
}
