class MainClass{
    public int foo(int a, int b) {
        int e = 3;
        try{
			e = 4;
		}
		catch (Exception f){
			e = 5;
		}
        finally{
            e = 6;
        }
        return e;
    }
    int test = foo(2,3);
}