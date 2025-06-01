program ValidDecls;
var
  i: INTEGER;
  r: REAL;
  b: BOOLEAN;
  s: STRING;
  arr: ARRAY [1..5] OF INTEGER;
begin
  i := 1;
  r := 2.5;
  b := TRUE;
  s := 'test';
  arr[1] := i;
  WRITELN(s, i, r, b, arr[1]);
end.