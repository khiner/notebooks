#include "Student_info.h"
#include "../chapter_10/grade.h"

#include <algorithm>
#include <iostream>

using std::istream; using std::vector; using std::cout;
using std::copy; using std::back_inserter;

using std::cout; using std::endl;

istream& read_hw(istream& in, vector<double>& hw) {
    if (in) {
        hw.clear();

        double x;
        while (in >> x) {
            hw.push_back(x);
        }

        in.clear();
    }
    return in;
}

Student_info::Student_info(): midterm(0), final(0) { }

Student_info::Student_info(istream& is) {
    read(is);
}

Student_info::Student_info(const Student_info& other) {
    n = other.n;
    midterm = other.midterm;
    final = other.final;
    total_grade = other.total_grade;
    homework = other.homework;

    ++copy_count;
}

Student_info& Student_info::operator=(const Student_info& other) {
    if (this != &other) {
        n = other.n;
        midterm = other.midterm;
        final = other.final;
        total_grade = other.total_grade;
        homework = other.homework;
    }
    ++assign_count;
    return *this;
}

Student_info::~Student_info() {
    ++destroy_count;
}

double Student_info::grade() const {
    return ::grade(midterm, final, homework);
}

bool Student_info::passed_for_pass_fail() const {
    return ::passed_for_pass_fail(midterm, final);
}

istream& Student_info::read(istream& is) {
    is >> n >> midterm >> final;
    read_hw(is, homework);
    total_grade = valid() ? grade() : 0;

    return is;
}

bool compare(const Student_info& x, const Student_info& y) {
    return x.name() < y.name();
}

void print_instrumentation() {
    std::cout << "Total copies: " << copy_count << std::endl;
    std::cout << "Total assignments: " << assign_count << std::endl;
    std::cout << "Total destroys: " << destroy_count << std::endl;
}
