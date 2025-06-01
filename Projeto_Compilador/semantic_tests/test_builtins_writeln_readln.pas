program TestBuiltinsIO;
var 
  i: INTEGER;
  s: STRING;
  r: REAL;
begin
  WRITELN('Introduza um inteiro, uma string e um real:');
  READLN(i, s, r);
  WRITE('Lido: '); { Usa WRITE se o tiveres adicionado aos builtins }
  WRITELN(i, ' ', s, ' ', r);
end.