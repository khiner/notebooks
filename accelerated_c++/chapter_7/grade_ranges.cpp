#include "../chapter_6/grade.h"
#include "../chapter_6/Student_info.h"

#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using std::cin;
using std::cout;
using std::domain_error;
using std::endl;
using std::map;
using std::max;
using std::setprecision;
using std::sort;
using std::streamsize;
using std::string;
using std::vector;

char letterForGrade(double grade) {
    // haven't learned switch statements yet.
    if (grade >= 90.0) {
        return 'A';
    } else if (grade >= 80.0) {
        return 'B';
    } else if (grade >= 70.0) {
        return 'C';
    } else if (grade >= 60.0) {
        return 'D';
    } else {
        return 'F';
    }
}

int main() {
    vector<Student_info> students;
    Student_info record;

    while(read(cin, record)) {
        students.push_back(record);
    }

    sort(students.begin(), students.end(), compare);

    map<char, int> number_of_students_with_grade;
    for (vector<Student_info>::const_iterator it = students.begin(); it != students.end(); ++it) {
        try {
            ++number_of_students_with_grade[letterForGrade(grade(*it))];
        } catch (domain_error e) {
            cout << e.what();
        }
    }

    if (!number_of_students_with_grade.empty()) {
        cout << "Grade" << '\t' << "Number of students" << endl;
    }
    for (map<char, int>::const_iterator it = number_of_students_with_grade.begin(); it != number_of_students_with_grade.end(); ++it) {
        cout << it->first << '\t' << it->second << endl;
    }
    cout << endl;

    return 0;
}
