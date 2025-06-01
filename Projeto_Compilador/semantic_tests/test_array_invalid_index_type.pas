program ArrayInvalidIndex;
var
  a: ARRAY [1..5] OF INTEGER;
  r_idx: REAL;
begin
  r_idx := 2.0;
  a[r_idx] := 100; { Erro aqui }
end.