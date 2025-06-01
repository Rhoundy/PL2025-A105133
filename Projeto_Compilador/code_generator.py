from ast_nodes import Node, IDNode, ArrayAccessNode, FunctionDeclarationNode, FunctionCallNode, VarDeclNode

class CodeGenerator:
    def __init__(self, semantic_analyzer_instance):
        self.semantic_analyzer = semantic_analyzer_instance
        self.vm_code = []
        self.label_counter = 0
        self.active_scope_for_lookups = None

    def new_label(self, prefix="L"):
        label = f"{prefix}{self.label_counter}"; self.label_counter += 1; return label

    def emit(self, instruction):
        self.vm_code.append(instruction)

    def generate_code(self, ast):
        self.vm_code = []; self.label_counter = 0
        self.active_scope_for_lookups = self.semantic_analyzer.current_scope

        self.emit("start")
        try:
            self.visit(ast) 
        except Exception as e:
            error_msg = f"ERRO CRÍTICO CG: {e}"
            if hasattr(self.semantic_analyzer, 'errors'): self.semantic_analyzer.errors.append(error_msg)
            print(error_msg); import traceback; traceback.print_exc(); return "" 

        if not self.vm_code: print("AVISO CG: Nenhuma instrução VM gerada.")
        return "\n".join(self.vm_code)

    def visit(self, node):
        if node is None: return None
        method_name = 'visit_' + type(node).__name__
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node):
        for child_attr_name in dir(node):
            if child_attr_name.startswith('_'): continue
            child = getattr(node, child_attr_name)
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, Node): self.visit(item)
            elif isinstance(child, Node): self.visit(child)
        return None

    def visit_ProgramNode(self, node):

        self.visit(node.block)
        self.emit("stop") 

    def visit_BlockNode(self, node):
        if node.declarations: self.visit(node.declarations)
        if node.compound_statement: self.visit(node.compound_statement)

    def visit_DeclarationsNode(self, node):
        if node and node.items:
            for item_list_or_node in node.items:
                items_to_process = item_list_or_node if isinstance(item_list_or_node, list) else [item_list_or_node]
                for item in items_to_process:
                    if isinstance(item, FunctionDeclarationNode):
                         self.visit(item)

    def visit_VarDeclNode(self, node): pass

    def visit_CompoundStatementNode(self, node):
        if node and node.statements:
            for statement in node.statements: self.visit(statement)

    def _get_symbol_from_active_scope(self, name_upper):
        return self.active_scope_for_lookups.lookup(name_upper)

    def visit_AssignmentNode(self, node):
        lhs_var_node = node.var

        if isinstance(lhs_var_node, IDNode) and \
           self.active_scope_for_lookups.scope_name != "global" and \
           lhs_var_node.name.upper() == self.active_scope_for_lookups.scope_name: 

            parent_scope = self.active_scope_for_lookups.parent
            if parent_scope: 
                function_symbol_in_parent = parent_scope.lookup(lhs_var_node.name.upper())
                if function_symbol_in_parent and function_symbol_in_parent['kind'] == 'function':
                    self.visit(node.expr) 

                    return 

        elif     isinstance(lhs_var_node, ArrayAccessNode):
            array_name_upper = lhs_var_node.id.name.upper()
            array_symbol = self._get_symbol_from_active_scope(array_name_upper)
            if not (array_symbol and 'address' in array_symbol and \
                    isinstance(array_symbol.get('full_type_spec'), dict) and \
                    array_symbol['full_type_spec'].get('type') == 'ARRAY'):
                self.semantic_analyzer.errors.append(f"Erro CG: Array '{lhs_var_node.id.name}' inv. p/ atrib. linha {node.lineno}.")
                return

            if array_symbol.get('is_global'): 
                self.emit(f"PUSHI {array_symbol['address']}") 
            else: 
                self.emit("PUSHFP") 
                self.emit(f"PUSHI {array_symbol['address']}") 
                self.emit("ADD") 

            self.visit(lhs_var_node.index_expr) 
            low_bound = array_symbol['full_type_spec'].get('low', 0)
            if low_bound != 0: self.emit(f"PUSHI {low_bound}"); self.emit("SUB") 
            self.emit("PADD") 

            self.visit(node.expr)

            self.emit("STORE 0") 

        elif isinstance(lhs_var_node, IDNode):
            self.visit(node.expr) 
            var_name_upper = lhs_var_node.name.upper()
            symbol = self._get_symbol_from_active_scope(var_name_upper)
            if not (symbol and symbol['kind'] in ['variable', 'parameter'] and 'address' in symbol):
                self.semantic_analyzer.errors.append(f"Erro CG: Var/Param '{lhs_var_node.name}' inv. p/ atrib. linha {node.lineno}.")
                return
            if symbol.get('is_global'): self.emit(f"STOREG {symbol['address']}")
            else: self.emit(f"STOREL {symbol['address']}")
        else:
            self.semantic_analyzer.errors.append(f"Erro CG: LHS inválido p/ atrib. linha {node.lineno}.")

    def visit_IDNode(self, node): 
        node_name_upper = node.name.upper()
        if node_name_upper == 'TRUE': self.emit("PUSHI 1"); return
        if node_name_upper == 'FALSE': self.emit("PUSHI 0"); return
        symbol = self._get_symbol_from_active_scope(node_name_upper)
        if not symbol: self.semantic_analyzer.errors.append(f"Erro CG: ID '{node.name}' não enc. linha {node.lineno}."); return
        if symbol['kind'] in ['variable', 'parameter']:
            if 'address' not in symbol: self.semantic_analyzer.errors.append(f"Erro CG: '{node.name}' s/addr linha {node.lineno}."); return
            if symbol.get('is_global'): self.emit(f"PUSHG {symbol['address']}")
            else: self.emit(f"PUSHL {symbol['address']}")
        elif symbol['kind'] == 'function' and self.active_scope_for_lookups.scope_name == node_name_upper :

            pass

    def visit_ArrayAccessNode(self, node): 
        array_id_node = node.id; array_name_upper = array_id_node.name.upper()
        array_symbol = self._get_symbol_from_active_scope(array_name_upper)
        if not (array_symbol and 'address' in array_symbol and \
                isinstance(array_symbol.get('full_type_spec'), dict) and \
                array_symbol['full_type_spec'].get('type') == 'ARRAY'):
            self.semantic_analyzer.errors.append(f"Erro CG: Array '{array_id_node.name}' inv. (leitura) linha {node.lineno}.")
            return

        if array_symbol.get('is_global'): 
            self.emit(f"PUSHI {array_symbol['address']}") 
        else: 
            self.emit("PUSHFP") 
            self.emit(f"PUSHI {array_symbol['address']}") 
            self.emit("ADD") 

        self.visit(node.index_expr)
        low_bound = array_symbol['full_type_spec'].get('low', 0)
        if low_bound != 0: self.emit(f"PUSHI {low_bound}"); self.emit("SUB")
        self.emit("PADD")
        self.emit("LOAD 0")

    def visit_NumberNode(self, node):
        if isinstance(node.value, int): self.emit(f"PUSHI {node.value}")
        elif isinstance(node.value, float): self.emit(f"PUSHF {node.value}")

    def visit_StringLiteralNode(self, node):
        processed_value = node.value.replace('"', '\\"')
        self.emit(f'PUSHS "{processed_value}"')

    def visit_BinOpNode(self, node):
        self.visit(node.left); self.visit(node.right)
        op_map = {'PLUS': 'ADD', 'MINUS': 'SUB', 'TIMES': 'MUL', 'DIVIDE': 'FDIV', 'DIV_OP': 'DIV', 
                  'MOD_OP': 'MOD', 'EQ': 'EQUAL', 'LT': 'INF', 'LE': 'INFEQ', 'GT': 'SUP', 
                  'GE': 'SUPEQ', 'AND_OP': 'AND', 'OR_OP': 'OR'}
        if node.op == 'NEQ': self.emit("EQUAL"); self.emit("NOT")
        elif node.op in op_map: self.emit(op_map[node.op])
        else: self.semantic_analyzer.errors.append(f"Erro CG: BinOp '{node.op}' não mapeado linha {node.lineno}.")

    def visit_UnaryOpNode(self, node):
        self.visit(node.operand)
        if node.op == 'MINUS': self.emit("PUSHI 0"); self.emit("SWAP"); self.emit("SUB")
        elif node.op == 'NOT_OP': self.emit("NOT")
        else: self.semantic_analyzer.errors.append(f"Erro CG: UnaryOp '{node.op}' não mapeado linha {node.lineno}.")

    def visit_WhileStatementNode(self, node):
        cond_label = self.new_label("WCOND"); end_label = self.new_label("WEND")
        self.emit(f"{cond_label}:"); self.visit(node.condition)
        self.emit(f"JZ {end_label}")
        self.visit(node.do_statement)
        self.emit(f"JUMP {cond_label}")
        self.emit(f"{end_label}:")

    def visit_IfStatementNode(self, node):
        else_label = self.new_label("ELSE"); end_if_label = self.new_label("ENDIF")
        self.visit(node.condition); self.emit(f"JZ {else_label}")
        self.visit(node.then_statement)
        if node.else_statement: self.emit(f"JUMP {end_if_label}")
        self.emit(f"{else_label}:")
        if node.else_statement: self.visit(node.else_statement)
        self.emit(f"{end_if_label}:")

    def visit_ForStatementNode(self, node):
        self.visit(node.initial_assignment)
        body_label = self.new_label("FORBODY"); condition_label = self.new_label("FORCOND"); end_loop_label = self.new_label("ENDFOR")
        self.emit(f"JUMP {condition_label}")
        self.emit(f"{body_label}:"); self.visit(node.do_statement)
        control_var_node = node.initial_assignment.var; var_name_upper = control_var_node.name.upper()
        symbol = self._get_symbol_from_active_scope(var_name_upper)
        if not (symbol and 'address' in symbol): self.semantic_analyzer.errors.append(f"Erro CG: Var FOR '{var_name_upper}' s/addr."); return
        push_op = "PUSHG" if symbol.get('is_global') else "PUSHL"; store_op = "STOREG" if symbol.get('is_global') else "STOREL"
        self.emit(f"{push_op} {symbol['address']}"); self.emit("PUSHI 1")
        self.emit("ADD" if node.direction.upper() == 'TO' else "SUB")
        self.emit(f"{store_op} {symbol['address']}")
        self.emit(f"{condition_label}:")
        self.emit(f"{push_op} {symbol['address']}")
        self.visit(node.limit_expr)
        self.emit("INFEQ" if node.direction.upper() == 'TO' else "SUPEQ")
        self.emit(f"JZ {end_loop_label}") 
        self.emit(f"JUMP {body_label}") 
        self.emit(f"{end_loop_label}:")

    def visit_ReadLnCallNode(self, node):

        simulated_id_node = IDNode('READLN', node.lineno)

        simulated_fcall_node = FunctionCallNode(simulated_id_node, node.args)
        simulated_fcall_node.lineno = node.lineno 
        self.visit(simulated_fcall_node) 

    def visit_WriteLnCallNode(self, node):

        simulated_id_node = IDNode('WRITELN', node.lineno)

        simulated_fcall_node = FunctionCallNode(simulated_id_node, node.args)
        simulated_fcall_node.lineno = node.lineno 
        self.visit(simulated_fcall_node)

    def visit_FunctionDeclarationNode(self, node): 
        function_name_upper = node.id.name.upper()
        self.emit(f"{function_name_upper}:") 
        function_scope_table = self.semantic_analyzer.function_scopes.get(function_name_upper)
        if not function_scope_table: self.semantic_analyzer.errors.append(f"Erro CG: Escopo '{function_name_upper}' não enc."); return

        local_var_space = function_scope_table.total_local_var_size
        if local_var_space > 0:
            self.emit(f"PUSHN {local_var_space}")

        original_active_scope = self.active_scope_for_lookups
        self.active_scope_for_lookups = function_scope_table
        if node.block: self.visit(node.block)
        self.active_scope_for_lookups = original_active_scope

        self.emit("RETURN")

    def visit_FunctionCallNode(self, node):
        func_name_upper = node.id.name.upper()

        function_symbol = self.semantic_analyzer.current_scope.lookup(func_name_upper) 

        if not (function_symbol and function_symbol['kind'] in ['function', 'procedure']):
            self.semantic_analyzer.errors.append(f"Erro CG: Chamada func/proc '{node.id.name}' não def linha {node.lineno}.")
            return

        if function_symbol.get('built_in'):

            params_def = function_symbol.get('params_definition', {})
            if func_name_upper == 'LENGTH':
                if len(node.args) == 1: self.visit(node.args[0]); self.emit("STRLEN")
                else: self.semantic_analyzer.errors.append(f"Erro CG: Chamada LENGTH {len(node.args)} args.")
                return
            elif func_name_upper == 'WRITE' or func_name_upper == 'WRITELN':
                for arg_expr in node.args:
                    self.visit(arg_expr)
                    inferred_type = getattr(arg_expr, 'inferred_type', 'UNKNOWN_TYPE')
                    if inferred_type == 'INTEGER': self.emit("WRITEI")
                    elif inferred_type == 'REAL': self.emit("WRITEF")
                    elif inferred_type == 'STRING': self.emit("WRITES")
                    elif inferred_type == 'BOOLEAN': self.emit("WRITEI") 
                    else: self.emit("WRITEI") 
                if func_name_upper == 'WRITELN': self.emit("WRITELN")
                return
            elif func_name_upper == 'READLN' or func_name_upper == 'READ':
                for arg_node in node.args:
                    var_name_upper = ""; is_array_access = isinstance(arg_node, ArrayAccessNode)
                    symbol_to_access = None
                    if isinstance(arg_node, IDNode): var_name_upper = arg_node.name.upper()
                    elif is_array_access: var_name_upper = arg_node.id.name.upper()
                    else: continue
                    symbol_to_access = self._get_symbol_from_active_scope(var_name_upper) 
                    if not (symbol_to_access and 'address' in symbol_to_access): continue

                    if is_array_access:
                        if symbol_to_access.get('is_global'): self.emit(f"PUSHG {symbol_to_access['address']}")
                        else: self.emit(f"PUSHL {symbol_to_access['address']}")
                        self.visit(arg_node.index_expr)
                        low_bound = symbol_to_access['full_type_spec'].get('low', 0)
                        if low_bound != 0: self.emit(f"PUSHI {low_bound}"); self.emit("SUB")
                        self.emit("PADD")

                    self.emit("READ")
                    inferred_type = getattr(arg_node, 'inferred_type', 'UNKNOWN_TYPE')
                    if is_array_access: inferred_type = symbol_to_access['full_type_spec']['of_type']
                    if inferred_type == 'INTEGER': self.emit("ATOI")
                    elif inferred_type == 'REAL': self.emit("ATOF")

                    if is_array_access: self.emit("STORE 0")
                    else:
                        if symbol_to_access.get('is_global'): self.emit(f"STOREG {symbol_to_access['address']}")
                        else: self.emit(f"STOREL {symbol_to_access['address']}")
                if func_name_upper == 'READLN' and hasattr(self.semantic_analyzer, 'vm_consumes_newline_for_readln') and self.semantic_analyzer.vm_consumes_newline_for_readln:
                    pass 

                return

        arg_total_slots = 0 

        if hasattr(function_symbol, 'params') and isinstance(function_symbol['params'], list):
            for i, arg_expr in enumerate(node.args): 
                self.visit(arg_expr)

                arg_total_slots += function_symbol['params'][i].get('size_on_stack', 1) if i < len(function_symbol['params']) else 1

        self.emit(f"PUSHA {func_name_upper}") 
        self.emit("CALL")                     

        if arg_total_slots > 0:
            self.emit(f"POP {arg_total_slots}") 

    def visit_empty(self, node): pass