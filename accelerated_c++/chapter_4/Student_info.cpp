#include "Student_info.h"
#include "grade.h"

using std::istream; using std::vector; using std::cout;

bool compare(const Student_info& x, const Student_info& y) {
    return x.name < y.name;
}

istream& read(istream& is, Student_info& s) {
    double midterm, final;
    is >> s.name >> midterm >> final;

    if (s.name.empty()) {
        return is;
    }

    vector<double> homework;
    read_hw(is, homework);
    if (!homework.empty()) {
        // I can't figure out how to get istream to just stop reading without a special end-string.
        // It always just reads blanks into every var when I press ctrl+d
        // So this should be treated as an error, case - it's a hack :(
        s.finalGrade = grade(midterm, final, homework);
    }
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
