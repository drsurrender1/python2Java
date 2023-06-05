#  this is an example comment
#  double that
class Employee:
    #  this is an example comment
    name = None
    age = 0
    designation = None
    #  this is an example comment
    salary = 0.0
    #  this is an example comment
    def foo(a: int, b: int) -> int:
        #  this is an example comment
        a = 4
        return a
    test2 = foo(3, 4)
    def foo2(a1: int, b1: int) -> int:
        c1 = 4
        #  this is an example comment
        return c1
    def foo4(a2: int, b2: int) -> int:
        c2 = 4
        return c2
    test4 = foo4(3, 4)
    a5 = 5
    b5 = 4
    c5 = 1
    #  this is an example comment
    if (a5 == b5):
        #  this is an example comment
        c5 = a5 + b5
        while (a5 < 10):
            a5 = a5 + 1
        while (a5 < 10):
            a5 = b5 + 1
    else:
        c5 = a5 * b5
        while (a5 < 10):
            a5 = a5 + 1
        while (a5 < 10):
            a5 = b5 + 1
    a6 = 5
    b6 = 4
    #  this is an example comment
    i = 0
    for i in range(0, 5, 1):
        while (a5 < 10):
            a5 = a5 + 1
        while (a5 < 10):
            a5 = b5 + 1
    t2 = 2
    t4 = 6
    t3 = 8
    #  this is an example comment
    t2 = 2
    t8 = 3
    while (t2 < t4):
        t3 = t3 + 1
        t2 = t2 + 1
        t8 = t8 + 1
    t5 = 8
    try:
        t5 = 4
        t5 = 5
        while (t5 < 10):
            t5 = t5 + 1
    except f:
        t5 = 9
        t5 = 5
        while (t5 < 10):
            t5 = t5 + 1
            t2 = t3 + 2
    finally:
        t5 = 20
        t5 = 5
        while (t5 < 10):
            t5 = t5 + 1
    #  this is an example comment
    def __init__(self, empName: String) -> None:
        self.name = empName
    def empAge(self, empAge: int) -> None:
        #  this is an example comment
        age = empAge
    def empDesignation(self, empDesig: String) -> None:
        designation = empDesig
    def empSalary(self, empSalary: float) -> None:
        salary = empSalary
    def printEmployee(self) -> None:
        #  this is an example comment
        print(name)
        print(age)
        print(designation)
        print(salary)
    def main(args) -> None:
        #  this is an example comment
        empOne = Employee("emp1")
        empOne.empAge(26)
        empOne.empDesignation("programmer")
        empOne.empSalary(1000.0)
        empOne.printEmployee()
        empTwo = Employee("emp2")
        empTwo.empAge(16)
        empTwo.empDesignation("new programmer")
        #  this is an example comment
        empTwo.empSalary(100.0)
        empTwo.printEmployee()
if __name__=="__main__":
    Employee.main([])
