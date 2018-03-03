#include "Student_info.h"
#include "grade.h"

#include <algorithm>
#include <iostream>
#include <string>

using std::min;
using std::istream; using std::vector;
using std::string;
using std::copy; using std::back_inserter;

using std::cout; using std::endl;

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

double Core::grade() const {
    return ::grade(midterm, final, homework);
}

double Grad::grade() const {
    return min(Core::grade(), thesis);
}

double PassFail::grade() const {
    return homework.empty() ? (midterm + final) / 2 : Core::grade();
}

string Core::letter_grade() const {
    return ::letter_grade(grade());
}

string Grad::letter_grade() const {
    return ::letter_grade(grade());
}

string PassFail::letter_grade() const {
    return grade() >= 60 ? "P" : "F";
}

istream& Core::read_common(istream& in) {
    in >> n >> midterm >> final;
    return in;
}

istream& Core::read(istream& in) {
    read_common(in);
    read_hw(in, homework);
    return in;
}

istream& Grad::read(istream& in) {
    read_common(in);
    in >> thesis;
    read_hw(in, homework);
    return in;
}
