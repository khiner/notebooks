#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "grade.h"
#include "Student_info.h"

using std::cin;
using std::cout;
using std::domain_error;
using std::endl;
using std::string;

int main() {
    try {
        Student_info record(cin);
    } catch (domain_error e) {
        cout << "Caught an error!" << endl;
        cout << e.what() << endl;
    }

    return 0;
}
