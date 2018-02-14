#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <list>
#include <vector>
#include <stdexcept>
#include <string>
#include "../chapter_4/Student_info.h"

using std::cin;
using std::cout;
using std::domain_error;
using std::endl;
using std::list;
using std::max;
using std::setprecision;
using std::sort;
using std::streamsize;
using std::string;
using std::vector;

typedef list<Student_info> student_collection;

bool fgrade(const Student_info& s) {
    return s.finalGrade < 60;
}

student_collection extractFails(student_collection& students) {
    student_collection fail;

    student_collection::size_type successCount = 0;
    for (student_collection::const_iterator iter = students.begin(); iter != students.end(); ++iter) {
        if (fgrade(*iter)) {
            fail.push_back(*iter);
        } else {
            students.insert(students.begin(), *iter);
            successCount++;
        }
    }
    students.resize(successCount);
    return fail;
}

void printStudentGrades(const student_collection& students, string::size_type maxlen) {
    for (student_collection::const_iterator it = students.begin(); it != students.end(); ++it) {
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
    student_collection students;
    Student_info record;
    string::size_type maxlen = 0;

    while(read(cin, record)) {
        maxlen = max(maxlen, record.name.size());
        students.push_back(record);
    }

    student_collection failingStudents = extractFails(students);

    cout << "Passing students:" << endl << endl;
    printStudentGrades(students, maxlen);

    cout << "Failing students:" << endl << endl;
    printStudentGrades(failingStudents, maxlen);
    return 0;
}
