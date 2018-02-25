#include "../chapter_6/Student_info.h"
#include "../chapter_6/grade.h"

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

using std::cin; using std::cout; using std::endl; using std::vector;
using std::ostream; using std::string; using std::transform;

template <class GradingScheme> double template_analysis(const vector<Student_info>& students, GradingScheme grading_scheme) {
    vector<double> grades;

    transform(students.begin(), students.end(), back_inserter(grades), grading_scheme);
    return median(grades);
}

template <class GradingScheme> void write_analysis(ostream& out, const string& name,
                      GradingScheme grading_scheme,
                      const vector<Student_info>& did,
                      const vector<Student_info>& didnt) {
    out << name << ": median(did) = " << template_analysis(did, grading_scheme) <<
                   ", median(didnt) = " << template_analysis(didnt, grading_scheme) << endl;
}

vector<Student_info> extract_didnt_do_all_hw(vector<Student_info>& students) {
    vector<Student_info> didnt;
    vector<Student_info>::iterator iter = students.begin();

    while (iter != students.end()) {
        if (!did_all_hw(*iter)) {
            didnt.push_back(*iter);
            iter = students.erase(iter);
        } else {
            ++iter;
        }
    }
    return didnt;
}

int main() {
    vector<Student_info> did;

    Student_info student;
    while (read(cin, student)) {
        did.push_back(student);
    }

    vector<Student_info> didnt = extract_didnt_do_all_hw(did);

    if (did.empty()) {
        cout << "No student did all the homework!" << endl;
        return 1;
    }
    if (didnt.empty()) {
        cout << "Every student did all the homework!" << endl;
        return 1;
    }

    write_analysis(cout, "median", grade_aux, did, didnt);
    write_analysis(cout, "average", average_grade, did, didnt);
    write_analysis(cout, "median of homework turned in", optimistic_median, did, didnt);

    return 0;
}
