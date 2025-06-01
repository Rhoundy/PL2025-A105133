program AssignValid;
var
  i: INTEGER;
  r: REAL;
  b: BOOLEAN;
  s: STRING;
begin
  i := 100;
  r := 2.5;
  r := i; { Int -> Real }
  b := FALSE;
  s := 'valid string';
  WRITELN(s, r, b);
end.