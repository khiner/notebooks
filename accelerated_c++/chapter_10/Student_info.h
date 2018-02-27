#ifndef GUARD_Student_info
#define GUARD_Student_info

#include <iostream>
#include <string>
#include <vector>

class Student_info {
public:
    Student_info();
    Student_info(std::istream&);
    std::string name() const { return n; }
    bool valid() const { return !homework.empty(); }
    bool passed_for_pass_fail() const;
    std::istream& read(std::istream&);
    double get_total_grade() const { return total_grade; }

private:
    std::string n;
    double midterm, final;
    double total_grade;
    std::vector<double> homework;
    double grade() const;
};

bool compare(const Student_info&, const Student_info&);

#endif
