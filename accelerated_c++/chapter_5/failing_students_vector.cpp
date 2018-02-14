#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "../chapter_4/Student_info.h"

using std::cin;
using std::cout;
using std::domain_error;
using std::endl;
using std::max;
using std::setprecision;
using std::sort;
using std::streamsize;
using std::string;
using std::vector;

bool fgrade(const Student_info& s) {
    return s.finalGrade < 60;
}

vector<Student_info> extractFails(vector<Student_info>& students) {
    vector<Student_info> fail;
    vector<Student_info>::iterator iter = students.begin();

    while (iter != students.end()) {
        if (fgrade(*iter)) {
            fail.push_back(*iter);
            iter = students.erase(iter);
        } else {
            ++iter;
        }
    }
    return fail;
}

void printStudentGrades(const vector<Student_info>& students, string::size_type maxlen) {
    for (vector<Student_info>::const_iterator it = students.begin(); it != students.end(); ++it) {
        cout << it->name << string(maxlen + 1 - it->name.size(), ' ');

        try {
            double finalGrade = it->finalGrade;
            streamsize prec = cout.precision();
            cout << setprecision(3) << finalGrade << setprecision(prec);
        } catch (domain_error e) {
            cout << e.what();
        }
        cout << endl;
    }
}

int main() {
    vector<Student_info> students;
    Student_info record;
    string::size_type maxlen = 0;

    while(read(cin, record)) {
        maxlen = max(maxlen, record.name.size());
        students.push_back(record);
    }

    sort(students.begin(), students.end(), compare);

    vector<Student_info> failingStudents = extractFails(students);

    cout << "Passing students:" << endl << endl;
    printStudentGrades(students, maxlen);

    cout << "Failing students:" << endl << endl;
    printStudentGrades(failingStudents, maxlen);
    return 0;
}
