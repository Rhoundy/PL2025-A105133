import os
import sys 
import ply.yacc as yacc 
from lexer import lexer 
from pascal_parser import parser 
from semantic_analyzer import SemanticAnalyzer 
from code_generator import CodeGenerator 
from ast_nodes import Node

def print_ast(node, indent=0):
    if node is None: return
    prefix = "  " * indent; node_type = type(node).__name__
    attrs_to_print = {};
    if hasattr(node, 'name'): attrs_to_print['name'] = node.name
    if hasattr(node, 'value'): attrs_to_print['value'] = node.value
    if hasattr(node, 'op'): attrs_to_print['op'] = node.op
    if hasattr(node, 'lineno'): attrs_to_print['line'] = node.lineno
    if hasattr(node, 'inferred_type') and node.inferred_type is not None: attrs_to_print['inf_type'] = node.inferred_type
    extra_info = ", ".join(f"{k}='{v}'" for k, v in attrs_to_print.items())
    print(f"{prefix}{node_type}({extra_info})")
    children_attrs = ['id', 'block', 'declarations', 'compound_statement', 'statements', 'items', 'ids', 'type_spec', 'var', 'expr', 'condition', 'then_statement', 'else_statement', 'do_statement', 'initial_assignment', 'limit_expr', 'args', 'params', 'left', 'right', 'operand', 'index_expr']
    for attr_name in children_attrs:
        if hasattr(node, attr_name):
            attr_value = getattr(node, attr_name)
            if isinstance(attr_value, Node): print_ast(attr_value, indent + 1)
            elif isinstance(attr_value, list):
                for item in attr_value:
                    if isinstance(item, Node): print_ast(item, indent + 1)

def run_test_suite(pascal_code_string, test_name="Teste", output_vm_dir="vm_outputs", generate_vm_code_if_analysis_ok=True):
    print(f"\n\n{'-'*30}\n>>> A EXECUTAR TESTE: {test_name}\n{'-'*30}")

    lexer.lineno = 1
    if hasattr(lexer, 'comment_nesting_level'):
        lexer.comment_nesting_level = 0

    current_lexer_state_func = getattr(lexer, 'current_state', lambda: 'INITIAL')
    while current_lexer_state_func() != 'INITIAL':
        lexer.pop_state()

    generated_ast = None

    semantic_analyzer_instance = SemanticAnalyzer() 
    analysis_phase_passed = False 

    try:

        generated_ast = parser.parse(pascal_code_string, lexer=lexer)

        if not generated_ast: 
            print(f"### RESULTADO: FALHA (Erro de Sintaxe Irrecuperável) - {test_name} ###")

            return False 

        semantic_analysis_ok = semantic_analyzer_instance.analyze(generated_ast)

        if not semantic_analysis_ok:
            print(f"### RESULTADO: FALHA (Erro Semântico) - {test_name} ###")

            return False 

        analysis_phase_passed = True
        print(f"### RESULTADO: SUCESSO (Análise) - {test_name} ###")

        if generate_vm_code_if_analysis_ok: 

            code_gen_instance = CodeGenerator(semantic_analyzer_instance) 

            vm_code_output_string = code_gen_instance.generate_code(generated_ast)

            current_errors_in_sa = semantic_analyzer_instance.errors 

            if current_errors_in_sa: 
                 print("\n--- Erros Reportados DURANTE/APÓS a Geração de Código ---")
                 for error_msg in current_errors_in_sa: 
                     print(error_msg)
                 print(f"### GERAÇÃO DE CÓDIGO COM ERROS para: {test_name} ###")

            if vm_code_output_string:

                if output_vm_dir:

                    if not os.path.exists(output_vm_dir): os.makedirs(output_vm_dir)

                    vm_output_filename = os.path.splitext(os.path.basename(test_name.split(" (")[0]))[0] + ".vm"
                    vm_output_filepath = os.path.join(output_vm_dir, vm_output_filename)
                    try:
                        with open(vm_output_filepath, 'w', newline='\n') as f:

                            f.write(vm_code_output_string)
                        print(f"Código VM salvo em: {vm_output_filepath}")
                    except Exception as e_write:
                        print(f"ERRO ao salvar código VM em {vm_output_filepath}: {e_write}")
                        if vm_code_output_string: print("\n--- Código VM (Consola) ---\n" + vm_code_output_string)
                else:
                    print("\n--- Código VM (Consola) ---")
                    print(vm_code_output_string)

        return analysis_phase_passed 

    except Exception: 
        print(f"\n!!!!!! ERRO CRÍTICO NO TEST RUNNER para: '{test_name}' !!!!!!!")
        import traceback
        traceback.print_exc()
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return False 

if __name__ == '__main__':
    test_dir = "semantic_tests"
    output_dir = "vm_outputs" 
    if not os.path.exists(test_dir): os.makedirs(test_dir)
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    all_test_files_info = [
            ("test_valid_declarations.pas", "Declarações válidas"),
            ("test_undeclared_var_assign.pas", "Var não declarada (atrib)"), 
            ("test_undeclared_var_expr.pas", "Var não declarada (expr)"),    
            ("test_redeclare_var.pas", "Redeclaração de var"),            
            ("test_assign_valid.pas", "Atribuições válidas"),
            ("test_assign_type_mismatch.pas", "Atribuições inválidas"),      
            ("test_expr_arithmetic_valid.pas", "Expr aritméticas válidas"),
            ("test_expr_arithmetic_invalid.pas", "Expr aritméticas inválidas"),
            ("test_expr_logical_valid.pas", "Expr lógicas válidas"),
            ("test_expr_logical_invalid.pas", "Expr lógicas inválidas"),    
            ("test_array_valid_access.pas", "Array válido"),
            ("test_array_invalid_index_type.pas", "Array índice inválido"),  
            ("test_array_access_non_array.pas", "Acesso a não-array"),       
            ("test_if_while_valid_condition.pas", "IF/WHILE válidos"),
            ("test_if_while_invalid_condition.pas", "IF/WHILE inválidos"),  
            ("test_for_loop_valid.pas", "FOR válido"),
            ("test_for_loop_invalid.pas", "FOR inválido"),                 
            ("test_builtins_writeln_readln.pas", "Builtins I/O"),
            ("test_builtins_length.pas", "Builtin LENGTH"),               
            ("test_readln_invalid_arg.pas", "READLN arg inválido (expr)"),
            ("test_function_user_defined_valid.pas", "Função BinToInt válida"),
            ("test_function_user_defined_call_errors.pas", "Chamadas de função com erros") 
        ]
    if len(sys.argv) > 1 and sys.argv[1] != "all":

        specific_test_file = sys.argv[1]
        if os.path.exists(( specific_test_file)):
            print(f"Executando teste específico: {specific_test_file}")
            specific_tests_to_run = [specific_test_file.split("/")[-1]]  
        else:
            print(f"Ficheiro de teste '{specific_test_file}' não encontrado no diretório '{test_dir}'.")
    else:

        specific_tests_to_run = ["test_assign_valid.pas", "test_array_valid_access.pas"]

    if len(sys.argv) > 1 and sys.argv[1] == "all":
        specific_tests_to_run = None  

    passed_count = 0
    failed_count = 0
    generated_code_count = 0

    tests_to_process = all_test_files_info
    if specific_tests_to_run:
        tests_to_process = [t for t in all_test_files_info if t[0] in specific_tests_to_run]
        if not tests_to_process:
            print("Nenhum dos testes especificados em `specific_tests_to_run` foi encontrado em `all_test_files_info`.")

    for filename, description in tests_to_process:
        full_test_name = f"{filename} ({description})"
        filepath = os.path.join(test_dir, filename)

        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                pascal_code = f.read()

            should_pass_analysis = "ESPERA ERRO" not in description.upper() 

            test_passed_analysis = run_test_suite(pascal_code, full_test_name, output_dir, generate_vm_code_if_analysis_ok=should_pass_analysis)

            if test_passed_analysis and should_pass_analysis:
                passed_count +=1
                generated_code_count +=1 
                print(f"Resultado para {full_test_name}: PASSOU ANÁLISE (VM gerada)")
            elif not test_passed_analysis and not should_pass_analysis:
                passed_count +=1
                print(f"Resultado para {full_test_name}: PASSOU (Erro esperado foi corretamente detetado)")
            else:
                failed_count +=1
                print(f"Resultado para {full_test_name}: FALHOU (Comportamento inesperado)")
        else:
            print(f"\nAVISO: Ficheiro de teste '{filepath}' não encontrado.")
            failed_count +=1 

    print(f"\n\n{'-'*30}\nSUMÁRIO DOS TESTES:\n  Passaram: {passed_count}\n  Falharam: {failed_count}\n  Código VM Gerado para: {generated_code_count} testes (que passaram análise)\n{'-'*30}")