program CondInvalid;
var i: INTEGER;
begin
  i := 1;
  IF i THEN WRITELN('oops');  { Erro: i é INTEGER }
  WHILE 0 DO WRITELN('loop'); { Erro: 0 é INTEGER }
end.