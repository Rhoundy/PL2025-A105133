program ArrayValidAccess;
var
  numbers: ARRAY [0..4] OF INTEGER;
  idx: INTEGER;
begin
  idx := 2;
  numbers[0] := 10;
  numbers[idx] := numbers[0] + 5;
  WRITELN(numbers[2]); { Deve ser 15 }
end.