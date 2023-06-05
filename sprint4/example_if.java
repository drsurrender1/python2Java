//test@@ test
// test
//
private class MainClass extends TestClass{
    // test3 test
    // test3 
    public int foo(int a, int b) {
        // test3 test
        // test3 
        int c = 2;
        // test3 test
        // test3 
        System.out.println(c); 
        System.out.println("1234"); 
        System.out.println(123); 
        // test3 test
        // test3 
        int d = 4;
        // test3 test
        // test3 
        if (c > d){
            // test3 test
            int e = 5;
            c = 4;
        }
        else if (c == d){
            // test 
            c = 7;
            // test
            d = 2 + 3;
        }
        else{
            int f = 6;
        }
        //test
        c = 8;
        return c;
    }
    //test3
    private int test = foo(2,3);
}