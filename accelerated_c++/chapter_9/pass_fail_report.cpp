#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "Student_info.h"

using std::cin;
using std::cout;
using std::endl;
using std::max;
using std::partition;
using std::sort;
using std::string;
using std::vector;

bool passing(const Student_info& student) {
    return student.passed_for_pass_fail();
}

int main() {
    vector<Student_info> students;
    Student_info record;
    string::size_type maxlen = 0;

    while(record.read(cin)) {
        maxlen = max(maxlen, record.name().size());
        students.push_back(record);
    }

    sort(students.begin(), students.end(), compare);

    vector<Student_info>::const_iterator failing_begin = partition(students.begin(), students.end(), passing);

    for (vector<Student_info>::const_iterator it = students.begin(); it != failing_begin; ++it) {
        cout << it->name() << string(maxlen + 1 - it->name().size(), ' ') << 'P' << endl;
    }

    for (vector<Student_info>::const_iterator it = failing_begin; it != students.end(); ++it) {
        cout << it->name() << string(maxlen + 1 - it->name().size(), ' ') << 'F' << endl;
    }

    return 0;
}
