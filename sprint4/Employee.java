// this is an example comment
// double that
public class Employee{
   // this is an example comment
   String name;
   int age;
   String designation;
   // this is an example comment
   float salary;

   int test = 3;

   // this is an example comment
	public int foo(int a, int b) {
      // this is an example comment
		int a = 4;
		return a;
	}
	
	int test2 = foo(3,4);

	public int foo2(int a1, int b1) {
		int c1 = 4;
      // this is an example comment
		return c1;
	}

	int test3 = 5;
	
	public int foo4(int a2, int b2) {
		int c2 = 4;
		return c2;
	}

	int test4 = foo4(3,4);

	int a5 = 5;
	int b5 = 4;
	int c5 = 1;

   // this is an example comment
	if (a5 == b5) {
      // this is an example comment
		c5 = a5 + b5;
      while (a5 < 10){
         a5 = a5 + 1;
      }
      while (a5 < 10){
         a5 = b5 + 1;
      }
	} else {
		c5 = a5 * b5;
      while (a5 < 10){
         a5 = a5 + 1;
      }
      while (a5 < 10){
         a5 = b5 + 1;
      }
	}

	int a6 = 5;
	int b6 = 4;

	int c6 = a6 * 2 + 20 / b6;

   // this is an example comment
	for (int i = 0; i < 5; i = i + 1) {
        int e = 5;
        while (a5 < 10){
           a5 = a5 + 1;
        }
        while (a5 < 10){
            a5 = b5 + 1;
        }
    }

	int t2 = 2;
	int t4 = 6;
   int t3 = 8;
   // this is an example comment
	while (t2 < t4){
		t3 = t3 + 1;
      t2 = t2 + 1;
	}
   t2 = 2
   int t8 = 3;
   while (t2 < t4){
      t8 = t8 + 1;
		t2 = t2 + 1;
	}
	int t5 = 8;
   
	try{
		t5 = 4;
      while (t5 < 10){
         t5 = t5 + 1;
      }
      t5 = 5;
      while (t5 < 10){
         t5 = t5 + 1;
      }
	}
	catch (Exception f){
		t5 = 9;
      while (t5 < 10){
         t5 = t5 + 1;
      }
      t5 = 5;
      while (t5 < 10){
         t5 = t5 + 1;
         t2 = t3 + 2;
      }
	}
	finally{
		t5 = 20;
      while (t5 < 10){
         t5 = t5 + 1;
      }
      t5 = 5;
      while (t5 < 10){
         t5 = t5 + 1;
      }
	}
   // this is an example comment
   public void Employee(String empName){
      this.name = empName;
   }

   public void empAge(int empAge){
      // this is an example comment
      age =  empAge;
   }

   public void empDesignation(String empDesig){
      designation = empDesig;
   }

   public void empSalary(float empSalary){
      salary = empSalary;
   }
   public void printEmployee(){
      // this is an example comment
      System.out.println( name );
      System.out.println( age );
      System.out.println( designation );
      System.out.println(salary);
   }
   public static void main(String[] args){
      // this is an example comment
      Employee empOne = new Employee("emp1");
      empOne.empAge(26);
      empOne.empDesignation("programmer");
      empOne.empSalary(1000.0);
      empOne.printEmployee();

      Employee empTwo = new Employee("emp2");
      empTwo.empAge(16);
      empTwo.empDesignation("new programmer");
      // this is an example comment
      empTwo.empSalary(100.0);
      empTwo.printEmployee();
   }
}