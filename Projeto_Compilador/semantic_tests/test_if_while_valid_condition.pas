program CondValid;
var i: INTEGER; b: BOOLEAN;
begin
  i := 0; b := TRUE;
  IF i < 10 THEN i := i + 1;
  WHILE (i > 0) AND_OP b DO
  begin
    i := i - 1;
    IF i = 0 THEN b := FALSE;
  end;
  WRITELN(i,b);
end.