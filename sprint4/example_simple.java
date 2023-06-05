class mainClass {
	int test = 3;

	public int foo(int a, int b) {
		int a = 4;
		return a;
	}
	
	int test2 = foo(3,4);

	public int foo2(int a1, int b1) {
		int c1 = 4;
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

	if (a5 == b5) {
		c5 = a5 + b5;
	} else {
		c5 = a5 * b5;
	}

	int a6 = 5;
	int b6 = 4;

	int c6 = a6 * 2 + 20 / b6;

	for (int i = 0; i < 5; i = i + 1) {
		// test3
        int e = 5;
		a6 = 2;
    }

	int t2 = 2;
	int t4 = 6;
	while (t2 < t4){
		t2 = t2 + 1;
	}
	int t5 = 8;
	try{
		t5 = 4;
	}
	catch (Exception f){
		t5 = 9;
	}
	finally{
		t5 = 20;
	}
}