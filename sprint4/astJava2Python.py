#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
# from sympy import root

class Node(object):
    """
    Abstract class for AST nodes.
    """
    # __init__ to be overwritten by child classes

    def children(self):
        """
        sequence of all children that are nodes, 
        
        To be overwritten by child classes
        """
        pass
    
    # Set of attributes for a given node
    attr_names = ()

class DeclClassStmt(Node):
    """
    This subclass is for class_statement in lexical specs.
    For example:
        class MyClass {
        }
    """   
    def __init__(self, access_type, name, extends, stmt_list, coord=None):
        """
        initialize tokens

        @params
        name: name of class
        extends: the class this class extends
        var_stmt: node from DeclVarStmt
        method_stmt: node from DeclMethodStmt
        coord: error index
        """
        self.name = name
        self.access_type = access_type
        self.extend = extends
        self.stmt_list = stmt_list
        self.coord = coord

    def children(self):
        lst = []
        if self.extend is not None:
            lst.append(('extend', self.extend))
        if self.access_type is not None:
            lst.append(('access_type', self.access_type))
        if self.stmt_list is not None:
            lst.append(('stmt_list', self.stmt_list))
        return tuple(lst)

    attr_names = ('name', )


class Extend(Node):
    """
    This class is for class inheritence information.
    """
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        return tuple([])

    attr_names = ('name', )

class DeclVarStmt(Node):
    """
    This subclass is for var_statement in lexical specs.
    For example:
        int i;
        int i = 0;
    """
    def __init__(self, access_type, var_type, name, expr=None, coord=None):
        """
        initialize tokens

        @params
        access_type: 'public'|'private'| None
        var_type: type of the variable
        name: name of statement
        expr: expression
        """
        self.access_type = access_type
        self.var_type = var_type
        self.name = name
        self.expr = expr
        self.coord = coord
    
    def children(self):
        lst = []
        if self.access_type is not None:
            lst.append(('access_type', self.access_type))
        if self.var_type is not None:
            lst.append(('type', self.var_type))
        if self.expr is not None:
            lst.append(('expr', self.expr))
        return tuple(lst)

    attr_names = ('name', )
class DeclObjRemoveCall(Node):
    def __init__(self, obj_name, obj_func, expr, coord=None):
        self.name = obj_name
        self.obj_func = obj_func
        self.expr = expr
        self.coord = coord

    def children(self):
        lst = []
        if self.expr is not None:
            lst.append(('func_param', self.expr))
        if self.name is not None:
            lst.append(('object name', self.name))
        if self.obj_func is not None:
            lst.append(('object func name', self.obj_func))
        return tuple(lst)

    attr_names = ('obj_add_name')
    
class DeclObjClearCall(Node):
    def __init__(self, obj_name, obj_func, coord=None):
        self.name = obj_name
        self.obj_func = obj_func
        self.coord = coord

    def children(self):
        lst = []
        if self.name is not None:
            lst.append(('object name', self.name))
        if self.obj_func is not None:
            lst.append(('object func name', self.obj_func))
        return tuple(lst)
    attr_names = ('obj_add_name')
class DeclObjPutCall(Node):
    def __init__(self, obj_name, obj_func, expr1,expr2, coord=None):
        self.name = obj_name
        self.obj_func = obj_func
        self.expr1 = expr1
        self.expr2 = expr2
        self.coord = coord

    def children(self):
        lst = []
        if self.expr1 is not None:
            lst.append(('func_param1', self.expr1))
        if self.expr2 is not None:
            lst.append(('func_param2', self.expr2))
        if self.name is not None:
            lst.append(('object name', self.name))
        if self.obj_func is not None:
            lst.append(('object func name', self.obj_func))
        return tuple(lst)

    attr_names = ('obj_put_name')

class DeclHashMap(Node):
    def __init__(self, type,  key_type, value_type, name, create_type, create_keytype, create_valuetype, coord=None):
        self.type = type
        self.key_type = key_type
        self.value_type = value_type
        self.create_type = create_type
        self.name = name
        self.create_keytype = create_keytype
        self.create_valuetype = create_valuetype
        self.coord = coord

    def children(self):
        lst = []
        if self.type is not None:
            lst.append(('type', self.type))
        if self.key_type is not None:
            lst.append(('key_type', self.key_type))
        if self.value_type is not None:
            lst.append(('value_type', self.key_type))
        if self.name is not None:
            lst.append(('name', self.name))
        if self.create_type is not None:
            lst.append(('create_type', self.create_type))
        if self.create_keytype is not None:
            lst.append(('create_keytype', self.create_keytype))
        if self.create_valuetype is not None:
            lst.append(('create_valuetype', self.create_valuetype))
        print("hashmap children", lst)
        return tuple(lst)
    attr_names = ('name',)

class DeclMethodStmt(Node):
    """
    This subclass is for method_statement in lexical specs.
    This also works for main_method_statement.
    For example: 
        public void example(String s) {

        }
    """
    def __init__(self, access_type, method_type, name, params, body, main=False, coord=None):
        """
        initialize tokens

        @params
        access_type : 'public'|'private' | None
        method_type : method return type
        name: method name
        params: parameters
        body: body statements, including return statement
        coord: error index
        """
        self.access_type = access_type
        self.method_type = method_type
        self.name = name
        if not isinstance(params, list):
            self.params = [params]
        else:
            self.params = params
        self.body = body
        self.coord = coord
        if self.method_type.name == 'void':
            self.ret_stmt = DeclRetStmt(None)
        else:
            self.ret_stmt = self.body.stmt_lst[-1]
            self.body = StmtList(body.stmt_lst[:-1])
        self.main = main

    def children(self):
        lst = []
        if self.access_type is not None:
            lst.append(('access_type', self.access_type))
        if self.method_type is not None:
            lst.append(('type', self.method_type))
        if self.body is not None:
            lst.append(('body', self.body))
        if self.params is not None:
            lst.append(('params', self.params))
        if self.ret_stmt is not None:
            lst.append(('ret_stmt', self.ret_stmt))
        return tuple(lst)       

    attr_names = ('name', )

class DeclAccessType(Node):
    """
    This subclass is for access_type in lexical specs.
    """
    def __init__(self, name, coord=None):
        """
        initialize tokens
        """
        self.name = name
        self.coord = coord
    
    def children(self):
        lst = []
        return tuple(lst)
    attr_names = ('name', )

class AssignStmt(Node):
    def __init__(self, name, expr, this=False, coord=None):
        self.name = name
        self.expr = expr
        self.coord = coord
        self.this = this

    def children(self):
        lst = []
        if self.expr is not None:
            lst.append(('expr', self.expr))
        return tuple(lst)

    attr_names = ('name', )

class DeclArrayList(Node):
    def __init__(self, type,  var_type, name, create_type, coord=None):
        self.type = type
        self.var_type = var_type
        self.name = name
        self.create_type = create_type
        self.coord = coord

    def children(self):
        lst = []
        if self.type is not None:
            lst.append(('type', self.type))
        if self.var_type is not None:
            lst.append(('var_type', self.var_type))
        if self.name is not None:
            lst.append(('name', self.name))
        if self.create_type is not None:
            lst.append(('create_type', self.create_type))
        return tuple(lst)
    attr_names = ('name',)

class DeclType(Node):
    """
    This subclass is for type in lexical specs.
    """
    def __init__(self, name, coord=None):
        """
        initialize tokens
        """
        self.name = name
        self.coord = coord
    
    def children(self):
        lst = []
        return tuple(lst)
    attr_names = ('name', ) 

class ParamList(Node):
    """
    This subclass is for parameter lists. 
    """
    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord

    def children(self):
        lst = []
        for i, child in enumerate(self.params or []):
            lst.append(('params[%d]' % i, child))
        return tuple(lst)
    attr_names = ()    

class FuncCallParamList(Node):
    def __init__(self, func_params, coord=None):
        self.func_params = func_params
        self.coord = coord

    def children(self):
        lst = []
        for i, child in enumerate(self.func_params or []):
            lst.append(('func_params[%d]' % i, child))
        return tuple(lst)
    attr_names = ()    

class Param(Node):
    def __init__(self, stmt_type, name, coord=None):
        self.name = name
        self.type = stmt_type
        self.coord = coord

    def children(self):
        lst = []
        if self.type is not None:
            lst.append(('type', self.type))
        return tuple(lst)

    attr_names = ('name', )

class FuncCallParam(Node):
    def __init__(self, value, coord=None):
        self.expr = value
        self.coord = coord
    
    def children(self):
        lst=[]
        return tuple(lst)
    
    attr_names = ('name', )

# class FuncCallParam(Node):
#     def __init__(self, stmt_type, name, coord=None):
#         self.name = name
#         self.type = stmt_type
#         self.coord = coord
    
#     def children(self):
#         lst=[]
#         if self.type is not None:
#             lst.append(('type', self.type))
#         return tuple(lst)
#     attr_names = ('name', )

class DeclFuncCall(Node):
    def __init__(self, access_type, var_type, name, func_name, expr, coord=None):
        self.access_type = access_type
        self.var_type = var_type
        self.name = name
        self.func_name = func_name
        self.func_param = expr
        self.coord = coord
    
    def children(self):
        lst = []
        if self.access_type is not None:
            lst.append(('access_type', self.access_type))
        if self.var_type is not None:
            lst.append(('type', self.var_type))
        if self.func_param is not None:
            lst.append(('func_param', self.func_param))
        return tuple(lst)

    attr_names = ('name', )

class DeclObjCall(Node):
    def __init__(self, obj_name, obj_func, expr, coord=None):
        self.obj_name = obj_name
        self.obj_func = obj_func
        self.func_param = expr
        self.coord = coord
    
    def children(self):
        lst = []
        if self.func_param is not None:
            lst.append(('func_param', self.func_param))
        if self.obj_name is not None:
            lst.append(('object name', self.obj_name))
        if self.obj_func is not None:
            lst.append(('object func name', self.obj_func))
        return tuple(lst)
    
    attr_names = ('obj_name')


class DeclObjAddCall(Node):
    def __init__(self, obj_name, obj_func, expr, coord=None):
        self.name = obj_name
        self.obj_func = obj_func
        self.expr = expr
        self.coord = coord

    def children(self):
        lst = []
        if self.expr is not None:
            lst.append(('func_param', self.expr))
        if self.name is not None:
            lst.append(('object name', self.name))
        if self.obj_func is not None:
            lst.append(('object func name', self.obj_func))
        return tuple(lst)

    attr_names = ('obj_add_name')

class StmtList(Node):
    def __init__(self, stmt_lst, coord=None):
        self.stmt_lst = stmt_lst
        self.coord = coord

    def children(self):
        lst = []
        for i, stmt in enumerate(self.stmt_lst or []):
            lst.append(('stmt[%d]' % i, stmt))
        return lst

    attr_names = ()

class DeclRetStmt(Node):
    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):
        lst = []
        if self.expr is not None:
            lst.append(('expr', self.expr))
        return tuple(lst)

    attr_names = ()

class DeclIfStmt(Node):
    """
    This class is for If statement. 
    """
    def __init__(self, if_cond, if_body, elif_cond, elif_body, else_body, coord=None):
        self.if_cond = if_cond
        self.if_body = if_body
        self.elif_cond = elif_cond
        self.elif_body = elif_body
        self.else_body = else_body
        self.coord = coord

    def children(self):
        lst = []
        if self.if_cond is not None:
            lst.append(('cond', self.if_cond))
        if self.if_body is not None:
            lst.append(('if_body', self.if_body))
        if self.elif_cond is not None:
            lst.append(('elif_cond', self.elif_cond))
        if self.elif_body is not None:
            lst.append(('elif_body', self.elif_body))
        if self.else_body is not None:
            lst.append(('else_body', self.else_body))
        return tuple(lst)

    attr_names = ()

class DeclWhileStmt(Node):
    """
    This class is for While statement
    """
    def __init__(self, cond, body, coord=None):
        self.cond = cond
        self.body = body
        self.coord = coord

    def children(self):
        lst = []
        if self.cond is not None:
            lst.append(('cond', self.cond))
        if self.body is not None:
            lst.append(('body', self.body))
        return tuple(lst)

    attr_names = ()

class DeclForStmt(Node):
    """
    This class is for For statement
    """
    def __init__(self, var_assign, cond, update, body, coord=None):
        self.var_assign = var_assign
        self.cond = cond
        self.body = body
        self.coord = coord
        self.cond_update = update

    def children(self):
        lst = []
        if self.var_assign is not None:
            lst.append(('expr', self.var_assign))
        if self.cond is not None:
            lst.append(('cond', self.cond))
        if self.body is not None:
            lst.append(('body', self.body))
        if self.cond_update is not None:
            lst.append(('cond_update', self.cond_update))
        return tuple(lst)

    attr_names = ()

class DeclTryStmt(Node):
    """
    This class is for Try Statement
    """
    def __init__(self, try_stmt_list, catch_id, \
    catch_stmt_list, finally_stmt_list=None, coord=None):
        self.try_stmt_list = try_stmt_list
        self.catch_id = DeclType(catch_id)
        self.catch_stmt_list = catch_stmt_list
        self.finally_stmt_list = finally_stmt_list

    def children(self):
        lst=[]
        if self.try_stmt_list is not None:
            lst.append(('try_stmt_list', self.try_stmt_list))
        if self.catch_id is not None:
            lst.append(('catch_id', self.catch_id))
        if self.catch_stmt_list is not None:
            lst.append(('cacth_stmt_list', self.catch_stmt_list))
        if self.finally_stmt_list is not None:
            lst.append(('finally_stmt_list', self.finally_stmt_list))
        return tuple(lst)
    attr_names = ()

class ObjInstance(Node):
    def __init__(self, obj, coord=None):
        self.obj = obj
        self.coord = coord

    def children(self):
        lst = []
        return tuple(lst)

    attr_names = ('obj', )

class BinOp(Node):
    """
    This class is for binary operation. 
    """
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord

    def children(self):
        lst = []
        if self.left is not None:
            lst.append(('left', self.left))
        if self.right is not None:
            lst.append(('right', self.right))
        return tuple(lst)

    attr_names = ('op', )

class UnaryOp(Node):
    """
    This class is for negation operation.
    """
    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr
        self.coord = coord

    def children(self):
        lst = []
        if self.expr is not None:
            lst.append(('expr', self.expr))
        return tuple(lst)

    attr_names = ('op', )

class LogicOp(Node):
    """
    This class is for logic operation.
    """
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord
    
    def children(self):
        lst = []
        if self.left is not None:
            lst.append(('left', self.left))
        if self.right is not None:
            lst.append(('right', self.right))
        return tuple(lst)

    attr_names = ('op', )        

class CompareOp(Node):
    """
    This class is for compare operator.
    """
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord
    
    def children(self):
        lst = []
        if self.left is not None:
            lst.append(('left', self.left))
        if self.right is not None:
            lst.append(('right', self.right))
        return tuple(lst)

    attr_names = ('op', )       

class Constant(Node):
    """
    This class is for constant. 
    """
    def __init__(self, var_type, value, coord=None):
        self.type = DeclType(var_type)
        self.value = value
        self.coord = coord

    def children(self):
        lst = []
        return tuple(lst)

    attr_names = ('type', 'value', )

class Program(Node):
    def __init__(self, class_decl, coord=None):
        self.class_decl = class_decl  #now it becomes a list of class declarations
    def children(self):
        lst = []

        if self.class_decl is not None:
            lst.append(('class_decl', self.class_decl))
        
        return tuple(lst)
    
class Comments(Node):
    def __init__(self, words, coord=None):
        if not isinstance(words, list):
            self.words = [words]
        else:
            self.words = words
    
    def children(self):
        lst = []
        if self.words is not None:
            lst.append(('Comments info', self.words))
        return tuple(lst)
    attr_names = ('comments', )  

class DeclPrintStmt(Node):
    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord
    def children(self):
        lst=[]
        if self.expr is not None:
            lst.append(("expr", DeclType(self.expr)))
        return tuple(lst)
    attr_names = ('print', )

class Word(Node):
    """
    This class is for word. 
    """
    def __init__(self, value, coord=None):
        self.value = value
        self.coord = coord

    def children(self):
        lst = []
        if self.value is not None:
            lst.append('value', self.value)
        return tuple(lst)

    attr_names = ('word', )