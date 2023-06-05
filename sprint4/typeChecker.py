#!/usr/bin/env python3

from symbolTable import SymbolTable, ParseError
import astJava2Python as ast

class TypeChecker(object):

    def typecheck(self, node, st=None):
        method = 'check_' + node.__class__.__name__
        return getattr(self, method, self.generic_typecheck)(node, st)

    def generic_typecheck(self, node, st=None):
        if node is None:
            return ''
        else:
            return ''.join(self.typecheck(c, st) for c_name, c in node.children())


    def eq_type(self, t1, t2):
        """
        Helper function to check if two given type node is that of the
        same type. Precondition is that both t1 and t2 are that of class Type
        """
        if not isinstance(t1, ast.DeclType) or not isinstance(t2, ast.DeclType):
            raise ParseError("eq_type invoked on non-type objects")
        return t1.name == t2.name

    def check_AssignStmt(self, node, st):
        var_type = st.lookup_variable(node.name, node.coord)
        expr_type = self.typecheck(node.expr, st)
        if not self.eq_type(var_type, expr_type):
            raise ParseError("Variable \"" + node.name + "\" has the type",
                             var_type.name, "but is being assigned the type",
                             expr_type.name)

        return expr_type


    def check_BinOp(self, node, st):
        """
        NOTE
        You should also check if the type of the left and right operation
        makes sense in the context of the operator (ie., you should not be
        able to add/subtract/multiply/divide strings or booleans). In this
        example, it only checks if the left and right expressions are of the
        same type, but that won't be sufficient for your project.
        """
        left_type = self.typecheck(node.left, st)
        right_type = self.typecheck(node.right, st)
        if not self.eq_type(left_type, right_type):
            raise ParseError("Left and right expressions are of different type", node.coord)

        if node.op in ['+', '-', '*', '/']:
            return ast.DeclType("int")

        return ast.DeclType("boolean")

    def check_Constant(self, node, st):
        """
        Returns the type of the constant. If the constant refers to
        some kind of id, then we need to find if the id has been declared.
        """
        if self.eq_type(node.type, ast.DeclType('id')):
            return st.lookup_variable(node.value, node.coord)
        return node.type

    def check_DeclVarStmt(self, node, st):
        st.declare_variable(node.name, node.var_type, node.coord)
        if node.expr is not None:
            expr_type = self.typecheck(node.expr, st)
            if not self.eq_type(expr_type, node.var_type):
                raise ParseError("Mismatch of declaration type", node.coord)

        return node.var_type

    def check_DeclArrayList(self,node,st):
        if node.var_type.name!=node.create_type.name:
            raise ParseError("Mismatch of declaration type", node.coord)
        else:
            st.declare_array_variable(node.name, node.type,node.var_type,node.coord)
            return [node.type,node.var_type]


    def check_Formal(self, node, st):
        st.declare_variable(node.name, node.type, node.coord)
        return node.type

    def check_FuncCall(self, node, st):
        method = st.lookup_method(node.name ,node.coord)

        if len(method.params or []) != len(node.args or []):
            raise ParseError("Argument length mismatch with method", node.coord)

        for i, arg in enumerate(node.args or []):
            arg_type = self.typecheck(arg)
            if not self.eq_type(arg_type, method.params[i].type):
                raise ParseError("Argument type mismatch with method parameter", node.coord)

        return method.ret_type


    def check_DeclIfStmt(self, node, st):
        """
        Check if the condition expression is a boolean type, then
        recursively typecheck all of if statement body.

        Note that most of the programming languages, such as C, Java, and
        Python, all accepts ints/floats for conditions as well. That is
        something you should consider for your project.
        """
        cond_type = self.typecheck(node.if_cond, st)
        if not self.eq_type(ast.DeclType('boolean'), cond_type):
            raise ParseError("If statement requires boolean as its condition", node.coord)

        if node.if_body is not None:
            st.push_scope()
            self.typecheck(node.if_body, st)
            st.pop_scope()
        if node.elif_body is not None:
            st.push_scope()
            self.typecheck(node.elif_body, st)
            st.pop_scope()
        if node.else_body is not None:
            st.push_scope()
            self.typecheck(node.else_body, st)
            st.pop_scope()

        return None


    def check_DeclForStmt(self, node, st):
        """
        Check if the condition expression is a boolean type, then
        recursively typecheck all of if statement body.

        Note that most of the programming languages, such as C, Java, and
        Python, all accepts ints/floats for conditions as well. That is
        something you should consider for your project.
        """
        #check condition
        self.typecheck(node.var_assign, st)
        cond_type = self.typecheck(node.cond, st)
        if not self.eq_type(ast.DeclType('boolean'), cond_type):
            raise ParseError("If statement requires boolean as its condition", node.coord)
        if node.cond_update is not None:
            self.typecheck(node.cond_update, st)
        if node.body is not None:
            st.push_scope()
            self.typecheck(node.body, st)
            st.pop_scope()
        return None

    def check_DeclWhileStmt(self, node, st):
        """
        Check if the condition expression is a boolean type, then
        recursively typecheck all of if statement body.

        Note that most of the programming languages, such as C, Java, and
        Python, all accepts ints/floats for conditions as well. That is
        something you should consider for your project.
        """
        #check condition
        cond_type = self.typecheck(node.cond, st)
        if not self.eq_type(ast.DeclType('boolean'), cond_type):
            raise ParseError("If statement requires boolean as its condition", node.coord)

        if node.body is not None:
            st.push_scope()
            self.typecheck(node.body, st)
            st.pop_scope()
        return None

    
    def check_CompareOp(self, node, st):
        left_type = self.typecheck(node.left, st)
        right_type = self.typecheck(node.right, st)
        if not self.eq_type(left_type, right_type):
            raise ParseError("Left and right expressions are of different type", node.coord)

        if node.op in ['+', '-', '*', '/']:
            return ast.DeclType("int")

        return ast.DeclType("boolean")

    def check_DeclMethodStmt(self, node, st):
        # Go through the parameters
        for param in node.params:
            self.typecheck(param, st)

        st.push_scope()

        # Go through the method body and type check each statements
        if node.body is not None:
            self.typecheck(node.body, st)

        # Check if the type of the return statement matches the return type
        # of the method
        if node.ret_stmt.expr is not None:
            ret_stmt_type = self.typecheck(node.ret_stmt, st)
            if not self.eq_type(ret_stmt_type, node.method_type):
                raise ParseError("Mismatch of return type within method \"" +
                                node.name + "\"", node.coord)
        else:
            ret_stmt_type = ast.DeclType("void", "void")

        st.pop_scope()

        st.declare_method(node.name, node, node.coord)
        return ret_stmt_type

    def check_ParamList(self, node, st):
        """
        Add all of the parameters to the symbol table
        """
        # Alternatively, you could have a separate check method for
        # "Formal" class, instead of declaring them as a variable here.
        if node.params is not None:
            for param in node.params:
                st.declare_variable(param.name, param.type, param.coord)
        return None
    
    def check_FuncCallParamList(self, node, st):
        return node

    def check_Program(self, node, st=None):
        """
        Generate global symbol table. Recursively typecheck its classes and
        add its class symbol table to itself.
        """
        # Generate global symbol table
        global_st = SymbolTable()
        for classes in node.class_decl:
            if isinstance(classes, list):
                for c in classes:
                    self.typecheck(c, global_st)
            else:
                self.typecheck(classes, global_st)

        return global_st

    def check_DeclRetStmt(self, node, st):
        return self.typecheck(node.expr, st)

    def check_DeclClassStmt(self, node, st):
        if node.stmt_list:
            for stmt in node.stmt_list:
                if isinstance(stmt, list):
                    for s in stmt:
                        self.typecheck(s, st)
                else:
                    self.typecheck(stmt, st)
        if node.extend:
            self.typecheck(node.extend, st)
        
        return None

    def check_StmtList(self, node, st):
        """
        Iterate through all the statements and perform typecheck on them.
        """
        for stmt in node.stmt_lst:
            if isinstance(stmt, list):
                for s in stmt:
                    self.typecheck(s, st)
            else:
                self.typecheck(stmt, st)

        # List itself does not have any type
        return None

    def check_DeclType(self, node, st):
        return node

    def check_DeclAccessType(self, node, st):
        return node
    
    def check_Extend(self, node, st):
        return node

    def check_DeclFuncCall(self, node, st):
        method = st.lookup_method(node.func_name, node.coord)
        if len(method.params[0].params or []) != len(node.func_param.func_params or []):
            raise ParseError("Argument length mismatch with method", node.coord)
        for i, param in enumerate(node.func_param.func_params or []):
            param_type = self.typecheck(param)
            if not self.eq_type(param_type, method.params[0].params[i].type):
                raise ParseError("Argument type mismatch with method parameter", node.coord)

        return method.method_type

    def check_FuncCallParam(self, node, st):
        return self.typecheck(node.expr, st)
    
    def check_DeclTryStmt(self, node, st):
        if node.try_stmt_list:
            for stmt in node.try_stmt_list.stmt_lst:
                self.typecheck(stmt, st)
        if node.catch_stmt_list:
            for stmt in node.catch_stmt_list.stmt_lst:
                self.typecheck(stmt, st)
        if node.finally_stmt_list:
            for stmt in node.finally_stmt_list.stmt_lst:
                self.typecheck(stmt, st)
        return node
    
    def check_Comments(self, node, st):
        return node
    
    def check_DeclPrintStmt(self, node, st):
        return self.typecheck(node.expr, st)

    
    def check_Word(self, node, st):
        return node

    def check_DeclObjCall(self, node, st):
        method = st.lookup_method(node.obj_func, node.coord)
        if len(method.params[0].params or []) != len(node.func_param.func_params or []):
            raise ParseError("Argument length mismatch with method", node.coord)
        for i, param in enumerate(node.func_param.func_params or []):
            param_type = self.typecheck(param)
            if not self.eq_type(param_type, method.params[0].params[i].type):
                raise ParseError("Argument type mismatch with method parameter", node.coord)

        return method.method_type

    def check_DeclObjAddCall(self, node, st):
        var_type = st.lookup_variable(node.name, node.coord)
        if len(var_type) !=2:
            raise ParseError("Variable \"" + node.name + "\" is not array")
        exprtype = var_type[1]
        expr_type = self.typecheck(node.expr, st)
        if not self.eq_type(exprtype, expr_type):
            raise ParseError("ARRAY Variable \"" + node.name + "\" has the type",
                             exprtype.name, "but is being assigned the type",
                             expr_type.name)

        return expr_type

    def check_DeclObjRemoveCall(self, node, st):
        var_type = st.lookup_variable(node.name, node.coord)
        if len(var_type) !=3:
            raise ParseError("Variable \"" + node.name + "\" is not map")
        exprtype = var_type[1]
        expr_type = self.typecheck(node.expr, st)
        if not self.eq_type(exprtype, expr_type):
            raise ParseError("Map Variable " + node.name + " has the key type",
                             exprtype.name, "but is being assigned the type",
                             expr_type.name)

        return expr_type

    def check_DeclObjClearCall(self, node, st):
        var_type = st.lookup_variable(node.name, node.coord)
        if len(var_type) !=3:
            raise ParseError("Variable \"" + node.name + "\" is not map")

        return var_type
    def check_DeclObjPutCall(self, node, st):
        var_type = st.lookup_variable(node.name, node.coord)
        if len(var_type) !=3:
            raise ParseError("Variable \"" + node.name + "\" is not MAP")
        exprtype = var_type[1]
        exprtype2 = var_type[2]
        expr_type = self.typecheck(node.expr1, st)
        expr_type2 = self.typecheck(node.expr2, st)
        if not self.eq_type(exprtype, expr_type) :
            raise ParseError("ARRAY Variable \"" + node.name + "\" has the key type",
                             exprtype.name, "but is being added by the value of type",
                             expr_type.name)
        if not self.eq_type(exprtype2, expr_type2) :
            raise ParseError("ARRAY Variable \"" + node.name + "\" has the value type",
                             exprtype2.name, "but is being added by the value of type",
                             expr_type2.name)

        return [expr_type,expr_type2]
    def check_DeclHashMap(self,node,st):
        if node.type!=node.create_type or node.key_type.name!=node.create_keytype.name or node.value_type.name!=node.create_valuetype.name :
            raise ParseError("Mismatch of declaration type", node.coord)
        else:
            st.declare_hashmap_variable(node.name, node.type,node.key_type,node.value_type,node.coord)
            return [node.type, node.key_type, node.value_type]

