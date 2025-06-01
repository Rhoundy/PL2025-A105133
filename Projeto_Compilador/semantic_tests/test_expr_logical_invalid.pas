program ExprLogicalInvalid;
var
  i1: INTEGER;
  b1: BOOLEAN;
begin
  i1 := 1;
  b1 := i1 AND_OP 0;    { Erro: AND com inteiros }
  b1 := NOT_OP i1;      { Erro: NOT com inteiro }
end.