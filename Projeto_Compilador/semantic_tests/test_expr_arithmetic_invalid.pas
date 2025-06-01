program ExprArithmeticInvalid;
var 
  i: INTEGER;
  s: STRING;
  b: BOOLEAN;
begin
  i := 1; s := 'a'; b := TRUE;
  i := i + s; { Erro }
  i := b * i; { Erro }
end.