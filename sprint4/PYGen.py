#!/usr/bin/env python3

from tracemalloc import start


class PYGen(object):
    def __init__(self, file_name):
        """
        PY_lst: list of classes, which are in the format of dictionary 
        """
        self.PY_lst = []
        self.class_name = []
        self.has_main = {}
        self.file_name = file_name
        self.construct = False
        self.arraylists = {}

        self.class_count = 0
        self.callable = {}
    
    def generate(self, node, last_indent, print_not=True):
        """
        Similar to 'typecheck' method from TypeChecker object
        """
        method = 'gen_' + node.__class__.__name__
        return getattr(self, method)(node, last_indent, print_not)
    
    def inc_class_count(self):
        self.class_count += 1
    
    def add_code(self, code):
        """
        Add 'code' to the PY_lst with correct spacing
        """
        self.PY_lst.append(code)
    
    def generate_code(self, code, indent):
        return "    "*indent + code
    
    def print_py(self):
        """
        Loop through the generated Python code and print them out to stdout
        """
        file_n = self.file_name[:-5]
        if file_n in self.has_main:
            if self.has_main[file_n]:
                self.add_code('if __name__=="__main__":')
                self.add_code(self.generate_code('{}.main({})'.format(file_n, []), 1))
        for c_dict in self.PY_lst:
            if isinstance(c_dict, dict):
                self.print_dict(c_dict)
            else:
                print(c_dict)
    
    def check_empty(self, body_dict):
        for key, val in body_dict.items():
            if isinstance(val, str):
                if "=" in val:
                    v = val.split("=")[0].strip()
                    if v in self.callable:
                        if self.callable[v] > 0:
                            return False
                else:
                    return False
            else:
                if isinstance(val, dict):
                    for k, v in val.items():
                        if k[:7] != 'comment':
                            return False
        return True

    def print_dict(self, pending_dict):
        for key, val in pending_dict.items():
            if isinstance(val, dict):
                if key == 'if_body' or key == 'elif_body' or key == 'else_body':
                    bdy_empty = self.check_empty(val)
                    if bdy_empty:
                        for k, v2 in val.items():
                            if isinstance(v2, str):
                                wsnum = v2.count(" ") // 4
                                break
                        print(" "*(wsnum*4) + 'pass')
                    else:
                        self.print_dict(val)
                else:
                    self.print_dict(val)
            elif val is None:
                pass
            else:
                if key == 'for_stmt':
                    bdy_empty = self.check_empty(pending_dict['for_body'])
                    if not bdy_empty:
                        print(val)
                else:
                    v = val.split("=")[0].strip()
                    if v in self.callable:
                        if self.callable[v] > 0:
                            if v in self.arraylists:
                                wsnum = val.count(" ") // 4
                                print(" "*(wsnum*4) + "{} = {}".format(v, self.arraylists[v]))
                            else:
                                print(val)
                    else:
                        print(val)

    def read_dict(self, pending_dict, f):
        for key, val in pending_dict.items():
            if isinstance(val, dict):
                if key == 'if_body' or key == 'elif_body' or key == 'else_body':
                    bdy_empty = self.check_empty(val)
                    if bdy_empty:
                        for k, v2 in val.items():
                            if isinstance(v2, str):
                                wsnum = v2.count(" ") // 4
                                break
                        f.write(" "*(wsnum*4) + 'pass' + '\n')
                    else:
                        self.read_dict(val,f)
                else:
                    self.read_dict(val,f)
            elif val is None:
                pass
            else:
                if key == 'for_stmt' or key == 'var_init':
                    bdy_empty = self.check_empty(pending_dict['for_body'])
                    if not bdy_empty:
                        f.write(val+'\n')
                else:
                    v = val.split("=")[0].strip()
                    if v in self.callable:
                        if self.callable[v] > 0:
                            if v in self.arraylists:
                                wsnum = val.count(" ") // 4
                                f.write(" "*(wsnum*4) + "{} = {}".format(v, self.arraylists[v]) + '\n')
                            else:
                                f.write(val+'\n')
                    else:
                        f.write(val+'\n')
        
    def generate_py(self):
        """
        Generate Python file
        """
        file_n = self.file_name[:-5]
        if file_n in self.has_main:
            if self.has_main[file_n]:
                self.add_code('if __name__=="__main__":')
                self.add_code(self.generate_code('{}.main({})'.format(file_n, []), 1))
        f = open("{}.py".format(file_n), 'w')
        for c_dict in self.PY_lst:
            if isinstance(c_dict, dict):
                self.read_dict(c_dict, f)
            else:
                f.write(c_dict+"\n")
        f.close()
    
    def gen_AssignStmt(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        expr = self.generate(node.expr, indent)
        if expr == 'true' or expr == 'false':
            expr = expr.capitalize()
        if not node.this:
            lbl = "{} = {}".format(node.name, expr)
        else:
            lbl = "self.{} = {}".format(node.name, expr)
        if node.name in self.callable:
            self.callable[node.name] += 1
        return self.generate_code(lbl, indent)
        
    
    def gen_BinOp(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        # Left operand
        left = self.generate(node.left, indent)
        # Right operand
        right = self.generate(node.right, indent)

        return "{} {} {}".format(left, node.op, right)
    
    def gen_CompareOp(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        # Left operand
        left = self.generate(node.left, indent)
        # Right operand
        right = self.generate(node.right, indent)

        return "{} {} {}".format(left, node.op, right)

    def gen_Constant(self, node, last_indent, print_not=True):
        if node.value in self.callable:
            self.callable[node.value] += 1
        return node.value
    
    def gen_DeclStmt(self, node, last_indent, print_not=True):
        expr = self.generate(node.expr, 0)
        return self.generate_code("{} = {}".format(node.name, expr), 0)

    def gen_DeclArrayList(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        if node.name not in self.callable:
            self.callable[node.name] = 0
        else:
            self.callable[node.name] += 1
        if node.name not in self.arraylists:
            self.arraylists[node.name] = []
        return self.generate_code("{} = []".format(node.name), indent)

    
    def gen_DeclFuncCall(self, node, last_indent, print_not=True):
        """
        self.access_type = access_type
        self.var_type = var_type
        self.name = name
        self.func_name = func_name
        self.func_param = expr
        self.coord = coord
        """

        # Push all of the arguments with "PushParam" function
        indent = last_indent + 1
        if len(node.children()) == 3:
            args = node.children()[2][1]
        else:
            args = node.children()[1][1]
        # if node.name in self.callable:
        #     self.callable[node.name] += 1
        lbl = ""
        if len(node.children()) == 3 and node.access_type.name and node.access_type.name.upper() == "PRIVATE":
            lbl = lbl + "_{}".format(node.name)
        else:
            lbl = lbl + "{}".format(node.name)
        lbl += " = {}(".format(node.func_name)
        i = 0
        if args.func_params is not None:
            while i < len(args.func_params):
                param = args.func_params[i]
                expr = self.generate(param, indent)
                lbl += "{}".format(expr)
                if i + 1 >= len(args.func_params):
                    pass
                else:
                    lbl += ", "
                i += 1
        lbl += ")"
        return self.generate_code(lbl, indent)
    
    def gen_DeclIfStmt(self, node, last_indent, print_not=True):
        cond = self.generate(node.if_cond, last_indent)
        indent = last_indent + 1
        if_dict = {}
        if not node.elif_cond:
            # Skip to the false_body if the condition is not met
            if_dict['if_cond'] = self.generate_code("if ({}):".format(cond), indent)
            if_dict['if_body'] = self.generate(node.if_body, indent)
            # Make sure the statements from false_body is skipped

            if_dict['else_cond'] = self.generate_code("else:", indent)
            if_dict['else_body'] = self.generate(node.else_body, indent)
        else:
            elifcond = self.generate(node.elif_cond, 0)
            # not if go to elseif
            if_dict['if_cond'] = self.generate_code("if ({}):".format(cond), indent)
            if_dict['if_body'] = self.generate(node.if_body, indent)
             # Make sure the statements from false_body is skipped

            # process elif situation            
            if_dict['elif_cond'] = self.generate_code("elif ({}):".format(elifcond), indent)
            if_dict['elif_body'] = self.generate(node.elif_body, indent)

            #else situation
            if_dict['else_cond'] = self.generate_code("else:", indent)
            if_dict['else_body'] = self.generate(node.else_body, indent)
            #end if statement
        return if_dict

    def gen_DeclWhileStmt(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        cond = self.generate(node.cond, 0)
        while_dict = {}
        # Skip to the false_body if the condition is not met
        while_dict['while_cond'] = self.generate_code("while ({}):".format(cond), indent)
        while_dict['while_body'] = self.generate(node.body, indent)
        # Make sure the statements from false_body is skipped
        return while_dict
    
    def gen_DeclHashMap(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        if node.name not in self.callable:
            self.callable[node.name] = 0
        else:
            self.callable[node.name] += 1
        return self.generate_code(f"{node.name} = {{}}", indent)

    def gen_DeclTryStmt(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        # Allocate room for function local variables
        try_dict = {}
        if not node.finally_stmt_list:
            try_dict['try_cond'] = self.generate_code("try:", indent)
            try_dict['try_body'] = self.generate(node.try_stmt_list, indent)
            exception_id = self.generate(node.catch_id, indent)
            try_dict['catch_cond'] = self.generate_code("except {}:".format(exception_id), indent)
            try_dict['catch_body'] = self.generate(node.catch_stmt_list, indent)
        else:
            try_dict['try_cond'] = self.generate_code("try:", indent)
            try_dict['try_body'] = self.generate(node.try_stmt_list, indent)

            exception_id = self.generate(node.catch_id, indent)
            try_dict['catch_cond'] = self.generate_code("except {}:".format(exception_id), indent)
            try_dict['catch_body'] = self.generate(node.catch_stmt_list, indent)
            try_dict['final_cond'] = self.generate_code("finally:", indent)
            try_dict['final_body'] = self.generate(node.finally_stmt_list, indent)
        return try_dict

    def gen_DeclMethodStmt(self, node, last_indent, print_not=True):
        """
        @params
        access_type : 'public'|'private' | None
        method_type : method return type
        name: method name
        params: parameters
        body: body statements, including return statement
        coord: error index

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
        """
        indent = last_indent + 1
        method_dict = {}
        # Function label
        lbl = "def"
        # if node.name not in self.callable:
        #     self.callable[node.name] = 0
        # else:
        #     self.callable[node.name] += 1
        if not node.main:
            if node.name == self.class_name[-1]:
                self.construct = True
                lbl += " __init__"
            else:
                if node.access_type.name and node.access_type.name.upper() == "PRIVATE":
                    lbl = lbl + " _"
                else:
                    lbl = lbl + " "
                lbl += "{}".format(node.name)
        else:
            self.has_main[self.class_name[-1]] = True
            lbl += " {}".format(node.name)
        lbl = lbl + "("
        if not node.main:
            pl_ind = 0
            while pl_ind < len(node.params):
                paramList = node.params[pl_ind]
                p_ind = 0
                if self.construct:
                    lbl += "self"
                if paramList.params is not None:
                    if self.construct:
                        lbl += ", "
                    while p_ind < len(paramList.params):
                        param = paramList.params[p_ind]
                        lbl = lbl + "{}: {}".format(param.name, param.type.name)
                        if pl_ind + 1 >= len(node.params) and p_ind + 1 >= len(paramList.params):
                            pass
                        else:
                            lbl = lbl + ", "
                        p_ind += 1
                pl_ind += 1
        else:
            lbl += 'args'
        lbl = lbl + ")"
        if node.method_type:
            if node.method_type.name == 'void':
                lbl = lbl + " -> {}".format('None')
            else:
                lbl = lbl + " -> {}".format(node.method_type.name)
        lbl = lbl + ":"
        method_dict['method_stmt'] = self.generate_code(lbl, indent)

        # Allocate room for function local variables

        # Actually generate the main body

        method_dict['method_body'] = self.generate(node.body, indent)
        method_dict['return_stmt'] = self.generate(node.ret_stmt, indent)

        # Do any cleanup before jumping back
        return method_dict

    def gen_Program(self, node, last_indent, print_not=True):
        for (child_name, child) in node.children():
            for c in child:
                if c is not None:
                    if isinstance(c, list):
                        for c2 in c:
                            self.add_code(self.generate(c2, last_indent))
                    else:
                        self.inc_class_count()
                        self.add_code(self.generate(c, last_indent))

    def gen_DeclRetStmt(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        if node.expr:
            expr = self.generate(node.expr, indent)
            if expr in self.callable:
                self.callable[expr] += 1
            return self.generate_code("return {}".format(expr), indent)

    def gen_StmtList(self, node, last_indent, print_not=True):
        stmt_dict = {}
        stmt_body_count = 0
        while_appeared = {}
        for stmt in node.stmt_lst:
            if stmt is not None:
                if not isinstance(stmt, list):
                    stmt_body_count += 1
                    res = self.generate(stmt, last_indent)
                    if isinstance(res, dict):
                        lst = list(while_appeared.keys())
                        lst_ind = []
                        count = 0
                        for l in lst:
                            if 'while_cond' in res:
                                if res['while_cond'] in l:
                                    count += 1
                                    lst_ind.append(l)
                        if 'while_cond' in res:
                            if count == 0:
                                stmt_dict['body{}'.format(stmt_body_count)] = res
                                while_appeared[res['while_cond']+"{}".format(count)] = [res, 'body{}'.format(stmt_body_count)]
                            else:
                                for i in lst_ind:
                                    old_while_body = while_appeared[i][0]['while_body']
                                    new_while_body = res['while_body']
                                    if self.check_step(new_while_body, old_while_body, res['while_cond']):
                                        appeared = while_appeared[i]
                                        old_res = appeared[0]
                                        old_pos = appeared[1]
                                        new_res = old_res
                                        stmts = res['while_body']
                                        for ind in list(old_res['while_body'].keys()):
                                                if 'body' in ind:
                                                    stmt_count = int(ind[4:])
                                        for key, var in stmts.items():
                                            if var not in new_res['while_body'].values():
                                                stmt_count += 1
                                                new_res['while_body']['body{}'.format(stmt_count)] = var
                                        del stmt_dict[old_pos]
                                        stmt_dict['body{}'.format(stmt_body_count)] = new_res
                                        while_appeared[i][0] = new_res
                                        break
                                    else:
                                        stmt_dict['body{}'.format(stmt_body_count)] = res
                                        while_appeared[res['while_cond']+"{}".format(count)] = [res, 'body{}'.format(stmt_body_count)]
                        else:
                            stmt_dict['body{}'.format(stmt_body_count)] = res
                    else:           
                        stmt_dict['body{}'.format(stmt_body_count)] = res
                else:
                    for s in stmt:
                        stmt_body_count += 1
                        stmt_dict['body{}'.format(stmt_body_count)] = self.generate(s, last_indent+1)
        return stmt_dict
    
    def check_step(self, new_body, old_body, condition):
        start_ind = condition.index('(')
        end_ind = condition.index(')')
        cond = condition[start_ind+1: end_ind]
        symbol_lst = ['==', '<', '<=', '>', '>=', "!="]
        symbol_ind = -1
        for symbol in symbol_lst:
            if symbol in cond:
                symbol_ind = cond.index(symbol)
        v = cond[:symbol_ind].replace(" ", "")
        new_body_values = list(new_body.values())
        old_body_values = list(old_body.values())
        old_step = ""
        for ov in old_body_values:
            if v in ov:
                old_step = ov.replace(" ","")
                break
        for nv in new_body_values:
            if isinstance(nv, str):
                rmvd = nv.replace(" ","")
                if rmvd == old_step:
                    return True
            else:
                if self.check_step(nv, old_body, condition):
                    return True
        return False

    def generate_comments(self, comments, indent):
        comments_dict = {}
        comment_count = 0
        if comments:
            for comment in comments:
                        comments = "#"
                        for w in comment.words:
                            if w is not None:
                                comments += " {}".format(w.value)
                        comment_count += 1
                        comments_dict['comments{}'.format(comment_count)] = self.generate_code(comments, indent)
        return comments_dict
    
    def gen_DeclObjPutCall(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        args = node.children()[0]
        if node.name in self.callable:
            self.callable[node.name] += 1
        expr1 = self.generate(node.expr1, indent)
        expr2 = self.generate(node.expr2, indent)
        lbl = "{}[{}] = {}".format(node.name, expr1,expr2)
        return self.generate_code(lbl, indent)

    def gen_DeclObjClearCall(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        #args = node.children()[0]
        if node.name in self.callable:
            self.callable[node.name] += 1
        lbl = "{}.clear()".format(node.name)
        return self.generate_code(lbl, indent)
    def gen_DeclClassStmt(self, node, last_indent, print_not=True):
        """
        parameters: access_type, name, extends, stmt_list, coord=None
        self.name = name
        self.access_type = access_type
        self.extend = extends
        self.stmt_list = stmt_list
        self.coord = coord
        """
        body_count = 0
        lbl = "class"
        while_appeared = {}
        if node.access_type.name and node.access_type.name.upper() == "PRIVATE":
            lbl = lbl + " _{}".format(node.name)
        else:
            lbl = lbl + " {}".format(node.name)
        self.class_name.append(node.name)
        if node.extend:
            lbl = lbl + "({})".format(node.extend.name)
        lbl += ":"  # lbl = class Mainclass:
        class_dict = {}
        class_dict[node.name] = self.generate_code(lbl, last_indent)
        if node.stmt_list:
            for stm in node.stmt_list:
                if stm is not None:
                    if isinstance(stm, list): #comments
                        for s in stm:
                            body_count += 1
                            class_dict['body{}'.format(body_count)] = self.generate(s, last_indent+1)
                    else:
                        body_count += 1
                        # print(type(stm))
                        # class_dict['body{}'.format(body_count)] = self.generate(stm, last_indent)
                        res = self.generate(stm, last_indent)
                        if isinstance(res, dict):
                            lst = list(while_appeared.keys())
                            lst_ind = []
                            count = 0
                            for l in lst:
                                if 'while_cond' in res:
                                    if res['while_cond'] in l:
                                        count += 1
                                        lst_ind.append(l)
                            if 'while_cond' in res:
                                if count == 0:
                                    class_dict['body{}'.format(body_count)] = res
                                    while_appeared[res['while_cond']+"{}".format(count)] = [res, 'body{}'.format(body_count)]
                                else:
                                    for i in lst_ind:
                                        old_while_body = while_appeared[i][0]['while_body']
                                        new_while_body = res['while_body']
                                        if self.check_step(new_while_body, old_while_body, res['while_cond']):
                                            appeared = while_appeared[i]
                                            old_res = appeared[0]
                                            old_pos = appeared[1]
                                            new_res = old_res
                                            stmts = res['while_body']
                                            for ind in list(old_res['while_body'].keys()):
                                                if 'body' in ind:
                                                    stmt_count = int(ind[4:])
                                            for key, var in stmts.items():
                                                if var not in new_res['while_body'].values():
                                                    stmt_count += 1
                                                    new_res['while_body']['body{}'.format(stmt_count)] = var
                                            del class_dict[old_pos]
                                            class_dict['body{}'.format(body_count)] = new_res
                                            while_appeared[i] = [new_res, 'body{}'.format(body_count)]
                                            break
                                        else:
                                            class_dict['body{}'.format(body_count)] = res
                                            while_appeared[res['while_cond']+"{}".format(count)] = [res, 'body{}'.format(body_count)]
                            else:
                                class_dict['body{}'.format(body_count)] = res
                        else:           
                            class_dict['body{}'.format(body_count)] = res
        return class_dict
    
    def gen_DeclVarStmt(self, node, last_indent, print_not=True):
        """
        self.access_type = access_type
        self.var_type = var_type
        self.name = name
        self.expr = expr
        self.coord = coord
        """
        indent = last_indent + 1
        lbl = ""
        if node.access_type.name and node.access_type.name.upper() == "PRIVATE":
            lbl += "_"
        lbl += "{}".format(node.name)
        if node.expr is not None:
            expr = self.generate(node.expr, indent)
        else:
            if node.var_type.name == 'String':
                expr = None
            elif node.var_type.name == 'int':
                expr = 0
            elif node.var_type.name == 'float':
                expr = 0.0
            elif node.var_type.name == 'boolean':
                expr = False
        if node.name not in self.callable:
            self.callable[node.name] = 0
        if expr == 'true' or expr == 'false':
            lbl += " = {}".format(expr.capitalize())
        else:
            lbl += " = {}".format(expr)
        
        return self.generate_code(lbl, indent)

    def gen_FuncCallParamList(self, node, last_indent, print_not=True):
        result = 0
        if node.func_params:
            for param in node.func_params:
                expr = self.generate(param, 0)
                result += expr
        return result
    
    def gen_FuncCallParam(self, node, last_indent, print_not=True):
        if node.expr:
            expr = self.generate(node.expr, 0)
            return expr
    
    def gen_DeclAccessType(self, node, last_indent, print_not=True):
        if node.name is None:
            return ''
        temp = self.generate(node.name, 0)
        return temp

    def gen_DeclType(self, node, last_indent, print_not=True):
        return node.name

    def gen_DeclForStmt(self, node, last_indent, print_not=True):
        """
        self.var_assign = var_assign
        self.cond = cond
        self.body = body
        self.coord = coord
        self.cond_update = update
        """
        indent = last_indent + 1
        for_dict = {}
        var_name = self.generate(node.var_assign, last_indent)
        var_name_splitted = var_name.split(" ")
        for_dict['var_init'] = var_name
        lbl = "for"
        cond = self.generate(node.cond, indent)
        cond_splitted = cond.split(" ")
        update_rule = self.generate(node.cond_update, indent, False)
        update_splitted = update_rule.split(" ")
        if '<' in cond_splitted:
            lbl += " {} in range({}, {}, {}):".format(cond_splitted[0], var_name_splitted[-1], cond_splitted[2], update_splitted[-1])
        if '>' in cond_splitted:
            lbl += " {} in range({}, {}, -{}):".format(cond_splitted[0], var_name_splitted[-1], cond_splitted[2], update_splitted[-1])

        for_dict['for_stmt'] = self.generate_code(lbl, indent)
        for_dict['for_body'] = self.generate(node.body, indent)
        return for_dict
    
    def gen_Comments(self, node, last_indent, print_not=True):
        indent = last_indent
        lbl = "#"
        i = 0
        lbl_dict = {}
        while i < len(node.words):
            word = node.words[i]
            lbl += " {}".format(word[2:])
            i += 1
            lbl_dict['comment{}'.format(i)] = self.generate_code(lbl, indent)
            lbl = '#'
        return lbl_dict
    
    def gen_DeclPrintStmt(self, node, last_indent, print_not=True):
        indent = last_indent+1
        expr = self.generate(node.expr, indent)
        if expr in self.callable:
            self.callable[expr] += 1
        lbl = "print({})".format(expr)
        
        return self.generate_code(lbl, indent)
    
    def gen_Word(self, node, last_indent, print_not=True):
        return

    def gen_DeclObjAddCall(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        args = node.children()[0]
        if node.name in self.callable:
            self.callable[node.name] += 1
        expr = self.generate(node.expr, indent)
        if node.name in self.arraylists:
            if isinstance(expr, str):
                if expr == 'true':
                    self.arraylists[node.name].append(True)
                elif expr == 'false':
                    self.arraylists[node.name].append(False)
                else:
                    self.arraylists[node.name].append(expr.replace('"', ''))
            else:
                self.arraylists[node.name].append(expr)
        return None
    
    def gen_DeclObjRemoveCall(self, node, last_indent, print_not=True):
        indent = last_indent + 1
        args = node.children()[0]
        if node.name in self.callable:
            self.callable[node.name] += 1
        expr = self.generate(node.expr, indent)
        lbl = "del {}[{}]".format(node.name, expr)
        return self.generate_code(lbl, indent)

    def gen_DeclObjCall(self, node, last_indent, print_not=True):
        """
        self.obj_name = obj_name
        self.obj_func = obj_func
        self.func_param = expr
        self.coord = coord
        """
        indent = last_indent + 1
        args = node.children()[0][1]
        lbl = ""
        lbl = lbl + "{}".format(node.obj_name)
        lbl += ".{}(".format(node.obj_func)
        i = 0
        if args.func_params is not None:
            while i < len(args.func_params):
                param = args.func_params[i]
                expr = self.generate(param, indent)
                lbl += "{}".format(expr)
                if i + 1 >= len(args.func_params):
                    pass
                else:
                    lbl += ", "
                i += 1
        lbl += ")"
        return self.generate_code(lbl, indent)