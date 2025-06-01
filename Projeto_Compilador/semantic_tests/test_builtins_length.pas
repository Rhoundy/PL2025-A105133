program TestLength;
var 
  s: STRING;
  len: INTEGER;
  i: INTEGER;
begin
  s := 'Pascal';
  len := LENGTH(s);
  WRITELN(len); { Deve ser 6 }
  i := LENGTH(len); { Erro: LENGTH espera STRING }
end.