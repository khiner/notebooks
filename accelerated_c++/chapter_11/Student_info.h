#ifndef GUARD_Student_info
#define GUARD_Student_info

#include <iostream>
#include <string>
#include <vector>

static int copy_count = 0;
static int assign_count = 0;
static int destroy_count = 0;

class Student_info {
public:
    Student_info();
    Student_info(std::istream&);
    Student_info(const Student_info&);
    Student_info& operator=(const Student_info&);
    ~Student_info();
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

void print_instrumentation();

#endif
