#!/usr/bin/env python3

class IRGen(object):
    """
    Uses the same visitor pattern as TypeChecker. It is modified to
    generate 3AC (Three Address Code) in a simple string.

    Bare in mind that this is for demonstration purpose only! For your
    actual project, you would want to generate some sort of objects rather
    than plain string. However, this should help you think about what you
    might want/need to do to convert your AST to your IR of choice.

    As mentioned in the tutorial, you are free to choose which IR you
    want to generate. I suggest you look into different optimization,
    as well as think about how your IR of choice will translate to your
    target language, since you would need to argue why your IR of choice
    makes sense for Sprint2.
    """

    def __init__(self):
        """
        IR_lst: list of IR code
        register_count: integer to keep track of which register to use
        label_count: similar to register_count, but with labels
        """
        self.IR_lst = []
        self.register_count = 0
        self.label_count = 0

    def generate(self, node):
        """
        Similar to 'typecheck' method from TypeChecker object
        """
        method = 'gen_' + node.__class__.__name__
        return getattr(self, method)(node)

    ################################
    ## Helper functions
    ################################

    def add_code(self, code):
        """
        Add 'code' to the IR_lst with correct spacing
        """
        self.IR_lst.append("    " + code)

    def inc_register(self):
        """
        Increase the register count and return its value for use
        """
        self.register_count += 1
        return self.register_count

    def reset_register(self):
        """
        Can reset the register_count to reuse them
        """
        self.register_count = 0

    def inc_label(self):
        """
        Increase the label count and return its value for use
        """
        self.label_count += 1
        return self.label_count

    def mark_label(self, label):
        """
        Add label mark to IR_lst
        """
        self.IR_lst.append("_L{}:".format(label))

    def print_ir(self):
        """
        Loop through the generated IR code and print them out to stdout
        """
        for ir in self.IR_lst:
            print(ir)

    def gen_AssignStmt(self, node):
        expr = self.generate(node.expr)
        self.add_code("{} := {}".format(node.name, expr))
        self.register_count = 0

    def gen_BinOp(self, node):
        # Left operand
        left = self.generate(node.left)
        # Right operand
        right = self.generate(node.right)

        reg = self.inc_register()
        self.add_code("{} := {} {} {}".format('_t%d' % reg, left, node.op, right))

        return '_t%d' % reg
    
    def gen_CompareOp(self, node):
        # Left operand
        left = self.generate(node.left)
        # Right operand
        right = self.generate(node.right)

        reg = self.inc_register()
        self.add_code("{} := {} {} {}".format('_t%d' % reg, left, node.op, right))

        return '_t%d' % reg

    def gen_Constant(self, node):
        return node.value

    def gen_DeclStmt(self, node):
        expr = self.generate(node.expr)
        self.add_code("{} := {}".format(node.name, expr))
        self.register_count = 0

    def gen_DeclFuncCall(self, node):

        # Push all of the arguments with "PushParam" function
        args = node.children()[2][1]
        for param in args.func_params:
            expr = self.generate(param)
            self.add_code("PushParam {}".format(expr) )

        # Once all of the parameter has been pushed, actually call the function
        self.add_code("FuncCall %s" % node.func_name)

        # After we're done with the function, remove the spaces reserved
        # for the arguments
        self.add_code("PopParams %d" % len(args.func_params))

        reg = self.inc_register()
        self.add_code("{} := ret".format('_t%d' % reg))

        self.add_code("{} := {}".format(node.name, '_t%d' % reg))
        return '_t%d' % reg

    def gen_DeclIfStmt(self, node):
        cond = self.generate(node.if_cond)

        fbranch_label = self.inc_label()
        tbranch_label = self.inc_label()

        if not node.elif_cond:
            # Skip to the false_body if the condition is not met
            self.add_code("if !({}) goto {}".format(cond, '_L%d' % fbranch_label))
            self.generate(node.if_body)
            # Make sure the statements from false_body is skipped
            self.add_code("goto _L%d" % tbranch_label)

            self.mark_label(fbranch_label)
            self.generate(node.else_body)
            self.mark_label(tbranch_label)
        else:
            elifbranch_label = self.inc_label()
            elifcond = self.generate(node.elif_cond)
            # not if go to elseif
            self.add_code("if !({}) goto {}".format(cond, '_L%d' % elifbranch_label))
            self.generate(node.if_body)
             # Make sure the statements from false_body is skipped
            self.add_code("goto _L%d" % tbranch_label)

            # process elif situation            
            self.mark_label(elifbranch_label)
            self.add_code("elif !({}) goto {}".format(elifcond, '_L%d' % fbranch_label))
            self.generate(node.elif_body)
            self.add_code("goto _L%d" % tbranch_label)

            #else situation
            self.mark_label(fbranch_label)
            self.generate(node.else_body)
            #end if statement
            self.mark_label(tbranch_label)

    def gen_DeclWhileStmt(self, node):
        self.add_code("Begin While Loop")
        cond = self.generate(node.cond)
        fbranch_label = self.inc_label()
        tbranch_label = self.inc_label()

        self.mark_label(tbranch_label)
        # Skip to the false_body if the condition is not met
        self.add_code("if !({}) goto {}".format(cond, '_L%d' % fbranch_label))
        self.generate(node.body)
        # Make sure the statements from false_body is skipped
        self.add_code("goto _L%d" % tbranch_label)

        self.mark_label(fbranch_label)

    def gen_DeclTryStmt(self, node):

        # Allocate room for function local variables
        if not node.finally_stmt_list:
            self.add_code("BeginTryCatch")
            cond = self.generate(node.try_stmt_list)
            fbranch_label = self.inc_label()
            tbranch_label = self.inc_label()

            # Skip to the false_body if the condition is not met
            self.add_code("if an execption happen in try, goto {}".format('_L%d' % fbranch_label))
        
            # Make sure the statements from false_body is skipped
            self.add_code("goto _L%d" % tbranch_label)

            self.mark_label(fbranch_label)
            exception_id = self.generate(node.catch_id)
            self.add_code("Exception := {} ".format(exception_id))
            catchcond = self.generate(node.catch_stmt_list)
            self.mark_label(tbranch_label)
            self.add_code("No Finally Statements, FinishTryCatch")
        else:
            fin_lable =  self.inc_label()  # finally label, end place
            self.add_code("BeginTryCatch")  
            fbranch_label = self.inc_label()
            tbranch_label = self.inc_label()
            
            cond = self.generate(node.try_stmt_list)

            # Skip to the false_body if the condition is not met
            self.add_code("if an execption happened in try, goto {}".format('_L%d' % fbranch_label))
            # Make sure the statements from false_body is skipped
            self.add_code("goto _L%d" % fin_lable)

            self.mark_label(fbranch_label)
            exception_id = self.generate(node.catch_id)
            self.add_code("Exception := {} ".format(exception_id))
            catchcond = self.generate(node.catch_stmt_list)
            self.mark_label(fin_lable)
            fincond = self.generate(node.finally_stmt_list)
            self.add_code("FinishTryCatch")

    def gen_DeclMethodStmt(self, node):
        skip_decl = self.inc_label()
        # We want to skip the function code until it is called
        self.add_code("goto _L%d" % skip_decl)

        # Function label
        self.mark_label(node.name)

        # Allocate room for function local variables
        self.add_code("BeginFunc")

        # Actually generate the main body
        
        self.generate(node.body)
        self.generate(node.ret_stmt)

        # Do any cleanup before jumping back
        self.add_code("EndFunc")

        self.mark_label(skip_decl)

    def gen_Program(self, node):
        for (child_name, child) in node.children():
            for c in child:
                self.generate(c)

    def gen_DeclRetStmt(self, node):
        if node.expr:
            expr = self.generate(node.expr)
            self.add_code("ret := {}".format(expr))

    def gen_StmtList(self, node):
        for stmt in node.stmt_lst:
            self.generate(stmt)
        reg = self.inc_register()
        return '_t%d' % reg

    def gen_DeclClassStmt(self, node):
        self.mark_label(node.name)
        self.add_code("BeginClass")
        if node.stmt_list:
            for stm in node.stmt_list:
                self.generate(stm)
        self.add_code("EndClass")
    
    def gen_DeclVarStmt(self, node):
        expr = self.generate(node.expr)
        reg = self.inc_register()
        self.add_code("{} := {}".format(node.name, expr))

    def gen_FuncCallParamList(self, node):
        result = 0
        if node.func_params:
            for param in node.func_params:
                expr = self.generate(param)
                result += expr
        return result
    
    def gen_FuncCallParam(self, node):
        if node.expr:
            expr = self.generate(node.expr)
            return expr
    
    def gen_DeclAccessType(self, node):
        if node.name is None:
            return ''
        temp = self.generate(node.name)
        return temp

    def gen_DeclType(self, node):
        return node.name

    def gen_DeclForStmt(self, node):
        self.add_code("Begin For Loop")
        var_name = self.generate(node.var_assign)
        cond = self.generate(node.cond)
        fbranch_label = self.inc_label()
        tbranch_label = self.inc_label()

        self.mark_label(tbranch_label)
        # Skip to the false_body if the condition is not met
        self.add_code("if !({}) goto {}".format(cond, '_L%d' % fbranch_label))
        self.generate(node.body)
        update_rule = self.generate(node.cond_update)
        # Make sure the statements from false_body is skipped
        self.add_code("goto _L%d" % tbranch_label)

        self.mark_label(fbranch_label)