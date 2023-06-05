#!/usr/bin/env python3
import argparse
from ply import yacc
from scanner import Scanner
import astJava2Python as ast

import xml.etree.ElementTree as ET
# from sympy import root
from scanner import tokens

class Parser:
    precedence = (
        ('left', 'AND', 'OR'),
        ('left', 'DOUBLEEQ', 'NEQ'),
        ('left', 'LESS', 'LESSEQ', 'GREATER', 'GREATEREQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UNARY')
    )

    start = 'program'

    def __init__(self):
        """
        Builds the Lexer and Parser
        """
        self.tokens = tokens
        self.lexer = Scanner()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        """
        Returns the root (Program) node of the AST, after parsing the file
        """
        return self.parser.parse(data)

    ################################
    ## Program (starting point)
    ################################

    def p_program(self, p):
        '''
        program : class_decl_or_empty
        '''
        p[0] = ast.Program(p[1]) 
    
    def p_print_stmt(self, p):
        '''
        print_stmt : PRINT LPAREN expr RPAREN SEMICOL

        '''
        p[0] = ast.DeclPrintStmt(p[3])
    
    def p_comments_lst(self, p):
        '''
        comments_lst : comments_lst comments
                     | comments
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
    
    def p_comments(self, p):
        '''
        comments : words_lst
        '''
        p[0] = ast.Comments(p[1])

    def p_comments_lst_or_empty(self, p):
        '''
        comments_lst_or_empty : comments_lst
                              | empty
        ''' 
        p[0] = p[1]
    
    def p_words_lst(self, p):
        '''
        words_lst : words_lst COMM
                  | COMM
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]
    
    ################################
    ## Class/Var/Method Declarations
    ################################

    def p_class_decl_or_empty(self, p):
        '''
        class_decl_or_empty : class_lst
                            | empty
        '''
        p[0] = p[1]

    def p_object_put_stmt(self, p):
        '''
        obj_call_stmt : ID PERIOD PUT LPAREN expr COMMA expr RPAREN SEMICOL
        '''
        p[0] = ast.DeclObjPutCall(p[1], p[3], p[5],p[7])

    def p_object_clear_stmt(self, p):
        '''
        obj_call_stmt : ID PERIOD CLEAR LPAREN RPAREN SEMICOL
        '''
        p[0] = ast.DeclObjClearCall(p[1], p[3])

    def p_class_list(self, p):
        '''
        class_lst : class_lst comments_lst_or_empty class_decl
                  | comments_lst_or_empty class_decl
        '''
        if len(p) == 3:
            p[0] = [p[1]] + [p[2]]
        else:
            p[0] = p[1] + [p[2]] + [p[3]]

    def p_class_decl(self, p):
        '''
        class_decl : access_or_empty CLASS ID ext_or_empty LBRACE decl_lsts RBRACE
        '''
        p[0] = ast.DeclClassStmt(p[1], p[3], p[4], p[6])

    def p_access_or_empty(self, p):
        '''
        access_or_empty : access_type
                        | empty
        '''
        p[0] = ast.DeclAccessType(p[1])

    def p_access_type(self, p):
        """
        access_type : PUBLIC
                    | PRIVATE
        """
        p[0] = p[1]
    
    def p_extend_or_empty(self, p):
        '''
        ext_or_empty : extends
                     | empty
        '''
        p[0] = p[1]

    def p_extend(self, p):
        '''
        extends : EXTENDS ID
        '''
        p[0] = ast.Extend(p[2])
    
    def p_decl_lists(self, p):
        '''
        decl_lsts : decl_lsts comments_lst_or_empty decl_lst
                  | comments_lst_or_empty decl_lst
        '''
        if len(p) == 3:
            p[0] = [p[1]] + [p[2]]
        else:
            p[0] = p[1] + [p[2]] + [p[3]]

    def p_decl_list(self, p):
        '''
        decl_lst : method_decl_stmt
                 | stmt
        '''
        p[0] = p[1]
    
    def p_var_decl_stmt(self, p):
        '''
        var_decl_stmt : access_or_empty type ID SEMICOL
                      | access_or_empty type ID EQ expr SEMICOL
        '''
        if len(p) == 5:
            p[0] = ast.DeclVarStmt(p[1], p[2], p[3])
        if len(p) == 7:
            p[0] = ast.DeclVarStmt(p[1], p[2], p[3], p[5])
    
    def p_func_call_stmt(self, p):
        '''
        func_call_stmt : access_or_empty type ID EQ ID func_call_params SEMICOL
                       | ID ID EQ NEW ID func_call_params SEMICOL
        '''
        if isinstance(p[1], ast.DeclAccessType):
            p[0] = ast.DeclFuncCall(p[1], p[2], p[3], p[5], p[6])
        else:
            p[0] = ast.DeclFuncCall(None, p[1], p[2], p[5], p[6])

    def p_object_remove_stmt(self, p):
        '''
        obj_call_stmt : ID PERIOD REMOVE LPAREN expr RPAREN SEMICOL
        '''
        p[0] = ast.DeclObjRemoveCall(p[1], p[3], p[5])
    def p_object_add_stmt(self, p):
        '''
        obj_call_stmt : ID PERIOD ADD LPAREN expr RPAREN SEMICOL
        '''
        p[0] = ast.DeclObjAddCall(p[1], p[3], p[5])

    def p_object_call_stmt(self, p):
        '''
        obj_call_stmt : ID PERIOD ID func_call_params SEMICOL
        '''
        p[0] = ast.DeclObjCall(p[1], p[3], p[4])

    def p_func_call_params(self, p):
        '''
        func_call_params : LPAREN func_call_param_lst_or_empty RPAREN
        '''
        p[0] = ast.FuncCallParamList(p[2])
    
    def p_func_params_or_empty(self, p):
        '''
        func_call_param_lst_or_empty : func_call_param_lst
                                     | empty
        '''
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]
    
    def p_func_call_param_lst(self, p):
        '''
        func_call_param_lst : func_call_param_lst COMMA func_call_param
                            | func_call_param
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    
    def p_func_call_param(self, p):
        '''
        func_call_param : expr
        '''
        p[0] = ast.FuncCallParam(p[1])
    
    def p_method_decl_stmt(self, p):
        '''
        method_decl_stmt : access_or_empty STATIC VOID MAIN method_params LBRACE stmts_or_empty RBRACE 
                         | access_or_empty type ID method_params LBRACE stmts_or_empty RBRACE 
        '''
        if len(p) == 9:
            void_type = ast.DeclType("void", "void")
            p[0] = ast.DeclMethodStmt(p[1], void_type, "main", p[5], p[7], True)
        else:
            p[0] = ast.DeclMethodStmt(p[1], p[2], p[3], p[4], p[6], False) 
    
    def p_method_params(self, p):
        '''
        method_params : LPAREN param_or_empty RPAREN
                      | LPAREN STRING LBRACK RBRACK ID RPAREN
        '''
        if len(p) == 4:
            p[0] = ast.ParamList(p[2])
        else:
            p[0] = ast.ParamList([])

    def p_param_or_empty(self, p):
        '''
        param_or_empty : param_lst
                       | empty
        '''
        if len(p) == 1:
            p[0] = []
        else:
            p[0] = p[1]
            
    def p_param_lst(self, p):
        '''
        param_lst : param_lst COMMA param
                  | param
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]
    
    def p_param(self, p):
        '''
        param : type ID
        '''
        p[0] = ast.Param(p[1], p[2])  
    
    def p_statements_or_empty(self, p):
        '''
        stmts_or_empty : stmt_lst
                       | empty
        '''
        p[0] = ast.StmtList(p[1])
    
    def p_statement_list(self, p):
        '''
        stmt_lst : stmt_lst comments_lst_or_empty stmt
                 | comments_lst_or_empty stmt
        '''
        if len(p) == 3:
            p[0] = [p[1]] + [p[2]]
        else:
            p[0] = p[1] + [p[2]] + [p[3]]
    
    def p_statement(self, p):
        '''
        stmt : assign_stmt
             | var_decl_stmt
             | if_stmt
             | while_stmt
             | for_stmt
             | try_stmt
             | ret_stmt
             | func_call_stmt
             | print_stmt
             | obj_call_stmt
             | array_lst
             | hash_map
        '''
        p[0] = p[1]
    
    def p_assign_statement(self, p):
        '''
        assign_stmt : ID EQ expr SEMICOL
                    | ID EQ expr
                    | THIS PERIOD ID EQ expr SEMICOL
        '''
        if len(p) == 5 or len(p) == 4:
            p[0] = ast.AssignStmt(p[1], p[3])
        if len(p) == 7:
            p[0] = ast.AssignStmt(p[3], p[5], True)
    
    def p_if_statement(self, p):
        '''
        if_stmt : IF LPAREN expr RPAREN scope ELSE scope
                | IF LPAREN expr RPAREN scope ELSE IF LPAREN expr RPAREN scope ELSE scope
        '''
        if len(p) <= 8:
            p[0] = ast.DeclIfStmt(p[3], p[5], None, None, p[7])
        else:
            p[0] = ast.DeclIfStmt(p[3], p[5], p[9], p[11], p[13])
    
    def p_scope(self, p):
        '''
        scope : LBRACE stmts_or_empty RBRACE
        '''
        p[0] = p[2]

    def p_array_list(self,p):
        '''
        array_lst : ARRAYLIST LESS type GREATER ID EQ NEW ARRAYLIST LESS type GREATER LPAREN RPAREN SEMICOL
        '''
        # 3 5 10
        p[0] = ast.DeclArrayList(p[1],p[3],p[5],p[10])
        pass
    
    def p_while_statement(self, p):
        '''
        while_stmt : WHILE LPAREN expr RPAREN scope
        '''
        p[0] = ast.DeclWhileStmt(p[3], p[5])
    
    def p_for_statement(self, p):
        '''
        for_stmt : FOR LPAREN type ID EQ expr SEMICOL expr SEMICOL assign_stmt RPAREN scope
        '''
        var_assign = ast.DeclVarStmt(ast.DeclAccessType('public'), p[3], p[4], p[6])
        p[0] = ast.DeclForStmt(var_assign, p[8], p[10], p[12])

    def p_try_statement(self, p):
        """
        try_stmt : TRY scope CATCH LPAREN EXCEPTION ID RPAREN scope FINALLY scope
                 | TRY scope CATCH LPAREN EXCEPTION ID RPAREN scope
        """
        if len(p) > 9:
            # finally is included
            p[0] = ast.DeclTryStmt(p[2], p[6], p[8], p[10])
        else:
            p[0] = ast.DeclTryStmt(p[2], p[6], p[8])
    
    def p_return_statement(self, p):
        '''
        ret_stmt : RETURN expr SEMICOL
        '''
        p[0] = ast.DeclRetStmt(p[2])
    
    ################################
    ## Expressions
    ################################
    def p_expr_object_instance(self, p):
        '''
        expr : NEW ID LPAREN RPAREN
        '''
        p[0] = ast.ObjInstance(p[2])
    
    def p_expr_binops(self, p):
        '''
        expr : expr PLUS expr
             | expr MINUS expr
             | expr TIMES expr
             | expr DIVIDE expr
        '''
        p[0] = ast.BinOp(p[2], p[1], p[3])
    
    def p_expr_compareops(self, p):
        """
        expr : expr DOUBLEEQ expr
             | expr LESS expr
             | expr LESSEQ expr
             | expr GREATER expr
             | expr GREATEREQ expr
             | expr NEQ expr
        """
        p[0] = ast.CompareOp(p[2], p[1], p[3])
    
    def p_expr_logicops(self, p):
        """
        expr : expr AND expr
             | expr OR expr
        """
        p[0] = ast.LogicOp(p[2], p[1], p[3])
    
    def p_expr_unary(self, p):
        '''
        expr : MINUS expr %prec UNARY
             | BANG expr %prec UNARY
        '''
        p[0] = ast.UnaryOp(p[1], p[2])
    
    def p_expr_group(self, p):
        '''
        expr : LPAREN expr RPAREN
        '''
        p[0] = p[2]

    def p_expr_number(self, p):
        '''
        expr : NUMBER PERIOD NUMBER
             | NUMBER
        '''
        if len(p) == 2:
            p[0] = ast.Constant('int', p[1])
        else:
            num = str(p[1]) + str(p[2]) + str(p[3])
            p[0] = ast.Constant('float', float(num))

    def p_expr_str(self, p):
        '''
        expr : STR
        '''
        p[0] = ast.Constant('String', p[1])
    
    def p_expr_bool(self, p):
        '''
        expr : TRUE
             | FALSE
        '''
        p[0] = ast.Constant('boolean', p[1])
    
    def p_expr_null(self, p):
        '''
        expr : NULL
        '''
        p[0] = ast.Constant('null', p[1])

    def p_expr_id(self, p):
        '''
        expr : ID
        '''
        p[0] = ast.Constant('id', p[1])

    # def p_expr_this(self, p):
    #     '''
    #     expr : THIS
    #     '''
    #     p[0] = ast.Constant('this', p[1])

    ################################
    ## Types
    ################################

    def p_type(self, p):
        '''
        type : base_type
        '''
        p[0] = ast.DeclType(p[1])

    def p_base_type(self, p):
        '''
        base_type : INT
                  | BOOLEAN
                  | STRING
                  | VOID
                  | FLOAT
        '''
        p[0] = p[1]
    
    ################################
    ## Misc
    ################################

    # This can be used to handle the empty production, by using 'empty'
    # as a symbol. For example:
    #
    #       optitem : item
    #               | empty
    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        print("Syntax error at token", p)

    def p_hash_map(self,p):
        '''
        hash_map : HASHMAP LESS type COMMA type GREATER ID EQ NEW HASHMAP LESS type COMMA type GREATER LPAREN RPAREN SEMICOL
        '''
        # 3 5 10
        p[0] = ast.DeclHashMap(p[1],p[3],p[5],p[7],p[10],p[12],p[14])
        pass