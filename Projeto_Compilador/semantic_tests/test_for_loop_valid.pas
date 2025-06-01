program ForValid;
var i, sum: INTEGER;
begin
  sum := 0;
  FOR i := 1 TO 5 DO
    sum := sum + i;
  WRITELN(sum); { Deve ser 15 }
end.