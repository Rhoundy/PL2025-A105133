program ExprLogicalValid;
var
  i1, i2: INTEGER;
  b1, b2, b3: BOOLEAN;
begin
  i1 := 10; i2 := 5;
  b1 := i1 > i2;             { TRUE }
  b2 := (i1 <> 10) OR_OP (i2 = 5); { FALSE OR TRUE -> TRUE }
  b3 := NOT_OP (b1 AND_OP b2);   { NOT (TRUE AND TRUE) -> FALSE }
  WRITELN(b1, b2, b3);
end.