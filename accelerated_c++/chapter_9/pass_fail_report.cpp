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
using std::domain_error;
using std::endl;
using std::max;
using std::sort;
using std::string;
using std::vector;

vector<Student_info> extract_failed_for_pass_fail(vector<Student_info>& students) {
    vector<Student_info> failed_for_pass_fail;

    for (vector<Student_info>::const_iterator it = students.begin(); it != students.end();) {
        if (!it->passed_for_pass_fail()) {
            failed_for_pass_fail.push_back(*it);
            students.erase(it);
        } else {
            ++it;
        }
    }

    return failed_for_pass_fail;
}

int main() {
    vector<Student_info> passing_students;
    Student_info record;
    string::size_type maxlen = 0;

    while(record.read(cin)) {
        maxlen = max(maxlen, record.name().size());
        passing_students.push_back(record);
    }

    sort(passing_students.begin(), passing_students.end(), compare);

    vector<Student_info> failing_students = extract_failed_for_pass_fail(passing_students);

    for (vector<Student_info>::const_iterator it = passing_students.begin(); it != passing_students.end(); ++it) {
        cout << it->name() << string(maxlen + 1 - it->name().size(), ' ') << 'P' << endl;
    }

    for (vector<Student_info>::const_iterator it = failing_students.begin(); it != failing_students.end(); ++it) {
        cout << it->name() << string(maxlen + 1 - it->name().size(), ' ') << 'F' << endl;
    }
    return 0;
}
