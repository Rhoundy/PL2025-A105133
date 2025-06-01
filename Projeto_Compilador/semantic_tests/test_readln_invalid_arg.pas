program ReadlnInvalidArg;
var 
  i: INTEGER;
begin
  i := 0;
  READLN(i + 1); (* Erro: i+1 nao e uma variavel (L-value) *)
end.
    