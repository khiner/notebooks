#include "grade.h"
#include "../../chapter_4/median.h"

#include <stdexcept>

using std::vector; using std::domain_error;

double grade(double midterm, double final, double homework) {
    return 0.2 * midterm + 0.4 * final + 0.4 * homework;
}

double grade(double midterm, double final, const vector<double>& hw) {
    if (hw.size() == 0) {
        throw domain_error("student has done no homework");
    }
    return grade(midterm, final, median(hw));
}

bool passed_for_pass_fail(double midterm, double final) {
    return (midterm + final) / 2 > 60;
}
