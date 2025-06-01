program BinarioParaInteiroValid;
var 
  bin_input: STRING;
  result_val: INTEGER;

FUNCTION BinToInt(bin_str_param: STRING): INTEGER; { Nome do parametro alterado para evitar confusao com var global }
  VAR
    idx, local_valor, local_potencia: INTEGER; { Nomes locais alterados }
    current_char_as_str : STRING; { Para simular char access }
  BEGIN
    local_valor := 0;
    local_potencia := 1;

    (* O acesso real a char de string e comparacao precisariam de logica mais detalhada.
       Ex: bin_str_param[idx] ou uma funcao get_char(str, idx).
       A semantica de bin_str_param[idx] precisa ser definida (retorna CHAR? STRING[1]?).
       Por agora, vamos focar na estrutura da chamada e definicao da funcao. 
       Esta implementacao de BinToInt e conceptualmente errada para a logica real,
       mas serve para testar a declaracao/chamada de funcao. *)

    IF LENGTH(bin_str_param) > 0 THEN
    BEGIN
        FOR idx := LENGTH(bin_str_param) DOWNTO 1 DO 
        BEGIN
          (* Simulacao de obter um char - na pratica isto e complexo *)
          (* if char_at(bin_str_param, idx) = '1' then *)
          (* Esta linha abaixo e apenas um placeholder para o IF, para que compile e rode o loop *)
          IF bin_str_param <> 'nao_vai_ser_igual_para_testar_o_if' THEN 
            local_valor := local_valor + local_potencia;
          local_potencia := local_potencia * 2;
        END;
    END;
    BinToInt := local_valor; (* Atribui ao nome da funcao para retornar valor *)
  END;

BEGIN { Bloco principal }
  bin_input := '101';
  WRITELN('A chamar BinToInt com: ', bin_input);
  result_val := BinToInt(bin_input);
  WRITELN('Resultado (BinToInt): ', result_val); 
  { O resultado aqui nao sera 5 com a logica simplificada acima, mas o teste e da chamada }
END.
