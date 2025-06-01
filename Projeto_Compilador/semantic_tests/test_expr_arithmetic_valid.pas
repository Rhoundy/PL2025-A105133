program ExprArithmeticValid;
var 
  i1, i2, i3: INTEGER;
  r1, r2: REAL;
begin
  i1 := 10; i2 := 20;
  i3 := i1 + i2 * 2;       { i3 = 50 }
  r1 := i1 / 4;            { r1 = 2.5 }
  r2 := (i1 + i2) / r1;    { r2 = 30 / 2.5 = 12.0 }
  i3 := i2 DIV_OP i1;        { i3 = 2 }
  i1 := i2 MOD_OP 3;         { i1 = 2 }
  WRITELN(i1, i3, r1, r2);
end.