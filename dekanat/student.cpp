#include "student.h"

Student::Student(QString pib,
                 QString zalikova,
                 QString group,
                 int course,
                 double average,
                 int absences,
                 QString educationForm,
                 bool scholarship)
{
    this->pib = pib;
    this->zalikova = zalikova;
    this->group = group;
    this->course = course;
    this->average = average;
    this->absences = absences;
    this->educationForm = educationForm;
    this->scholarship = scholarship;
}

QString Student::getPib()
{
    return pib;
}

QString Student::getZalikova()
{
    return zalikova;
}

QString Student::getGroup()
{
    return group;
}

int Student::getCourse()
{
    return course;
}

double Student::getAverage()
{
    return average;
}

int Student::getAbsences()
{
    return absences;
}

QString Student::getEducationForm()
{
    return educationForm;
}

bool Student::getScholarship()
{
    return scholarship;
}