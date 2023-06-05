class demo:
    # optimization3 
    sites = [1, 2]
    var3 = "demostration"
    #  this for loop will be optimized by dead code elimination    
    opt2 = 2
    #  loops will be merged by loop fusion based on update steps
    #  pay attention to var3
    while (opt2 < 20):
        #  opt3 to be optimized
        var3 = "merge3"
        opt2 = opt2 + 2
        var3 = "merge4"
    while (opt2 < 20):
        var3 = "merge1"
        opt2 = opt2 + 1
        var3 = "merge2"
