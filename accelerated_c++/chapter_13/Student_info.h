#ifndef GUARD_Student_info
#define GUARD_Student_info

#include <iostream>
#include <string>
#include <vector>

class Core {
    friend class Student_info;
public:
    Core(): midterm(0), final(0) { }

    Core(std::istream& is) {
        read(is);
    }

    virtual ~Core() { }

    std::string name() const {
        return n;
    }

    virtual std::istream& read(std::istream&);

    virtual double grade() const;
    virtual std::string letter_grade() const;

    virtual bool valid() const { return !homework.empty(); };

protected:
    virtual Core* clone() const { return new Core(*this); }

    std::istream& read_common(std::istream&);
    double midterm, final;
    std::vector<double> homework;

private:
    std::string n;
};

class PassFail: public Core {
public:
    PassFail(std::istream& is) { Core::read(is); }
    double grade() const;
    std::string letter_grade() const;
protected:
    PassFail* clone() const { return new PassFail(*this); }
};

class Auditing: public Core {
public:
    Auditing(std::istream& is) { Core::read(is); }
    double grade() const { return 0; } // no grades for auditing students
    std::string letter_grade() const { return "NA"; }
    bool valid() const { return true; }; // auditing students need nothing to be valid
protected:
    Auditing* clone() const { return new Auditing(*this); }
};

class Grad: public Core {
public:
    Grad(): thesis(0) { }

    Grad(std::istream& is) {
        read(is);
    }

    double grade() const;
    std::string letter_grade() const;

    bool valid() const { return Core::valid() && thesis != 0; };

    std::istream& read(std::istream&);

protected:
    virtual Grad* clone() const { return new Grad(*this); }

private:
    double thesis;
};

class Student_info {
public:
    Student_info(): cp(0) { }

    Student_info(std::istream& is): cp(0) { read(is); }

    Student_info(const Student_info& s): cp(0) {
        if (s.cp)
            cp = s.cp->clone();
    }

    Student_info& operator=(const Student_info& s) {
        if (&s != this) {
            delete cp;
            cp = s.cp ? s.cp->clone() : 0;
        }
        return *this;
    }

    ~Student_info() { delete cp; }

    std::string name() const {
        if (cp) return cp->name();
        else throw std::runtime_error("uninitialized Student");
    }

    std::istream& read(std::istream& in) {
        delete cp;

        char ch;
        in >> ch;

        if (ch == 'A') {
            cp = new Auditing(in);
        } else if (ch == 'P') {
            cp = new PassFail(in);
        } else if (ch == 'U') {
            cp = new Core(in);
        } else {
            cp = new Grad(in);
        }

        return in;
    }

    double grade() const {
        if (cp) return cp->grade();
        else throw std::runtime_error("uninitialized Student");
    }

    std::string letter_grade() const {
        if (cp) return cp->letter_grade();
        else throw std::runtime_error("uninitialized Student");
    }

    bool valid() const {
        if (cp) return cp->valid();
        else throw std::runtime_error("uninitialized Student");
    }

    static bool compare(const Student_info& s1, const Student_info& s2) {
        return s1.name() < s2.name();
    }
private:
    Core* cp;
};

#endif
