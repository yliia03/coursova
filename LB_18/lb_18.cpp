#include <iostream>
#include <memory>
#include <vector>

using namespace std;

class Product {
public:
    string name;
    string category;
    double price;

    Product(string n, string c, double p) {
        name = n;
        category = c;
        price = p;
    }
};

class Employee {
public:
    string fullName;
    string position;
    double salary;

    Employee(string f, string p, double s) {
        fullName = f;
        position = p;
        salary = s;
    }
};

class University {
public:
    string name;
    string city;
    int rating;

    University(string n, string c, int r) {
        name = n;
        city = c;
        rating = r;
    }
};

int main() {

    cout << "===== TASK 1 =====" << endl;

    unique_ptr<Product> p1 =
        make_unique<Product>("Laptop", "Electronics", 35000);

    unique_ptr<Product> p2 = move(p1);

    if (p1 == nullptr) {
        cout << "p1 is nullptr" << endl;
    }
    cout << "Product: " << p2->name << endl;
    cout << "Category: " << p2->category << endl;
    cout << "Price: " << p2->price << endl;


    cout << "\n===== TASK 2 =====" << endl;

    shared_ptr<Employee> e1 =
        make_shared<Employee>("Ivan Petrenko", "Manager", 25000);

    cout << "use_count after e1: "
         << e1.use_count() << endl;

    {
        shared_ptr<Employee> e2 = e1;
        cout << "use_count after e2: "
             << e1.use_count() << endl;

        shared_ptr<Employee> e3 = e1;
        cout << "use_count after e3: "
             << e1.use_count() << endl;
    }

    cout << "use_count after scope: "
         << e1.use_count() << endl;


    cout << "\n===== TASK 3 =====" << endl;

    vector<University> universities = {
        {"KPI", "Kyiv", 95},
        {"LNU", "Lviv", 85},
        {"KhNU", "Kharkiv", 78},
        {"ONU", "Odesa", 90}
    };

    int minRating = 80;

    auto checkRating = [minRating](University u) {
        return u.rating > minRating;
    };

    int count = 0;

    for (University u : universities) {
        if (checkRating(u)) {
            count++;
        }
    }

    cout << "Universities with rating > "
         << minRating << ": "
         << count << endl;

    return 0;
}