program AssignTypeMismatch;
var
  i: INTEGER;
  r: REAL;
  b: BOOLEAN;
  s: STRING;
begin
  i := 1.5;       { Erro: REAL to INTEGER }
  b := 0;         { Erro: INTEGER to BOOLEAN }
  s := i;         { Erro: INTEGER to STRING }
  r := 'hello';   { Erro: STRING to REAL }
end.