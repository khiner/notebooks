#include "Student_info.h"
#include "grade.h"

#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using std::cin; using std::cout; using std::endl; using std::vector;
using std::ostream; using std::string; using std::max; using std::domain_error;
using std::streamsize; using std::setprecision;

void write_analysis(ostream& out, const string& name,
                      double analysis(const vector<Student_info>&),
                      const vector<Student_info>& did,
                      const vector<Student_info>& didnt) {
    out << name << ": median(did) = " << analysis(did) <<
                   ", median(didnt) = " << analysis(didnt) << endl;
}

bool ends_with(const string& value, const std::string& ending) {
    if (ending.size() > value.size()) {
        return false;
    }
    return std::equal(ending.rbegin(), ending.rend(), value.rbegin());
}

bool last_name_rhymes_with_alligator(const Student_info& student) {
    static const string alligator = "alligator";
    return ends_with(student.name, alligator);
}

vector<Student_info> extract_rhymes_with_alligator(vector<Student_info>& students) {
    vector<Student_info> rhymes_with_alligator;
    vector<Student_info>::iterator iter = students.begin();

    while (iter != students.end()) {
        if (last_name_rhymes_with_alligator(*iter)) {
            rhymes_with_alligator.push_back(*iter);
            iter = students.erase(iter);
        } else {
            ++iter;
        }
    }
    return rhymes_with_alligator;
}

void printStudentGrades(const vector<Student_info>& students, string::size_type maxlen) {
    for (vector<Student_info>::const_iterator it = students.begin(); it != students.end(); ++it) {
        cout << it->name << string(maxlen + 1 - it->name.size(), ' ');

        try {
            double finalGrade = grade(*it);
            streamsize prec = cout.precision();
            cout << setprecision(3) << finalGrade << setprecision(prec);
        } catch (domain_error e) {
            cout << e.what();
        }
        cout << endl;
    }
}

int main() {
    vector<Student_info> does_not_rhyme_with_alligator;
    string::size_type maxlen = 0;

    Student_info student;
    while (read(cin, student)) {
        maxlen = max(maxlen, student.name.size());
        does_not_rhyme_with_alligator.push_back(student);
    }

    vector<Student_info> rhymes_with_alligator = extract_rhymes_with_alligator(does_not_rhyme_with_alligator);

    cout << "Students whose last name rhymes with \"alligator\":" << endl << endl;
    printStudentGrades(rhymes_with_alligator, maxlen);

    cout << "Students whose last name does not rhyme with \"alligator\":" << endl << endl;
    printStudentGrades(does_not_rhyme_with_alligator, maxlen);
    return 0;

    return 0;
}
