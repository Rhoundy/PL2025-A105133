program ForInvalid;
var i: INTEGER; r: REAL; b: BOOLEAN;
begin
  r := 1.0;
  FOR i := r TO 5 DO WRITELN('a');    { Erro: limite inicial REAL }
  FOR b := TRUE TO FALSE DO WRITELN('b'); { Erro: var de controlo BOOLEAN }
end.