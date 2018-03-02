#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <list>
#include <stdexcept>
#include <string>
#include "Student_info.h"
#include "../chapter_9/grade.h"

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

bool fgrade(const Student_info& s) {
    return s.get_total_grade() < 60;
}

list<Student_info> extractFails(list<Student_info>& students) {
    list<Student_info> fail;
    list<Student_info>::iterator iter = students.begin();

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

void printStudentGrades(const list<Student_info>& students, string::size_type maxlen) {
    for (list<Student_info>::const_iterator it = students.begin(); it != students.end(); ++it) {
        cout << it->name() << string(maxlen + 1 - it->name().size(), ' ');

        try {
            streamsize prec = cout.precision();
            cout << setprecision(3) << it->get_total_grade() << setprecision(prec);
        } catch (domain_error e) {
            cout << e.what();
        }
        cout << endl;
    }
}

int main() {
    list<Student_info> students;
    Student_info record;
    string::size_type maxlen = 0;

    while(record.read(cin)) {
        maxlen = max(maxlen, record.name().size());
        students.push_back(record);
    }

    students.sort(compare);

    list<Student_info> failingStudents = extractFails(students);

    cout << "Passing students:" << endl << endl;
    printStudentGrades(students, maxlen);

    cout << "Failing students:" << endl << endl;
    printStudentGrades(failingStudents, maxlen);
    return 0;
}
