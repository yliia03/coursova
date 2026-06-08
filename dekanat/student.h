#ifndef STUDENT_H
#define STUDENT_H

#include <QString>

class Student
{
private:
    QString pib;
    QString zalikova;
    QString group;
    int course;
    double average;
    int absences;
    QString educationForm;
    bool scholarship;

public:
    Student(QString pib,
            QString zalikova,
            QString group,
            int course,
            double average,
            int absences,
            QString educationForm,
            bool scholarship);

    QString getPib();
    QString getZalikova();
    QString getGroup();
    int getCourse();
    double getAverage();
    int getAbsences();
    QString getEducationForm();
    bool getScholarship();
};

#endif