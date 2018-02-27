#ifndef GUARD_grade_h
#define GUARD_grade_h

#include <string>
#include <vector>
#include "Student_info.h"

double grade(double, double, double);
double grade(double, double, const std::vector<double>&);
bool passed_for_pass_fail(double, double);
std::string letter_grade(double);

#endif
