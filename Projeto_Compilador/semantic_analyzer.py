from ast_nodes import *

class SemanticError(Exception):
    """Exceção personalizada para erros semânticos."""
    pass

class SymbolTable:
    def __init__(self, parent=None, scope_name="global"):
        self.symbols = {}
        self.parent = parent
        self.scope_name = scope_name

        self.total_local_var_size = 0 
        self.total_param_size = 0     

        self.next_param_offset = 2  
        self.next_local_offset = -1 

    def add_symbol(self, name, symbol_info):

        kind = symbol_info['kind']

        actual_size_in_memory_units = symbol_info.get('size', 1) 

        if kind == 'parameter':
            symbol_info['address'] = self.next_param_offset
            self.next_param_offset += actual_size_in_memory_units 
            self.total_param_size += actual_size_in_memory_units

        elif kind == 'variable':
            if symbol_info.get('is_global'):

                pass
            else: 

                local_var_stack_size = 1 
                full_type_spec_local = symbol_info.get('full_type_spec')
                if isinstance(full_type_spec_local, dict) and full_type_spec_local.get('type') == 'ARRAY':
                    try:
                        low = int(full_type_spec_local['low']); high = int(full_type_spec_local['high'])
                        local_var_stack_size = (high - low + 1) if high >= low else 0
                    except: pass 
                symbol_info['size'] = local_var_stack_size 

                symbol_info['address'] = self.next_local_offset 
                self.next_local_offset -= local_var_stack_size 
                self.total_local_var_size += local_var_stack_size

        self.symbols[name] = symbol_info

    def lookup(self, name):
        if name in self.symbols: return self.symbols[name]
        if self.parent: return self.parent.lookup(name)
        return None

    def enter_scope(self, scope_name):
        new_scope = SymbolTable(parent=self, scope_name=scope_name)

        return new_scope

    def exit_scope(self):
        if not self.parent: raise SemanticError("Tentativa de sair do escopo global.")
        return self.parent

class SemanticAnalyzer:
    def __init__(self):
        self.current_scope = SymbolTable(scope_name="global")
        self.errors = [] 
        self.function_scopes = {} 
        self.global_address_counter = 0
        self._initialize_built_ins()

    def _initialize_built_ins(self):

        self.current_scope.add_symbol('WRITELN', {'kind': 'procedure', 'params_definition': {'accepts_variable_args': True}, 'return_type': 'VOID', 'built_in': True})
        self.current_scope.add_symbol('WRITE', {'kind': 'procedure', 'params_definition': {'accepts_variable_args': True}, 'return_type': 'VOID', 'built_in': True})
        self.current_scope.add_symbol('READLN', {'kind': 'procedure', 'params_definition': {'accepts_variable_args': True, 'arg_must_be_lvalue': True, 'allowed_types': ['INTEGER', 'REAL', 'STRING', 'BOOLEAN']}, 'return_type': 'VOID', 'built_in': True})
        self.current_scope.add_symbol('READ', {'kind': 'procedure', 'params_definition': {'accepts_variable_args': True, 'arg_must_be_lvalue': True, 'allowed_types': ['INTEGER', 'REAL', 'STRING', 'BOOLEAN']}, 'return_type': 'VOID', 'built_in': True})
        self.current_scope.add_symbol('LENGTH', {'kind': 'function', 'params_definition': {'fixed_args': [{'name': 'source_string', 'type': 'STRING'}]}, 'return_type': 'INTEGER', 'built_in': True})

    def analyze(self, ast):
        if ast is None: return False

        self.current_scope = SymbolTable(scope_name="global")
        self.global_address_counter = 0
        self._initialize_built_ins() 
        self.errors = [] 
        try:
            self.visit(ast)
        except SemanticError as e:
            self.errors.append(str(e))
        except Exception as e:
            import traceback
            self.errors.append(f"Erro Python inesperado na análise semântica: {e}\n{traceback.format_exc()}")

        if self.errors:
            print("\n--- Erros Semânticos Encontrados ---")
            for error_msg in self.errors: print(error_msg)
            return False
        else:
            print("\nAnálise Semântica Concluída. Nenhuns erros semânticos encontrados.")

            return True

    def print_scope_details(self, scope_to_print, indent_level=0): 
        prefix = "  " * indent_level
        print(f"{prefix}--- Escopo: {scope_to_print.scope_name} (Offset Máximo: {scope_to_print.current_offset}, Vars/Params Declarados: {scope_to_print.var_count}) ---")
        if not scope_to_print.symbols:
            print(f"{prefix}  (Este escopo específico não tem símbolos próprios definidos nele, além de built-ins se for o global)")

        sorted_symbols = sorted(scope_to_print.symbols.items())

        for name, info in sorted_symbols:
            if not info.get('built_in'):
                print(f"{prefix}  - Símbolo: {name}")
                for key, value in info.items():
                    if key == 'full_type_spec' and isinstance(value, dict):
                        print(f"{prefix}    {key}: Tipo Base='{value.get('type')}', Limites=[{value.get('low')}..{value.get('high')}], Tipo Elemento='{value.get('of_type')}'")
                    elif key == 'params' and isinstance(value, list):
                        print(f"{prefix}    {key}:")
                        for param_idx, param_detail in enumerate(value):
                            print(f"{prefix}      Param {param_idx+1}: Nome='{param_detail.get('name')}', Tipo='{param_detail.get('type')}'")
                    else:
                        print(f"{prefix}    {key}: {value}")
        print(f"{prefix}--- Fim do Escopo: {scope_to_print.scope_name} ---")

    def visit(self, node):
        if node is None: return None
        method_name = 'visit_' + type(node).__name__
        visitor_method = getattr(self, method_name, self.generic_visit)
        inferred_type = visitor_method(node)
        if inferred_type is not None and hasattr(node, 'lineno'): 
            node.inferred_type = inferred_type
        return inferred_type

    def generic_visit(self, node):
        for child_attr_name in dir(node): 
            if child_attr_name.startswith('_'): continue 
            child = getattr(node, child_attr_name)
            if isinstance(child, list):
                for item in child:
                    if isinstance(item, Node): self.visit(item)
            elif isinstance(child, Node):
                self.visit(child)
        return None 

    def visit_ProgramNode(self, node):
        self.current_scope.add_symbol(node.id.name.upper(), {'kind': 'program', 'lineno': node.lineno}) 
        self.visit(node.block)

    def visit_BlockNode(self, node):
        self.visit(node.declarations)
        self.visit(node.compound_statement)

    def visit_DeclarationsNode(self, node):
        if node: 
            for item in node.items:
                if isinstance(item, list): 
                    for var_decl_item in item: self.visit(var_decl_item)
                else: self.visit(item)

    def visit_VarDeclNode(self, node):
        type_spec_info = node.type_spec
        var_base_type = type_spec_info['type'] if isinstance(type_spec_info, dict) else type_spec_info

        var_declared_size = 1 
        if var_base_type == 'ARRAY':
            try:
                low = int(type_spec_info['low']); high = int(type_spec_info['high'])
                var_declared_size = (high - low + 1) if high >= low else 0
                if var_declared_size == 0 and high >= low: 
                    var_declared_size = 1
            except: var_declared_size = 0 

        for id_node in node.ids:
            symbol_data = {
                'kind': 'variable', 
                'type': var_base_type, 
                'full_type_spec': type_spec_info, 
                'lineno': id_node.lineno,
                'size': var_declared_size 
            }
            if self.current_scope.scope_name == "global":
                symbol_data['is_global'] = True
                symbol_data['address'] = self.global_address_counter
                self.global_address_counter += var_declared_size
            else: 
                symbol_data['is_global'] = False

            self.current_scope.add_symbol(id_node.name.upper(), symbol_data)

    def visit_FunctionDeclarationNode(self, node):
        param_details_for_symbol = []
        for param_node in node.params: 
            param_base_type = param_node.type_spec['type'] if isinstance(param_node.type_spec, dict) else param_node.type_spec

            parameter_slot_size = 1 

            for id_node_param in param_node.ids: 
                param_details_for_symbol.append({
                    'name': id_node_param.name.upper(), 
                    'type': param_base_type, 
                    'full_type_spec': param_node.type_spec, 
                    'lineno': id_node_param.lineno,
                    'size_on_stack': parameter_slot_size 
                })

        return_type_base = node.return_type['type'] if isinstance(node.return_type, dict) else node.return_type
        function_name_upper = node.id.name.upper()

        self.current_scope.add_symbol(
            function_name_upper,
            {'kind': 'function', 
             'params': param_details_for_symbol, 
             'return_type': return_type_base, 
             'full_return_type_spec': node.return_type, 
             'lineno': node.lineno, 
             'is_global': (self.current_scope.scope_name == "global")}
        )

        old_scope = self.current_scope
        self.current_scope = self.current_scope.enter_scope(function_name_upper) 
        self.function_scopes[function_name_upper] = self.current_scope

        for param_detail in param_details_for_symbol:
            param_data = {
                'kind': 'parameter', 
                'type': param_detail['type'], 
                'full_type_spec': param_detail['full_type_spec'], 
                'lineno': param_detail['lineno'],
                'is_global': False,
                'size': param_detail['size_on_stack'] 
            }
            self.current_scope.add_symbol(param_detail['name'], param_data)

        self.visit(node.block) 

        self.current_scope = old_scope

    def visit_CompoundStatementNode(self, node):
        if node: 
            for statement in getattr(node, 'statements', []):
                self.visit(statement)

    def visit_AssignmentNode(self, node):
        lhs_var_node = node.var 
        lhs_type = self.visit(lhs_var_node) 
        rhs_type = self.visit(node.expr)

        var_name = ""
        if isinstance(lhs_var_node, IDNode): var_name = lhs_var_node.name.upper()
        elif isinstance(lhs_var_node, ArrayAccessNode): var_name = lhs_var_node.id.name.upper()

        if lhs_type == 'UNKNOWN_TYPE' or rhs_type == 'UNKNOWN_TYPE': return

        is_return_assignment = False

        if self.current_scope.parent is not None and self.current_scope.parent.scope_name == "global": 

            current_function_scope_name_upper = self.current_scope.scope_name 

            function_symbol_from_parent = self.current_scope.parent.lookup(current_function_scope_name_upper)

            if function_symbol_from_parent and function_symbol_from_parent['kind'] == 'function' and \
               isinstance(lhs_var_node, IDNode) and lhs_var_node.name.upper() == current_function_scope_name_upper:
                is_return_assignment = True
                expected_return_type = function_symbol_from_parent['return_type']
                if (expected_return_type == 'REAL' and rhs_type == 'INTEGER') or expected_return_type == rhs_type:
                    pass
                else:
                    self.errors.append(f"Erro Semântico: Tipo incompatível para valor de retorno da função '{current_function_scope_name_upper}'. Esperado '{expected_return_type}', recebido '{rhs_type}' na linha {node.lineno}.")

        if not is_return_assignment: 
            if lhs_type == 'REAL' and rhs_type == 'INTEGER':
                pass
            elif lhs_type != rhs_type:
                self.errors.append(f"Erro Semântico: Atribuição de tipos incompatíveis. Variável '{var_name}' (tipo: {lhs_type}) não pode receber expressão do tipo '{rhs_type}' na linha {node.lineno}.")

    def visit_IDNode(self, node):
        node_name_upper = node.name.upper()
        if node_name_upper == 'TRUE' or node_name_upper == 'FALSE':
            return 'BOOLEAN' 

        symbol = self.current_scope.lookup(node_name_upper)
        if not symbol:
            self.errors.append(f"Erro Semântico: Identificador '{node.name}' não declarado na linha {node.lineno}.")
            return 'UNKNOWN_TYPE'

        current_func_scope_name = self.current_scope.scope_name 
        if self.current_scope.parent and self.current_scope.parent.scope_name == "global": 
            parent_func_symbol = self.current_scope.parent.lookup(current_func_scope_name)
            if parent_func_symbol and parent_func_symbol['kind'] == 'function' and node_name_upper == current_func_scope_name:
                return parent_func_symbol['return_type']

        if symbol['kind'] == 'function':

            return symbol.get('return_type', 'UNKNOWN_TYPE') 

        return symbol['type'] 

    def visit_ArrayAccessNode(self, node):
        array_id_node = node.id 
        array_name_upper = array_id_node.name.upper()
        symbol = self.current_scope.lookup(array_name_upper)

        if not symbol:
            self.errors.append(f"Erro Semântico: Array '{array_id_node.name}' não declarado na linha {node.lineno}.")
            return 'UNKNOWN_TYPE'

        if not (symbol['kind'] == 'variable' and isinstance(symbol.get('full_type_spec'), dict) and symbol['full_type_spec'].get('type') == 'ARRAY'):
            self.errors.append(f"Erro Semântico: Identificador '{array_id_node.name}' não é um array na linha {node.lineno}.")
            return 'UNKNOWN_TYPE'

        index_type = self.visit(node.index_expr)
        if index_type != 'INTEGER':
            self.errors.append(f"Erro Semântico: Índice de array para '{array_id_node.name}' deve ser INTEGER, mas é '{index_type}' na linha {getattr(node.index_expr, 'lineno', node.lineno)}.")

        return symbol['full_type_spec']['of_type']

    def visit_BinOpNode(self, node): 
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.op 
        result_type = 'UNKNOWN_TYPE'

        if left_type == 'UNKNOWN_TYPE' or right_type == 'UNKNOWN_TYPE': pass 
        elif op in ['PLUS', 'MINUS', 'TIMES']:
            if left_type == 'INTEGER' and right_type == 'INTEGER': result_type = 'INTEGER'
            elif (left_type == 'REAL' and right_type == 'REAL') or \
                 (left_type == 'REAL' and right_type == 'INTEGER') or \
                 (left_type == 'INTEGER' and right_type == 'REAL'): result_type = 'REAL'
            else: self.errors.append(f"Erro Semântico: Operação aritmética '{op}' entre tipos '{left_type}' e '{right_type}' inválida na linha {node.lineno}.")
        elif op == 'DIVIDE':
            if (left_type in ['INTEGER', 'REAL']) and (right_type in ['INTEGER', 'REAL']): result_type = 'REAL'
            else: self.errors.append(f"Erro Semântico: Operador '/' requer operandos numéricos, mas obteve '{left_type}' e '{right_type}' na linha {node.lineno}.")
        elif op == 'DIV_OP':
            if left_type == 'INTEGER' and right_type == 'INTEGER': result_type = 'INTEGER'
            else: self.errors.append(f"Erro Semântico: Operador 'DIV_OP' (div) requer operandos INTEGER, mas obteve '{left_type}' e '{right_type}' na linha {node.lineno}.")
        elif op == 'MOD_OP':
            if left_type == 'INTEGER' and right_type == 'INTEGER': result_type = 'INTEGER'
            else: self.errors.append(f"Erro Semântico: Operador 'MOD_OP' (mod) requer operandos INTEGER, mas obteve '{left_type}' e '{right_type}' na linha {node.lineno}.")
        elif op in ['EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE']:
            if (left_type == right_type) or \
               (left_type in ['INTEGER', 'REAL'] and right_type in ['INTEGER', 'REAL']):
                result_type = 'BOOLEAN'
            else: self.errors.append(f"Erro Semântico: Comparação '{op}' entre tipos incompatíveis '{left_type}' e '{right_type}' na linha {node.lineno}.")
        elif op == 'AND_OP' or op == 'OR_OP':
            if left_type == 'BOOLEAN' and right_type == 'BOOLEAN': result_type = 'BOOLEAN'
            else: self.errors.append(f"Erro Semântico: Operador lógico '{op}' requer operandos BOOLEAN, mas obteve '{left_type}' e '{right_type}' na linha {node.lineno}.")
        else: self.errors.append(f"Erro Semântico: Operador binário desconhecido ou não tratado '{op}' na linha {node.lineno}.")
        return result_type

    def visit_UnaryOpNode(self, node):
        operand_type = self.visit(node.operand)
        op = node.op 
        result_type = 'UNKNOWN_TYPE'
        if operand_type == 'UNKNOWN_TYPE': pass
        elif op == 'MINUS':
            if operand_type in ['INTEGER', 'REAL']: result_type = operand_type
            else: self.errors.append(f"Erro Semântico: Operador '-' unário aplicado a tipo não numérico '{operand_type}' na linha {node.lineno}.")
        elif op == 'NOT_OP':
            if operand_type == 'BOOLEAN': result_type = 'BOOLEAN'
            else: self.errors.append(f"Erro Semântico: Operador 'NOT_OP' aplicado a tipo não BOOLEAN '{operand_type}' na linha {node.lineno}.")
        else: self.errors.append(f"Erro Semântico: Operador unário desconhecido ou não tratado '{op}' na linha {node.lineno}.")
        return result_type

    def visit_NumberNode(self, node):
        return 'INTEGER' if isinstance(node.value, int) else 'REAL'

    def visit_StringLiteralNode(self, node):
        return 'STRING'

    def visit_FunctionCallNode(self, node):
        func_name_to_lookup = node.id.name.upper()
        function_symbol = self.current_scope.lookup(func_name_to_lookup)

        if not function_symbol:
            self.errors.append(f"Erro Semântico: Função/Procedimento '{node.id.name}' não declarado na linha {node.lineno}.")
            return 'UNKNOWN_TYPE'

        if function_symbol['kind'] not in ['function', 'procedure']:
            self.errors.append(f"Erro Semântico: '{node.id.name}' não é uma função ou procedimento na linha {node.lineno}.")
            return 'UNKNOWN_TYPE'

        actual_args_nodes = node.args
        actual_args_types = [self.visit(arg_node) for arg_node in actual_args_nodes]

        expected_return_type = function_symbol.get('return_type', 'VOID') 

        if function_symbol.get('built_in'):
            params_def = function_symbol.get('params_definition', {})
            if params_def.get('accepts_variable_args'):
                if params_def.get('arg_must_be_lvalue'): 
                    allowed_lvalue_types = params_def.get('allowed_types', [])
                    for i, arg_node in enumerate(actual_args_nodes):
                        if not isinstance(arg_node, (IDNode, ArrayAccessNode)):
                            self.errors.append(f"Erro Semântico: Argumento {i+1} de '{func_name_to_lookup}' deve ser uma variável/array na linha {getattr(arg_node, 'lineno', node.lineno)}.")
                        elif actual_args_types[i] not in allowed_lvalue_types and actual_args_types[i] != 'UNKNOWN_TYPE':
                             self.errors.append(f"Erro Semântico: Argumento {i+1} de '{func_name_to_lookup}' tem tipo '{actual_args_types[i]}' não permitido para leitura. Permitidos: {allowed_lvalue_types} na linha {getattr(arg_node, 'lineno', node.lineno)}.")

            elif 'fixed_args' in params_def: 
                expected_fixed_args = params_def['fixed_args']
                if len(expected_fixed_args) != len(actual_args_types):
                    self.errors.append(f"Erro Semântico: Número de argumentos para '{func_name_to_lookup}'. Esperado: {len(expected_fixed_args)}, Recebido: {len(actual_args_types)} na linha {node.lineno}.")
                else:
                    for i, p_def in enumerate(expected_fixed_args):
                        expected_type = p_def['type'] 
                        actual_type = actual_args_types[i]
                        is_ok = False
                        if isinstance(expected_type, list): is_ok = actual_type in expected_type
                        else: is_ok = actual_type == expected_type
                        if not is_ok and not (expected_type == 'REAL' and actual_type == 'INTEGER'): 
                            if actual_type != 'UNKNOWN_TYPE': self.errors.append(f"Erro Semântico: Arg {i+1} para '{func_name_to_lookup}' espera '{expected_type}', recebeu '{actual_type}' na linha {getattr(actual_args_nodes[i], 'lineno', node.lineno)}.")
        else: 
            expected_user_params = function_symbol.get('params', []) 
            if len(expected_user_params) != len(actual_args_types):
                self.errors.append(f"Erro Semântico: Número de argumentos para '{func_name_to_lookup}'. Esperado: {len(expected_user_params)}, Recebido: {len(actual_args_types)} na linha {node.lineno}.")
            else:
                for i, expected_param_detail in enumerate(expected_user_params):
                    expected_type = expected_param_detail['type']
                    actual_type = actual_args_types[i]
                    if actual_type == 'UNKNOWN_TYPE': continue
                    if not (expected_type == actual_type or (expected_type == 'REAL' and actual_type == 'INTEGER')):
                        self.errors.append(f"Erro Semântico: Tipo de argumento para '{func_name_to_lookup}'. Param '{expected_param_detail.get('name', f'#{i+1}')}' espera '{expected_type}', recebeu '{actual_type}' na linha {getattr(actual_args_nodes[i], 'lineno', node.lineno)}.")

        return expected_return_type

    def visit_ReadLnCallNode(self, node): 

        if node.args: 
            simulated_id_node = IDNode('READLN', node.lineno)
            simulated_fcall_node = FunctionCallNode(simulated_id_node, node.args)
            simulated_fcall_node.lineno = node.lineno
            return self.visit(simulated_fcall_node) 
        return 'VOID'

    def visit_WriteLnCallNode(self, node): 
        if node.args is not None: 
            simulated_id_node = IDNode('WRITELN', node.lineno)
            simulated_fcall_node = FunctionCallNode(simulated_id_node, node.args)
            simulated_fcall_node.lineno = node.lineno
            return self.visit(simulated_fcall_node)
        return 'VOID'

    def visit_IfStatementNode(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != 'BOOLEAN':
            self.errors.append(f"Erro Semântico: Condição do IF deve ser BOOLEAN, mas é '{condition_type}' na linha {getattr(node.condition, 'lineno', node.lineno)}.")
        self.visit(node.then_statement)
        if node.else_statement: self.visit(node.else_statement)

    def visit_WhileStatementNode(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != 'BOOLEAN':
            self.errors.append(f"Erro Semântico: Condição do WHILE deve ser BOOLEAN, mas é '{condition_type}' na linha {getattr(node.condition, 'lineno', node.lineno)}.")
        self.visit(node.do_statement)

    def visit_ForStatementNode(self, node):
        self.visit(node.initial_assignment) 
        var_control_node = node.initial_assignment.var
        control_var_type = getattr(var_control_node, 'inferred_type', 'UNKNOWN_TYPE')

        if control_var_type != 'INTEGER':
            self.errors.append(f"Erro Semântico: Variável de controle do FOR '{var_control_node.name}' deve ser INTEGER, mas é '{control_var_type}' na linha {node.initial_assignment.lineno}.")

        limit_expr_type = self.visit(node.limit_expr)
        if limit_expr_type != 'INTEGER':
            self.errors.append(f"Erro Semântico: Expressão limite do FOR deve ser INTEGER, mas é '{limit_expr_type}' na linha {getattr(node.limit_expr, 'lineno', node.lineno)}.")

        self.visit(node.do_statement)

    def visit_ParameterNode(self, node): pass 
    def visit_empty(self, node): return None