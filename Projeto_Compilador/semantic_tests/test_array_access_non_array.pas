program AccessNonArray;
var
  i: INTEGER;
begin
  i := 1;
  i[0] := 10; (* Erro: 'i' nao e um array *)
end.
