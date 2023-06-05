public class demo{
    //optimization3 
    ArrayList<int> sites = new ArrayList<int>();
    sites.add(1);
    sites.add(2);
    String var3 = "demostration";
    // this for loop will be optimized by dead code elimination    
    for (int i = 0; i < 5; i = i + 1){
        int dead = 1;
    }
    int opt2 = 2;    
    // loops will be merged by loop fusion based on update steps
    // pay attention to var3
    while (opt2 < 20){
        var3 = "merge1";
        opt2 = opt2 + 1;
    }
    while (opt2 < 20){
        // opt3 to be optimized
        int opt3 = 5;
        var3 = "merge3";
        opt2 = opt2 + 2;
    }
    while (opt2 < 20){
        var3 = "merge4";
        opt2 = opt2 + 2;
    }
    while (opt2 < 20){
        var3 = "merge2";
        opt2 = opt2 + 1;
    }
}