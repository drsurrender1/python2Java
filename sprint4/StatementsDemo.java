// This document shows how statements and data types are converted by our compiler
public class StatementsDemo{

    // boolean variable
    boolean var1 = true;

    // method declaration
    public int method1(int a, int b) {

        // int variable 
        int var2 = 2;

        // string variable
        String var3 = "demostration";

        // if/else statement
        if (var2 < 5){
            var1 = false;
        }
        else if (var2 == 2){
            var3 = "completed";
        }
        else{
            var2 = 1;
        }

        // while loop
        while (var2 < 20){

            //for loop 
            for (int i = 0; i < 5; i = i + 1){
                System.out.println(i);
            }

            // math operator
            var2 = var2 + 1;
        }

        // return statement
        return a;
    }

    // function call
    int fun1 = method1(5, 6);

    int try1 = 1;

    try {
        try1 = 1 / 0;
    }
    catch (Exception e){
        System.out.println("error raised");
    }
    finally{
        System.out.println("completed");
    }
}