#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <string>
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::setprecision;
using std::sort;
using std::streamsize;
using std::string;
using std::vector;

int main() {
    int numStudents = 2;
    vector<string> names;
    vector<double> grades;
    for (int i = 0; i < numStudents; i++)  {
        cout << "Student " << i + 1 << ", please enter your first name: ";
        string name;
        cin >> name;
        names.push_back(name);
        cout << "Hello, " << names[i] << "!" << endl;

        cout << name << ", please enter your midterm and final exam grades: ";
        double midterm, final;
        cin >> midterm >> final;

        double runningTotalGrade = 0.2 * midterm + 0.4 * final;

        vector<double> homeworkGrades;

        int numHomeworkGrades = 3;
        cout << "Enter all " << numHomeworkGrades << " of your homework grades, "
                "followed by end-of-file: ";

        double homeworkGrade;

        for (int i = 0; i < numHomeworkGrades; i++) {
            cin >> homeworkGrade;
            homeworkGrades.push_back(homeworkGrade);
        }

        sort(homeworkGrades.begin(), homeworkGrades.end());

        double median = homeworkGrades[numHomeworkGrades / 2];
        grades.push_back(runningTotalGrade + 0.4 * median);
    }

    for (int i = 0; i < numStudents; i++) {
        streamsize prec = cout.precision();
        cout << names[i] << ", your final grade is " << setprecision(3) << grades[i] << setprecision(prec) << endl;
    }

    return 0;
}
